from extensions import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class SearchHistory(db.Model):
    __tablename__ = 'search_history'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    query_image_id = db.Column(db.String, nullable=False)
    model_keys = db.Column(db.String, nullable=False)
    similarity_metric = db.Column(db.String, nullable=False)
    retrieved_paths = db.Column(db.Text, nullable=False)
    metrics = db.Column(db.JSON, nullable=False)
    plot_path = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
