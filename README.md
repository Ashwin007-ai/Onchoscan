"# Onchoscan

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0%2B-green)](https://flask.palletsprojects.com/)

## Project Info

**Onchoscan** is an intelligent multi-cancer detection and analysis platform that leverages deep learning models to assist healthcare professionals in early cancer diagnosis. The system provides real-time predictions, comprehensive patient analytics, and detailed medical reports for multiple cancer types including brain and skin cancers.

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
- [Example Use Case](#example-use-case)
- [Future Enhancements](#future-enhancements)
- [License](#license)
- [Contributing](#contributing)
- [Contact](#contact)

---

## Features

### Core Features
- **Multi-Cancer Detection**: Support for multiple cancer types (Brain, Skin)
- **AI-Powered Analysis**: Deep learning models for accurate predictions
- **Patient Dashboard**: Comprehensive patient information management
- **Real-time Analytics**: Interactive analytics and visualization
- **Batch Processing**: Process multiple patient records simultaneously
- **Report Generation**: Automated medical report creation with predictions
- **Patient History**: Track and compare historical patient data
- **Recommendation Engine**: AI-driven clinical recommendations based on analysis
- **Authentication System**: Secure user login and role-based access
- **Responsive UI**: Mobile-friendly web interface

### Advanced Features
- Comparative analysis between patient records
- Customizable prediction thresholds
- Export functionality for reports
- Real-time model inference
- Patient profile management
- Advanced search and filtering

---

## Project Architecture

### Architecture Overview

```
Onchoscan/
├── Frontend (Web UI)
│   ├── Dashboard & Analytics
│   ├── Patient Management
│   ├── Authentication
│   └── Report Viewer
│
├── Backend (API Server)
│   ├── Flask Application
│   ├── Model Inference Engine
│   ├── Report Generator
│   ├── Recommendation Engine
│   └── Database Layer
│
└── ML Models
    ├── Brain Cancer Model
    ├── Skin Cancer Model
    └── Model Loader
```

### Component Description

| Component | Purpose | Technology |
|-----------|---------|-----------|
| **Frontend** | User interface and interaction | HTML5, CSS3, JavaScript |
| **Backend API** | Core business logic and inference | Flask, Python 3.8+ |
| **ML Models** | Cancer detection predictions | PyTorch, Deep Learning |
| **Report Generator** | Automated medical report creation | Jinja2, HTML Templates |
| **Database** | Patient and prediction data storage | SQLite/PostgreSQL |

---

## Tools and Technologies

### Backend
- **Framework**: Flask 2.0+
- **Language**: Python 3.8+
- **Server**: Uvicorn (ASGI)
- **ML Framework**: PyTorch
- **Data Processing**: NumPy, Pandas
- **API Documentation**: OpenAPI/Swagger (optional)

### Frontend
- **HTML5**: Semantic markup and structure
- **CSS3**: Responsive styling and animations
- **JavaScript (ES6+)**: Dynamic interactions and AJAX
- **Bootstrap/Tailwind**: (If used) CSS framework

### ML/Data Science
- **Model Framework**: PyTorch
- **Model Format**: .pth (PyTorch serialized models)
- **Image Processing**: Pillow, OpenCV
- **Numerical Computing**: NumPy, SciPy

### Deployment
- **Runtime**: Python 3.8+
- **Package Manager**: pip
- **Version Control**: Git

### Development
- **IDE**: VS Code / PyCharm
- **Debugging**: Python debugger, Flask development server
- **Testing**: pytest (recommended)

---

## System Workflow

### 1. User Authentication
```
User Access
    ↓
Login System (auth.js)
    ↓
Session Management
    ↓
Dashboard Access
```

### 2. Patient Data Entry
```
New Patient
    ↓
Form Submission
    ↓
Backend Validation
    ↓
Database Storage
```

### 3. Cancer Detection Workflow
```
Medical Image Upload
    ↓
Image Preprocessing
    ↓
Model Loader (model_loader.py)
    ↓
Inference Engine (predict.py)
    ↓
Prediction Generation
    ↓
Confidence Score Calculation
```

### 4. Report Generation
```
Prediction Results
    ↓
Report Generator (report_generator.py)
    ↓
Template Rendering
    ↓
HTML Report Creation
    ↓
PDF Export (optional)
```

### 5. Recommendation Engine
```
Patient Data + Predictions
    ↓
Recommendation Engine (recommendation_engine.py)
    ↓
Clinical Analysis
    ↓
Recommendation Generation
    ↓
Report Integration
```

### 6. Batch Processing
```
Multiple Patient Records
    ↓
Batch Report Generator (batch_report_generator.py)
    ↓
Parallel Processing
    ↓
Bulk Report Generation
    ↓
Results Storage
```

### 7. Analytics & Dashboard
```
Patient Database
    ↓
Data Aggregation
    ↓
Analytics Calculation
    ↓
Dashboard Visualization (analytics.html)
    ↓
Real-time Updates
```

---

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Backend Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/onchoscan.git
cd onchoscan
```

2. **Navigate to backend directory**
```bash
cd backend
```

3. **Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Verify model files**
Ensure the following model files are in the `models/` directory:
- `brain_model.pth`
- `skin_model.pth`

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd ../frontend
```

2. **No installation required** - Frontend runs on HTML/CSS/JavaScript
   Simply open `index.html` in your browser or serve with a local server

3. **Optional: Start a local server**
```bash
# Python 3
python -m http.server 8000

# Then open http://localhost:8000
```

### Running the Application

1. **Start Backend Server**
```bash
cd backend
python -m uvicorn app:app --reload
```
Server will run on: `http://localhost:8000`

2. **Start Frontend**
```bash
cd frontend

# Option 1: Open in browser
# Double-click index.html or open in browser

# Option 2: Run local server
python -m http.server 8001
# Access at http://localhost:8001
```

3. **Access Application**
- Open `http://localhost:8001` (or your frontend port)
- Login with credentials
- Navigate to Dashboard

---

## Usage

### Patient Management
1. Navigate to **Patients** section
2. Click **Add New Patient**
3. Fill in patient information
4. Upload medical imaging data
5. Submit for analysis

### Running Predictions
1. Go to **Analysis** tab
2. Select patient
3. Choose cancer type (Brain/Skin)
4. System automatically processes image
5. View prediction results

### Generating Reports
1. Complete patient analysis
2. Click **Generate Report**
3. Review report preview
4. Download as PDF (if enabled)
5. Save to patient record

### Batch Processing
1. Navigate to **Batch Operations**
2. Upload CSV file with patient data
3. System processes all records
4. Download bulk report
5. Save results to database

### Viewing Analytics
1. Go to **Analytics** dashboard
2. View prediction statistics
3. Compare patient trends
4. Export analytics data

---

## Example Use Case

### Scenario: Early Brain Cancer Detection

**Patient Details:**
- Name: John Doe
- Age: 45
- Medical ID: P001
- Symptoms: Headaches, vision issues

**Workflow:**

1. **Intake**: Patient data entered into system
2. **Imaging**: MRI scan uploaded
3. **Preprocessing**: Image normalized and prepared
4. **Analysis**: Brain cancer model processes image
5. **Results**:
   - Prediction: Tumor Detected (85% confidence)
   - Tumor Type: Glioblastoma
   - Risk Level: High
6. **Recommendations**:
   - Urgent specialist referral
   - Additional imaging recommended
   - Treatment options provided
7. **Report**: Comprehensive medical report generated and shared with physician

**Output**: Automated report with:
- Prediction results
- Confidence metrics
- Risk assessment
- Clinical recommendations
- Follow-up suggestions

---

## Future Enhancements

### Phase 2 Features
- [ ] Support for additional cancer types (Lung, Breast, Colorectal)
- [ ] 3D medical image analysis
- [ ] Multi-model ensemble predictions
- [ ] Confidence interval calculations

### Technical Improvements
- [ ] Advanced caching mechanisms
- [ ] Real-time WebSocket updates
- [ ] Containerization (Docker/Kubernetes)
- [ ] Cloud deployment (AWS/Azure/GCP)
- [ ] Automated testing suite (pytest)
- [ ] CI/CD pipeline (GitHub Actions)

### AI/ML Enhancements
- [ ] Model fine-tuning capabilities
- [ ] Transfer learning implementations
- [ ] Federated learning support
- [ ] Explainable AI (XAI) integration
- [ ] Model versioning and tracking

### Security & Compliance
- [ ] HIPAA compliance implementation
- [ ] End-to-end encryption
- [ ] Advanced audit logging
- [ ] Two-factor authentication
- [ ] Data anonymization tools

### User Experience
- [ ] Mobile application (iOS/Android)
- [ ] Multi-language support
- [ ] Advanced visualization dashboards
- [ ] Real-time notifications
- [ ] Telemedicine integration

---

## Installation Troubleshooting

### Common Issues

**Issue: Model files not found**
```
Solution: Ensure models/ directory contains:
- brain_model.pth
- skin_model.pth
```

**Issue: Port already in use**
```
Solution: Change port:
python -m uvicorn app:app --reload --port 8001
```

**Issue: Dependencies installation fails**
```
Solution:
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

**Issue: CORS errors**
```
Solution: Update Flask app to include CORS:
from flask_cors import CORS
CORS(app)
```

---

## License

This project is licensed under the **MIT License** - see the LICENSE file for details.

### MIT License Summary
- ✅ Commercial use
- ✅ Modification
- ✅ Distribution
- ✅ Private use
- ⚠️ Liability limited
- ⚠️ Warranty not provided

**Notice**: Include the following in your project:
```
MIT License

Copyright (c) 2026 [Your Name/Organization]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Standards
- Follow PEP 8 for Python code
- Use meaningful variable names
- Add comments for complex logic
- Include docstrings for functions
- Test before submitting PR

---

## Contact

**Project Maintainer**: [Your Name]  
**Email**: [your.email@example.com]  
**GitHub**: [@yourprofile](https://github.com/yourprofile)  
**LinkedIn**: [Your LinkedIn Profile]

### Support
For issues and questions:
- Create an issue on GitHub
- Check existing documentation
- Review FAQ section

---

## Acknowledgments

- Thanks to the open-source community
- PyTorch team for the ML framework
- Flask community for the web framework
- All contributors and testers

---

## References

- [PyTorch Documentation](https://pytorch.org/docs/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Medical Image Analysis](https://en.wikipedia.org/wiki/Medical_image_computing)
- [Deep Learning in Healthcare](https://www.ibm.com/cloud/blog/deep-learning-healthcare)

---

**Last Updated**: May 2026  
**Status**: Active Development  
**Version**: 1.0.0" 
