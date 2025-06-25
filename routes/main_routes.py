from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from werkzeug.utils import secure_filename
from models.models import SearchHistory
from extensions import db
from models_loader import MODELS
import os
import json
from search_core.main import search_similar_images

main_bp = Blueprint('main', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Please log in.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@main_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    uploaded_filename = None

    if request.method == 'POST':
        file = request.files.get('query_image')
        selected_models = request.form.getlist('models')
        similarity_method = request.form.get('similarity_method')
        results_count = request.form.get('results_count')

        if not file or file.filename == '' or not allowed_file(file.filename):
            return "Invalid file"

        if not selected_models:
            return "No model selected"

        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        uploaded_filename = filename

        print("Models:", selected_models)
        print("Method:", similarity_method)
        print("Count:", results_count)

    return render_template('index.html', uploaded_filename=uploaded_filename)

@main_bp.route('/search', methods=['POST'])
def search():
    current_user = {
        "id": session.get('user_id'),
        "username": session.get('username'),
    }

    query_image_id = request.form.get('query_image')
    if not query_image_id:
        print("No image file received!")
        return "No image file received", 400

    top_x = request.form.get('results_count')
    top_x = int(top_x)
    if not top_x:
        top_x=20

    similarity = request.form.get('similarity_method')
    if not similarity:
        similarity="euclidean"
    
    model_keys = request.form.getlist('models')  # e.g. ['vgg16', 'resnet50']
    if not model_keys:
        print("No model received!")
        return "No model received", 400

    retrieved_paths, metrics, plot_path = search_similar_images(
        query_image_id=query_image_id,
        model_keys=model_keys,
        metric=similarity,
        top_k=top_x,
        image_folder='image.orig'
    )

    if retrieved_paths and metrics:
        history_entry = SearchHistory(
            user_id=current_user['id'],
            query_image_id=query_image_id,
            model_keys=','.join(model_keys),
            similarity_metric=similarity,
            retrieved_paths=json.dumps(retrieved_paths),
            metrics=metrics,
            plot_path=plot_path
        )

        db.session.add(history_entry)
        db.session.commit()

    return redirect(url_for('main.results'))

@main_bp.route('/results')
def results():
    current_user = {
        "id": session.get('user_id'),
        "username": session.get('username'),
    }

    # Query all searches, ordered by newest first
    searches = SearchHistory.query.filter(SearchHistory.user_id == current_user["id"]).order_by(SearchHistory.timestamp.desc()).all()

    processed_searches = []
    i=len(searches)
    for s in searches:
        metrics = {}
        if s.metrics:
            metrics = {
                'final_precision': s.metrics.get('final_precision'),
                'final_recall': s.metrics.get('final_recall'),
                'average_precision': s.metrics.get('average_precision'),
                'r_precision': s.metrics.get('r_precision'),
                'found_relevant': s.metrics.get('found_relevant'),
                'total_relevant': s.metrics.get('total_relevant')
            }
            

        processed_searches.append({
            'id': s.id,
            'timestamp': s.timestamp,
            'query_image_id': s.query_image_id,
            'model_keys': s.model_keys,
            'similarity_metric': s.similarity_metric,
            'metrics': metrics,
            'retrieved_paths': s.retrieved_paths or '',
            'plot_path': s.plot_path or '',
            'nr': i,
        })
        i = i - 1

    return render_template('results.html', search_history=processed_searches)


