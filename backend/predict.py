from PIL import Image
import torch
from torchvision import transforms
from model_loader import (
    brain_model, skin_model,
    brain_classes, skin_classes,
    brain_cam, skin_cam, device
)
import numpy as np
import cv2
import os
import uuid
from pytorch_grad_cam.utils.image import show_cam_on_image
from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget

from recommendation_engine import generate_recommendation   # ← NEW

# ─── TRANSFORM ─────────────────────────────────────────────────────────────────
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# ─── PREDICTORS ────────────────────────────────────────────────────────────────
def predict_brain(image):
    t     = transform(image).unsqueeze(0).to(device)
    out   = brain_model(t)
    probs = torch.softmax(out, dim=1)
    idx   = torch.argmax(out, 1).item()
    return brain_classes[idx], probs[0][idx].item(), probs[0].tolist()

def predict_skin(image):
    t     = transform(image).unsqueeze(0).to(device)
    out   = skin_model(t)
    probs = torch.softmax(out, dim=1)
    idx   = torch.argmax(out, 1).item()
    return skin_classes[idx], probs[0][idx].item(), probs[0].tolist()

# ─── RISK HELPERS ──────────────────────────────────────────────────────────────
SAFE_PREDICTIONS = {"notumor", "benign"}

def get_risk_score(prediction, confidence):
    if prediction in SAFE_PREDICTIONS:
        return max(1, int((1 - confidence) * 100))
    else:
        return int(confidence * 100)

def get_risk_level(score):
    if score >= 70:
        return "High Risk"
    elif score >= 35:
        return "Medium Risk"
    return "Low Risk"

def generate_diagnostic_text(prediction, confidence):
    pct = round(confidence * 100, 2)
    if prediction in SAFE_PREDICTIONS:
        return (
            f"No malignant pattern detected. Model confidence: {pct}%. "
            f"Routine monitoring is still recommended."
        )
    return (
        f"Potential cancer-like pattern detected consistent with "
        f"<strong>{prediction}</strong> (confidence {pct}%). "
        f"Immediate clinical verification is strongly recommended."
    )

# ─── HEATMAP ───────────────────────────────────────────────────────────────────
def generate_heatmap(image, model_type, predicted_class):
    image_resized = image.resize((224, 224))
    image_np      = np.array(image_resized) / 255.0
    input_tensor  = transform(image_resized).unsqueeze(0).to(device)
    targets       = [ClassifierOutputTarget(predicted_class)]

    cam = brain_cam if model_type == "brain" else skin_cam
    grayscale_cam = cam(
        input_tensor=input_tensor,
        targets=targets,
        aug_smooth=True,
        eigen_smooth=True,
    )[0]

    visualization = show_cam_on_image(
        image_np, grayscale_cam, use_rgb=True, image_weight=0.4
    )

    os.makedirs("outputs", exist_ok=True)
    uid           = uuid.uuid4().hex
    heatmap_path  = f"outputs/heatmap_{uid}.png"
    original_path = f"outputs/original_{uid}.png"

    cv2.imwrite(heatmap_path, cv2.cvtColor(visualization, cv2.COLOR_RGB2BGR))
    image_resized.save(original_path)

    return heatmap_path, original_path


def _describe_image_profile(image):
    image_resized = image.resize((224, 224)).convert("RGB")
    image_np = np.array(image_resized).astype(np.float32) / 255.0
    gray = cv2.cvtColor((image_np * 255).astype(np.uint8), cv2.COLOR_RGB2GRAY).astype(np.float32) / 255.0

    brightness = float(gray.mean())
    contrast = float(gray.std())
    channel_means = image_np.mean(axis=(0, 1))
    warmness = float(channel_means[0] - channel_means[2])

    brightness_label = (
        "dark" if brightness < 0.32 else
        "balanced" if brightness < 0.68 else
        "bright"
    )
    contrast_label = (
        "soft-contrast" if contrast < 0.16 else
        "moderate-contrast" if contrast < 0.28 else
        "high-contrast"
    )

    if warmness > 0.05:
        color_label = "warm-toned"
    elif warmness < -0.05:
        color_label = "cool-toned"
    else:
        color_label = "neutral-toned"

    return {
        "brightness": round(brightness * 100, 1),
        "contrast": round(contrast * 100, 1),
        "brightness_label": brightness_label,
        "contrast_label": contrast_label,
        "color_label": color_label,
    }


