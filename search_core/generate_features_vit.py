import os
import pickle
from PIL import Image
from tqdm import tqdm
import torch
import torchvision.models as models
from torchvision.models import ViT_B_16_Weights

image_folder = "image.orig"
output_pkl = "static/features/VIT.pkl"
os.makedirs("static/features", exist_ok=True)

device = torch.device("mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu")
weights = ViT_B_16_Weights.DEFAULT
vit = models.vit_b_16(weights=weights).to(device)
vit.eval()

preprocess = weights.transforms()

features = []

for filename in tqdm(os.listdir(image_folder)):
    if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        continue

    img_path = os.path.join(image_folder, filename)
    image = Image.open(img_path).convert("RGB")
    input_tensor = preprocess(image).unsqueeze(0).to(device)

    with torch.no_grad():
        x = vit._process_input(input_tensor)
        cls_token = vit.class_token.expand(x.shape[0], -1, -1)
        x = torch.cat((cls_token, x), dim=1)
        x = vit.encoder(x)
        cls_embedding = x[:, 0]  # CLS

    features.append((img_path, cls_embedding.cpu().numpy().flatten()))

with open(output_pkl, "wb") as f:
    pickle.dump(features, f)

print(f"[✓] VIT features saved to: {output_pkl}")
