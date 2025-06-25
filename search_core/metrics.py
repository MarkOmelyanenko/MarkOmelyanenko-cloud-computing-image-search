import os
import matplotlib.pyplot as plt
import torch
import uuid

def compute_rp(top, query_name, retrieved_image_paths, features_dict, save_dir="search_core/metrics"):
    """
    Calculates Precision/Recall based on the name of the query image and the list of images found.
    Saves a .txt file with Precision/Recall values.
    """
    os.makedirs(save_dir, exist_ok=True)
    base_id = int(query_name) // 100

    total_relevant = sum(1 for name in features_dict if int(name) // 100 == base_id)

    result_labels = []
    for path in retrieved_image_paths[:top]:
        name = os.path.basename(path).split('.')[0]
        group_id = int(name) // 100
        result_labels.append("relevant" if group_id == base_id else "irrelevant")

    recall_precision = []
    relevant_count = 0

    for i, label in enumerate(result_labels):
        if label == "relevant":
            relevant_count += 1
        precision = relevant_count / (i + 1)
        recall = relevant_count / total_relevant if total_relevant > 0 else 0
        recall_precision.append((precision * 100, recall * 100))

    out_file = os.path.join(save_dir, f"{query_name}_RP.txt")
    with open(out_file, 'w') as f:
        for p, r in recall_precision:
            f.write(f"{p:.2f} {r:.2f}\n")

    print(f"[✓] RP saved to: {out_file}")
    return recall_precision



def display_rp(query_name, model_name="VGG16", save_dir="search_core/metrics/"):
    """
    Builds an RP graph from a .txt file saved by compute_rp()
    """
    file_path = os.path.join(save_dir, f"{query_name}_RP.txt")
    if not os.path.exists(file_path):
        print(f"[✗] File not found: {file_path}")
        return

    x, y = [], []
    with open(file_path, 'r') as f:
        for line in f:
            try:
                p, r = map(float, line.strip().split())
                x.append(r)
                y.append(p)
            except:
                continue

    plt.figure(figsize=(8, 6))
    plt.plot(x, y, marker='o', label=model_name)
    plt.xlabel("Recall (%)")
    plt.ylabel("Precision (%)")
    plt.title(f"Recall/Precision Curve – Query: {query_name}")
    plt.legend()
    plt.grid(True)

    unique_id = uuid.uuid4().hex
    image_path = os.path.join("plots", f"{str(unique_id)}.png")
    full_image_path = os.path.join("static", image_path)
    plt.savefig(full_image_path)
    plt.show()
    print(f"[✓] RP graph saved to: {image_path}")

    return image_path

def compute_average_precision(recall_precision_list):
    """
    Calculates Average Precision (AP) for a single query
    recall_precision_list — list (precision, recall)
    """
    recall_precision_list = sorted(recall_precision_list, key=lambda x: x[1])
    precisions = [p for p, r in recall_precision_list]
    return sum(precisions) / len(precisions)


def compute_r_precision(query_name, features_dict, retrieved_image_paths):
    """
    Calculates R-Precision for a single query
    """
    query_class = int(query_name) // 100

    R = sum(1 for name in features_dict if int(name) // 100 == query_class)

    if R == 0:
        return 0.0

    top_R_paths = retrieved_image_paths[:R]

    count_relevant = 0
    for path in top_R_paths:
        name = os.path.basename(path).split('.')[0]
        if int(name) // 100 == query_class:
            count_relevant += 1

    return count_relevant / R

def compute_map(all_ap):
    """
    Calculates Mean Average Precision (mAP) for multiple queries
    """
    if not all_ap:
        return 0.0
    return sum(all_ap) / len(all_ap)
