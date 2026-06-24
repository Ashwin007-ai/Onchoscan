# OnchoScan

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-green.svg)
![PyTorch](https://img.shields.io/badge/PyTorch-2.2.2-red.svg)

## Intelligent Multi-Cancer Detection and Analysis Platform

**OnchoScan** is an AI-powered cancer detection and analysis platform designed to assist healthcare professionals with early diagnosis of Brain and Skin cancers. The system integrates Deep Learning, Explainable AI (Grad-CAM), PDF report generation, patient management, analytics, and AI-generated clinical recommendations.

The platform combines FastAPI, PyTorch, Groq LLM integration, and modern frontend technologies to provide an end-to-end diagnostic workflow.

---

# Features

## Core Features

### Multi-Cancer Detection

* Brain Tumor Classification
* Skin Cancer Classification
* Deep Learning-based prediction pipeline
* Confidence score generation

### Explainable AI

* Grad-CAM heatmap generation
* Visual explanation of model predictions
* Region-of-interest highlighting
* Improved prediction transparency

### Patient Management

* Patient registration
* Patient history tracking
* Profile management
* Prediction record storage

### Analytics Dashboard

* Prediction analytics
* Patient statistics
* Historical trends
* Interactive visualizations

### Report Generation

* Automated PDF reports
* Risk assessment summary
* Confidence analysis
* Downloadable reports

### Batch Processing

* CSV-based bulk processing
* Multiple patient predictions
* Bulk report generation
* ZIP report downloads

### AI Recommendation Engine

* Groq LLM integration
* Clinical recommendation generation
* Prediction interpretation
* Diagnostic assistance

### Authentication

* JWT-based authentication
* Secure login system
* Password hashing with bcrypt
* Protected routes

---

# Project Architecture

```text
OnchoScan/
│
├── backend/
│   ├── app.py
│   ├── predict.py
│   ├── model_loader.py
│   ├── recommendation_engine.py
│   ├── report_generator.py
│   ├── batch_report_generator.py
│   ├── landing.html
│   ├── requirements.txt
│   ├── runtime.txt
│   ├── .env.example
│   └── .gitignore
│
├── frontend/
│   ├── index.html
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
│   └── profile.js
│
├── models/
│   ├── brain_model.pth
│   └── skin_model.pth
│
├── LICENSE
└── README.md
```

---

# Technology Stack

## Backend

| Technology    | Purpose               |
| ------------- | --------------------- |
| FastAPI       | Backend Framework     |
| Uvicorn       | ASGI Server           |
| Python-Jose   | JWT Authentication    |
| Passlib       | Password Hashing      |
| Bcrypt        | Security              |
| Python-Dotenv | Environment Variables |
| Groq API      | LLM Integration       |
| SQLite        | Database              |

---

## Machine Learning

| Technology  | Purpose               |
| ----------- | --------------------- |
| PyTorch     | Deep Learning         |
| Torchvision | Pretrained Models     |
| ResNet18    | Cancer Classification |
| Grad-CAM    | Explainable AI        |
| NumPy       | Numerical Computing   |
| OpenCV      | Image Processing      |
| Pillow      | Image Handling        |

---

## Frontend

| Technology      | Purpose      |
| --------------- | ------------ |
| HTML5           | Structure    |
| CSS3            | Styling      |
| JavaScript ES6+ | Client Logic |

---

## Report Generation

| Technology | Purpose        |
| ---------- | -------------- |
| ReportLab  | PDF Generation |

---

# System Workflow

## Authentication Flow

```text
User Login
     │
     ▼
Authentication
     │
     ▼
JWT Token Generated
     │
     ▼
Dashboard Access
```

---

## Prediction Workflow

```text
Image Upload
     │
     ▼
Preprocessing
     │
     ▼
Model Inference
     │
     ▼
Prediction Result
     │
     ▼
Grad-CAM Generation
     │
     ▼
Risk Assessment
```

---

## Recommendation Workflow

```text
Prediction Result
      │
      ▼
Patient Information
      │
      ▼
Groq LLM
      │
      ▼
Clinical Recommendation
```

---

## Report Workflow

```text
Prediction
     │
     ▼
Report Generator
     │
     ▼
PDF Creation
     │
     ▼
Download
```

---

# Installation

## Prerequisites

* Python 3.11 Recommended
* Python 3.10–3.12 Supported
* Git
* pip
* Modern Browser

---

## Clone Repository

```bash
git clone https://github.com/Ashwin007-ai/Onchoscan.git
cd Onchoscan
```

---

## Backend Setup

### Navigate to Backend

```bash
cd backend
```

### Create Virtual Environment

```bash
py -3.11 -m venv venv
```

### Activate Environment

#### Windows CMD

```cmd
venv\Scripts\activate
```

#### Windows PowerShell

```powershell
venv\Scripts\Activate.ps1
```

#### Linux / macOS

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

# Environment Variables

Create a file named:

```text
.env
```

inside the backend directory.

Example:

```env
GROQ_API_KEY=your_groq_api_key_here
```

A template file is already provided:

```text
.env.example
```

Copy the template and replace the placeholder value with your actual API key.

---

# Model Files

Verify that the following model files exist:

```text
models/
├── brain_model.pth
└── skin_model.pth
```

---

# Running the Application

Start the backend server:

```bash
cd backend
uvicorn app:app --reload
```

Server URL:

```text
http://localhost:8000
```

---

# API Documentation

Swagger UI:

```text
http://localhost:8000/docs
```

ReDoc:

```text
http://localhost:8000/redoc
```

---

# Main Pages

| Page      | Description           |
| --------- | --------------------- |
| Home      | Application Overview  |
| Dashboard | Prediction Interface  |
| Analytics | Prediction Analytics  |
| Batch     | Bulk Processing       |
| Compare   | Prediction Comparison |
| History   | Historical Records    |
| Profile   | User Profile          |
| About     | Project Information   |

---

# Running a Prediction

1. Open Dashboard.
2. Upload Brain MRI or Skin Lesion image.
3. Select Cancer Type.
4. Click Analyze.
5. Review:

   * Prediction
   * Confidence Score
   * Risk Assessment
   * Grad-CAM Heatmap
6. Download PDF Report.

---

# Batch Processing

1. Open Batch Processing page.
2. Upload CSV file.
3. Start processing.
4. Wait for report generation.
5. Download ZIP package.

---

# Requirements

```txt
fastapi==0.110.0
uvicorn==0.29.0
python-jose[cryptography]==3.3.0
python-multipart==0.0.9
python-dotenv==1.2.2
passlib[bcrypt]==1.7.4
groq
pillow==10.3.0
torch==2.2.2
torchvision==0.17.2
numpy==1.26.4
opencv-python-headless==4.9.0.80
grad-cam==1.5.2
reportlab==4.1.0
bcrypt==4.0.1
```

---

# Troubleshooting

## Missing Model Files

```text
FileNotFoundError
```

Ensure:

```text
models/brain_model.pth
models/skin_model.pth
```

exist.

---

## Missing Groq API Key

Error:

```text
groq.GroqError
```

Solution:

Create:

```text
backend/.env
```

and add:

```env
GROQ_API_KEY=your_groq_api_key_here
```

---

## Dependency Installation Issues

Use Python 3.11:

```bash
py -3.11 -m venv venv
```

---

## PowerShell Activation Error

Error:

```text
running scripts is disabled on this system
```

Run:

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Or use Command Prompt:

```cmd
venv\Scripts\activate.bat
```

---

# Future Enhancements

## Cancer Detection

* Lung Cancer Detection
* Breast Cancer Detection
* Colorectal Cancer Detection
* Multi-Cancer Ensemble Models

## Explainable AI

* SHAP Integration
* LIME Integration
* Interactive Heatmaps

## Infrastructure

* Docker Support
* GitHub Actions CI/CD
* Cloud Deployment
* Automated Testing

## Security

* Two-Factor Authentication
* Role-Based Access Control
* Enhanced Encryption

## User Experience

* Mobile Application
* Notifications
* Telemedicine Integration

---

# Contributing

1. Fork Repository
2. Create Feature Branch

```bash
git checkout -b feature/new-feature
```

3. Commit Changes

```bash
git commit -m "Add new feature"
```

4. Push Changes

```bash
git push origin feature/new-feature
```

5. Open Pull Request

---

# License

This project is licensed under the MIT License.

---

# Contact

**Maintainer:** P Ashwin Kumar

**GitHub:** https://github.com/Ashwin007-ai

**LinkedIn:** https://www.linkedin.com/in/ashwinkumarpaswan/

**Project:** OnchoScan

---

# References

* FastAPI Documentation
* PyTorch Documentation
* Grad-CAM Research Paper
* Groq API Documentation

---

**Version:** 1.0.0

**Status:** Active Development

**Last Updated:** June 2026
