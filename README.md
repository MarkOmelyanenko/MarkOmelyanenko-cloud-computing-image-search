# 🖼️ Image Retrieval System

This project is a lightweight content-based image retrieval (CBIR) application. It lets users search for visually similar images using precomputed deep-learning descriptors and provides precision/recall metrics for each query.

## 🚀 Features

- 🔍 Search by image ID using multiple deep learning models (MobileNet, ResNet50, ViT and VGG16)
- 📊 Visualize retrieval results along with precision/recall plots
- 🧠 Choose between several similarity functions: Euclidean, Chi‑square and Bhattacharyya
- 📁 Search history stored with user accounts
- 👤 Simple authentication using Flask sessions

## 📷 Example Use Case

1. Log in or register an account.
2. Enter an image number from the dataset, choose the models and similarity metric.
3. The application displays the top matches and evaluation metrics.

## 🛠️ Tech Stack

- **Backend:** Flask, SQLAlchemy, PostgreSQL
- **Frontend:** HTML, CSS (custom + Tailwind), JavaScript
- **Image Processing:** NumPy, OpenCV, PIL, PyTorch
- **Visualization:** Matplotlib

## 📸 Screenshots

### Sign In
![Sign In Screenshot](screenshots/signin.png)

### Main Page
![Main Page Screenshot](screenshots/main_page_1.png)

![Main Page Screenshot](screenshots/main_page_2.png)

### Results Page
![Results Screenshot](screenshots/results_1.png)

### Results Page
![Results Screenshot](screenshots/results_2.png)

## Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL database
- Optional: Docker and Docker Compose

### Installation

1. Clone the repository and enter the project directory.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a PostgreSQL database and note the connection URI (e.g. `postgresql://user:pass@localhost/dbname`).
4. Export the required environment variables:
   ```bash
   export SECRET_KEY=<random-secret>
   export DATABASE_URI=<your-postgres-uri>
   ```
5. Run the application:
   ```bash
   python app.py
   ```
   Visit `http://localhost:8000` in your browser.

### Docker Compose

1. Provide a `.env` file with database credentials (`DB_USER`, `DB_PASSWORD`, `DB_NAME` and `DATABASE_URI`).
2. Build and start the containers:
   ```bash
   docker-compose up --build
   ```
3. The Flask app will be available on port `8000` (or through Nginx on port `80`).

### Directory Structure

- `image.orig/` – original image dataset used for queries
- `static/features/` – precomputed descriptors for each model
- `search_core/` – search engine logic and metric utilities
- `templates/` – HTML templates for the Flask app
- `static/css/` – styling for the user interface