def _describe_attention_profile(image, model_type, predicted_class):
    image_resized = image.resize((224, 224))
    input_tensor = transform(image_resized).unsqueeze(0).to(device)
    targets = [ClassifierOutputTarget(predicted_class)]
    cam = brain_cam if model_type == "brain" else skin_cam

    grayscale_cam = cam(
        input_tensor=input_tensor,
        targets=targets,
        aug_smooth=True,
        eigen_smooth=True,
    )[0]

    strong_mask = grayscale_cam >= 0.6
    strong_ratio = float(strong_mask.mean())

    if strong_ratio < 0.10:
        focus_label = "focal"
    elif strong_ratio < 0.24:
        focus_label = "regional"
    else:
        focus_label = "diffuse"

    yy, xx = np.indices(grayscale_cam.shape)
    weight = grayscale_cam + 1e-6
    cx = float((xx * weight).sum() / weight.sum()) / grayscale_cam.shape[1]
    cy = float((yy * weight).sum() / weight.sum()) / grayscale_cam.shape[0]

    horizontal = "left-sided" if cx < 0.4 else "right-sided" if cx > 0.6 else "central"
    vertical = "upper" if cy < 0.4 else "lower" if cy > 0.6 else "mid-zone"

    return {
        "focus_label": focus_label,
        "focus_percent": round(strong_ratio * 100, 1),
        "attention_zone": f"{vertical} {horizontal}".strip(),
    }

# ─── MAIN ROUTER ───────────────────────────────────────────────────────────────
def predict_cancer(image, cancer_type):
    if cancer_type == "brain":
        pred, conf, all_probs = predict_brain(image)
        predicted_class       = brain_classes.index(pred)
        all_classes           = brain_classes
    elif cancer_type == "skin":
        pred, conf, all_probs = predict_skin(image)
        predicted_class       = skin_classes.index(pred)
        all_classes           = skin_classes
    else:
        return {"error": "Invalid cancer type"}

    risk_score = get_risk_score(pred, conf)
    risk_level = get_risk_level(risk_score)
    diagnostic = generate_diagnostic_text(pred, conf)

    # ── Class probabilities dict (percentage values) ───────────────────────
    class_probabilities = {
        cls: round(p * 100, 2)
        for cls, p in zip(all_classes, all_probs)
    }
    image_profile = _describe_image_profile(image)
    attention_profile = _describe_attention_profile(image, cancer_type, predicted_class)

    # ── Generate Grad-CAM heatmap ──────────────────────────────────────────
    heatmap_path, original_path = generate_heatmap(image, cancer_type, predicted_class)

    # ── Dynamic AI recommendation via Groq + LLaMA 3 ──────────────────────
    # LLaMA reads the full probability distribution and generates a unique
    # clinical paragraph for every scan based on actual image patterns.
    # Falls back safely to a static message if Groq is unavailable.
    recommendation = generate_recommendation(
        cancer_type    = cancer_type,
        prediction     = pred,
        confidence     = round(conf * 100, 2),  # percentage e.g. 87.3
        risk_level     = risk_level,
        risk_score     = risk_score,
        probabilities  = class_probabilities,   # full dict e.g. {"glioma": 87.3, ...}
        gradcam_region = "",                    # extend later if region detection added
        image_profile  = image_profile,
        attention_profile = attention_profile,
    )

    return {
        "cancer_type":         cancer_type,
        "prediction":          pred,
        "confidence":          round(conf * 100, 2),
        "risk_score":          risk_score,
        "risk_level":          risk_level,
        "diagnostic_text":     diagnostic,
        "recommendation":      recommendation,   # ← single AI paragraph (replaces suggestions list)
        "class_probabilities": class_probabilities,
        "heatmap":             heatmap_path,
        "original":            original_path,
    }
