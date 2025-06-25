import numpy as np
import os

def convert_to_dict(raw_features):
    """Converts a list (path, vector) into a dictionary name → vector"""
    features_dict = {}
    for path, vector in raw_features:
        name = os.path.splitext(os.path.basename(path))[0]
        features_dict[name] = vector
    return features_dict

def combine_features(*dicts):
    """
    Accepts multiple dictionaries features_dict.
    Combines vectors by key (image name).
    """
    combined = {}
    all_keys = set(dicts[0].keys())
    for d in dicts[1:]:
        all_keys &= set(d.keys())  # we only keep shared keys

    for name in all_keys:
        vectors = [d[name] for d in dicts]
        combined[name] = np.concatenate(vectors)
    return combined
