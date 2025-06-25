import os
from search_core.features_loading import features_data
from search_core.search_engine import recherche
from search_core.metrics import compute_rp, display_rp, compute_average_precision, compute_r_precision
from search_core.features_utils import convert_to_dict, combine_features

def search_similar_images(query_image_id, model_keys, metric="euclidean", top_k=20, image_folder="image.orig"):
    """
    Run image search for a given query image ID and selected model(s).
    
    Parameters:
        query_image_id (str): ID of the query image (without extension).
        model_keys (list[str]): List of model keys, e.g. ["vgg16", "resnet50"].
        metric (str): Distance metric to use, default "euclidean".
        top_k (int): Number of top results to return.
        image_folder (str): Folder where images are stored.
    
    Returns:
        retrieved_paths (list[str]): List of file paths for the top similar images.
        metrics (dict): Dictionary with precision, recall, average precision, and R-precision.
    """
    # Load features for each model
    feature_dicts = []
    for key in model_keys:
        raw = features_data[key]
        print(f"[✓] Loaded features for: {key}")
        feature_dicts.append(convert_to_dict(raw))

    # Combine features if more than one model
    if len(feature_dicts) == 1:
        features = feature_dicts[0]
    else:
        features = combine_features(*feature_dicts)
        print(f"[✓] Combined {len(feature_dicts)} descriptors")

    # Search for similar images
    retrieved_paths = recherche(query_image_id, features, image_folder, top=top_k, metric=metric)

    # Compute metrics
    rp_points = compute_rp(top_k, query_image_id, retrieved_paths, features)
    plot_path = display_rp(query_image_id, model_name="+".join(model_keys).upper())
    ap = compute_average_precision(rp_points)
    r_prec = compute_r_precision(query_image_id, features, retrieved_paths)
    final_p, final_r = rp_points[-1]

    query_class = int(query_image_id) // 100
    total_relevant = sum(1 for name in features if int(name) // 100 == query_class)
    found_relevant = sum(1 for path in retrieved_paths if int(os.path.basename(path).split('.')[0]) // 100 == query_class)

    metrics = {
        "final_precision": final_p,
        "final_recall": final_r,
        "average_precision": ap,
        "r_precision": r_prec,
        "found_relevant": found_relevant,
        "total_relevant": total_relevant,
    }

    # Optional: Display metrics (remove if you want pure function)
    print(f"📊 Final Precision: {final_p:.2f}%")
    print(f"📊 Final Recall: {final_r:.2f}%")
    print(f"📊 Average Precision (AP): {ap:.2f}")
    print(f"📊 R-Precision: {r_prec:.2f}")
    print(f"🧮 Found relevant: {found_relevant}")
    print(f"🧮 Total relevant in dataset: {total_relevant}")

    return retrieved_paths, metrics, plot_path
