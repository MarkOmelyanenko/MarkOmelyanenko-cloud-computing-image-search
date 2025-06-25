import pickle

def load_models():
    models = {}
    model_names = ['mobilenet', 'resnet50', 'vit16', 'vgg16']
    for name in model_names:
        with open(f'static/features/{name}.pkl', 'rb') as f:
            models[name] = pickle.load(f)
    return models

# Load once globally
MODELS = load_models()
