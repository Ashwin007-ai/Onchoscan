[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-green)](https://fastapi.tiangolo.com/)

# Onchoscan

**Onchoscan** is an intelligent multi-cancer detection and analysis platform that leverages deep learning models to assist healthcare professionals in early cancer diagnosis. The system provides real-time predictions, comprehensive patient analytics, and detailed medical reports for brain and skin cancers.

**Project Type:** Medical AI/ML Application
**Current Version:** 1.0.0
**Last Updated:** May 2026

---

## Table of Contents

- [Features](#features)
- [Project Architecture](#project-architecture)
- [Tools and Technologies](#tools-and-technologies)
- [System Workflow](#system-workflow)
- [Installation](#installation)
- [Usage](#usage)
- [Future Enhancements](#future-enhancements)
- [License](#license)
- [Contributing](#contributing)
- [Contact](#contact)

---

## Features

### Core Features
- **Multi-Cancer Detection** — Support for Brain and Skin cancer types
- **AI-Powered Analysis** — Deep learning models with Grad-CAM heatmap explainability
- **Patient Dashboard** — Comprehensive patient information management
- **Real-time Analytics** — Interactive analytics and visualization
- **Batch Processing** — Process multiple patient records via CSV upload
- **Report Generation** — Automated PDF medical report creation
- **Patient History** — Track and compare historical patient data
- **Recommendation Engine** — AI-driven clinical recommendations via Groq (Llama 3)
- **Authentication System** — Secure login with JWT-based session management

### Advanced Features
- Comparative analysis between patient records
- Grad-CAM heatmap visualization for model explainability
- Patient profile management
- Export functionality for reports

---

## Project Architecture

```
onchoscan/
├── backend/
│   ├── app.py                      # FastAPI application entry point
│   ├── model_loader.py             # Loads brain and skin models
│   ├── predict.py                  # Inference engine
│   ├── report_generator.py         # Single patient PDF report
│   ├── batch_report_generator.py   # Bulk report generation
│   ├── recommendation_engine.py    # Groq LLM recommendations
│   ├── landing.html                # Landing page served by FastAPI
│   ├── onchoscan.db                # SQLite database
│   ├── requirements.txt
│   ├── runtime.txt
│   ├── outputs/                    # Prediction output files
│   ├── reports/                    # Generated PDF reports
│   └── .gitignore
│
├── frontend/
│   ├── index.html                  # Entry point
│   ├── home.html
│   ├── dashboard.html
│   ├── analytics.html
│   ├── batch.html
│   ├── compare.html
│   ├── history.html
│   ├── about.html
│   ├── profile.html
│   ├── style.css
│   ├── patient_notes.css
│   ├── profile.css
│   ├── app.js
│   ├── auth.js
│   ├── script.js
│   ├── features.js
│   ├── patient_notes.js
│   ├── profile.js
│   └── patients/
│
├── models/
│   ├── brain_model.pth
│   └── skin_model.pth
│
├── LICENSE
└── README.md
```

### Component Description

| Component | Purpose | Technology |
|-----------|---------|------------|
| **Frontend** | User interface and interaction | HTML5, CSS3, JavaScript (ES6+) |
| **Backend API** | Core business logic and inference | FastAPI 0.110.0, Python |
| **ML Models** | Cancer detection predictions | PyTorch, ResNet18 |
| **Report Generator** | Automated PDF report creation | ReportLab |
| **Database** | Patient and prediction data storage | SQLite |
| **LLM Integration** | AI-driven recommendations | Groq API (Llama 3) |
| **Explainability** | Visual heatmap generation | Grad-CAM |

---

## Tools and Technologies

### Backend
- **Framework**: FastAPI 0.110.0
- **Language**: Python 3.8+
- **Server**: Uvicorn 0.29.0 (ASGI)
- **Authentication**: OAuth2 with JWT (python-jose 3.3.0)
- **Password Hashing**: bcrypt 4.0.1
- **File Uploads**: python-multipart 0.0.9
- **Database**: SQLite
- **LLM Integration**: Groq API (Llama 3)
- **API Documentation**: OpenAPI/Swagger (built-in with FastAPI)

### ML / Data Science
- **ML Framework**: PyTorch 2.2.2
- **Vision Library**: Torchvision 0.17.2
- **Model Architecture**: ResNet18 (transfer learning from ImageNet)
- **Model Format**: `.pth` (PyTorch serialized)
- **Image Processing**: Pillow 10.3.0, OpenCV 4.9.0 (headless)
- **Numerical Computing**: NumPy 1.26.4
- **Explainability**: Grad-CAM 1.5.2

### Frontend
- **HTML5**: Semantic markup and structure
- **CSS3**: Responsive styling and animations
- **JavaScript (ES6+)**: Dynamic interactions and AJAX calls to backend API

### Report Generation
- **ReportLab 4.1.0**: PDF generation for medical reports

---

## System Workflow

### 1. User Authentication
```
User Access → Login (auth.js) → JWT Token Issued → Dashboard Access
```

### 2. Cancer Detection
```
Image Upload → Preprocessing → model_loader.py → predict.py → Confidence Score + Grad-CAM
```

### 3. Report Generation
```
Prediction Results → report_generator.py → PDF Report → Download
```

### 4. Recommendation Engine
```
Patient Data + Prediction → recommendation_engine.py → Groq API (Llama 3) → Clinical Recommendations
```

### 5. Batch Processing
```
CSV Upload → batch_report_generator.py → Parallel Inference → Bulk PDF Reports → ZIP Download
```

### 6. Analytics Dashboard
```
SQLite Database → Data Aggregation → analytics.html → Real-time Visualization
```

---

## Installation

### Prerequisites
- Python 3.8 or higher
- pip
- Git
- Modern web browser (Chrome, Firefox, Safari, Edge)

### 1. Clone the Repository

```bash
git clone https://github.com/ashwin007-ai/onchoscan.git
cd onchoscan
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate — Windows
venv\Scripts\activate

# Activate — macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Verify Model Files

Ensure the following files exist in the `models/` directory at the project root:

```
models/
├── brain_model.pth
└── skin_model.pth
```

> If you trained the models yourself using the training scripts, copy the `.pth` files from your output directory into `models/`.

### 4. Start the Backend Server

```bash
cd backend
uvicorn app:app --reload
```

Backend runs at: `http://localhost:8000`

API documentation available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 5. Start the Frontend

```bash
cd frontend

# Option 1: Open index.html directly in your browser

# Option 2: Serve with Python
python -m http.server 8001
# Then open http://localhost:8001
```

---

## Usage

### Main Pages

| Page | URL | Purpose |
|------|-----|---------|
| Home | `/home.html` | Landing overview |
| Predict | `/dashboard.html` | Upload image and run prediction |
| Batch | `/batch.html` | Process multiple images via CSV |
| History | `/history.html` | View all past predictions |
| Compare | `/compare.html` | Side-by-side prediction comparison |
| Analytics | `/analytics.html` | Stats and trends |
| Profile | `/profile.html` | User profile management |
| About | `/about.html` | Project information |

### Running a Prediction

1. Go to the **Dashboard** page
2. Upload a medical image (Brain MRI or Skin lesion image)
3. Select the cancer type (Brain or Skin)
4. Click **Analyze**
5. View results:
   - Prediction label and confidence score (%)
   - Grad-CAM heatmap showing regions of interest
   - Risk level assessment
6. Download the PDF report if needed

### Batch Processing

1. Go to the **Batch** page
2. Upload a CSV file containing image paths and patient info
3. The system processes all images and generates reports
4. Download all reports as a ZIP file

### Compare Predictions

1. Go to the **Compare** page
2. Select two or more past predictions
3. View side-by-side confidence scores and visualizations

---

## Troubleshooting

**Model files not found**
```
Ensure models/brain_model.pth and models/skin_model.pth exist.
```

**Port already in use**
```bash
uvicorn app:app --reload --port 8001
```

**Dependency installation fails**
```bash
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

**CORS errors in browser**
```
CORS is already configured in app.py via FastAPI's CORSMiddleware.
If issues persist, ensure the backend is running before opening the frontend.
```

---

## Future Enhancements

### Cancer Detection
- [ ] Support for additional cancer types (Lung, Breast, Colorectal)
- [ ] Multi-model ensemble predictions
- [ ] 3D medical image analysis

### Infrastructure
- [ ] Containerization with Docker
- [ ] Cloud deployment (AWS / Azure / GCP)
- [ ] CI/CD pipeline with GitHub Actions
- [ ] Automated test suite with pytest
- [ ] Real-time WebSocket updates

### AI/ML
- [ ] LIME/SHAP integration alongside existing Grad-CAM
- [ ] Model versioning and tracking (MLflow)
- [ ] Federated learning support

### Security & Compliance
- [ ] HIPAA compliance implementation
- [ ] End-to-end encryption
- [ ] Two-factor authentication
- [ ] Data anonymization tools

### User Experience
- [ ] Mobile application (iOS/Android)
- [ ] Real-time notifications
- [ ] Telemedicine integration

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add your feature'`
4. Push to branch: `git push origin feature/your-feature`
5. Open a Pull Request

Please follow PEP 8 for Python code and include docstrings for all functions.

---

## Contact

**Project Maintainer**: P Ashwin Kumar
**Email**: ashwinkumarp2004@gmail.com
**GitHub**: [@ashwin007-ai](https://github.com/ashwin007-ai)
**LinkedIn**: [ashwinkumarpaswan](https://www.linkedin.com/in/ashwinkumarpaswan/)

---

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [PyTorch Documentation](https://pytorch.org/docs/)
- [Grad-CAM Paper](https://arxiv.org/abs/1610.02391)
- [Groq API Documentation](https://console.groq.com/docs)

---

*Last Updated: May 2026 | Version: 1.0.0 | Status: Active Development*
