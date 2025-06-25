import os
from search_core.similarity_functions import euclidean, chiSquareDistance, bhatta
from matplotlib.pyplot import imread
import matplotlib.pyplot as plt
import math

def getkVoisins(features_dict, query_name, k, metric='euclidean'):
    if query_name not in features_dict:
        raise ValueError(f"Query {query_name} not in features!")

    query_vector = features_dict[query_name]

    metric_func = {
        'euclidean': euclidean,
        'chi2': chiSquareDistance,
        'bhatta': bhatta
    }.get(metric, euclidean)

    distances = []
    for name, vector in features_dict.items():
        dist = metric_func(query_vector, vector)
        distances.append((name, dist))

    distances.sort(key=lambda x: x[1])
    return distances[:k]

def recherche(query_name, features_dict, image_folder, top=20, metric='euclidean', save_dir='search_core/results'):
    voisins = getkVoisins(features_dict, query_name, top, metric)
    image_paths = []
    for name, _ in voisins:
        path = os.path.join(image_folder, name + ".jpg")
        if os.path.exists(path):
            image_paths.append(path)

    plt.figure(figsize=(5, 5))
    plt.imshow(imread(os.path.join(image_folder, query_name + ".jpg")))
    plt.title("Query Image")
    plt.axis("off")

    query_save_path = os.path.join(save_dir, f"{query_name}_query.png")
    plt.savefig(query_save_path)
    plt.close()
    print(f"[✓] Query image saved to: {query_save_path}")

    plt.figure(figsize=(20, 10))
    cols = 5
    rows = math.ceil(len(image_paths) / cols)
    for i, path in enumerate(image_paths):
        plt.subplot(rows, cols, i + 1)
        plt.imshow(imread(path))
        plt.title(f"Similar #{i + 1}")
        plt.axis('off')

    plt.tight_layout()
    plt.show()

    # --- Saving to results folder ---
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, f"{query_name}_TOP{top}.png")
    plt.savefig(save_path)
    print(f"[✓] Similarity figure saved to: {save_path}")

    return image_paths
