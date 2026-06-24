import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt
import torchvision.models as models

from torchvision import transforms
from PIL import Image
from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.image import show_cam_on_image
from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget


MODEL_PATH = "models/brain_model.pth"
CLASS_NAMES = ["glioma", "meningioma", "notumor", "pituitary"]

predict_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])


def load_model(device):
    model = models.resnet18(weights=None)
    model.fc = nn.Linear(model.fc.in_features, 4)
    model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
    model.to(device).eval()
    print("Brain model loaded successfully")
    return model


def get_risk_score(confidence):
    return int(confidence * 100)


def get_risk_level(score):
    if score > 80:
        return "High Risk"
    elif score > 50:
        return "Medium Risk"
    return "Low Risk"


def get_confidence_label(confidence):
    if confidence > 0.85:
        return "Very High"
    elif confidence > 0.6:
        return "High"
    elif confidence > 0.4:
        return "Moderate"
    return "Low"


def generate_diagnostic_text(prediction, confidence):
    confidence_percent = round(confidence * 100, 2)
    if prediction == "notumor":
        return f"No abnormal tumor detected. Model confidence {confidence_percent}%. No visible pathological region identified."
    return f"Tumor-like pattern detected consistent with {prediction}. Model confidence {confidence_percent}%. Clinical verification recommended."


def predict_with_report(image_path, model, device):
    image = Image.open(image_path).convert("RGB").resize((224, 224))
    input_tensor = predict_transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = model(input_tensor)

    probs = torch.softmax(outputs, dim=1)
    predicted_class = torch.argmax(outputs, dim=1).item()
    confidence = probs[0][predicted_class].item()
    prediction = CLASS_NAMES[predicted_class]

    return {
        "prediction": prediction,
        "confidence": confidence,
        "risk_score": get_risk_score(confidence),
        "risk_level": get_risk_level(get_risk_score(confidence)),
        "confidence_indicator": get_confidence_label(confidence),
        "diagnostic_text": generate_diagnostic_text(prediction, confidence)
    }


def generate_gradcam(image_path, model, device):
    image = Image.open(image_path).convert("RGB").resize((224, 224))
    image_np = np.array(image) / 255.0
    input_tensor = predict_transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = model(input_tensor)

    predicted_class = torch.argmax(outputs, dim=1).item()
    prediction = CLASS_NAMES[predicted_class]

    if prediction == "notumor":
        plt.figure(figsize=(5, 4))
        plt.imshow(image)
        plt.title("Prediction → notumor (No Grad-CAM)")
        plt.axis("off")
        plt.show()
        return

    cam = GradCAM(model=model, target_layers=[model.layer4[-1]])
    grayscale_cam = cam(
        input_tensor=input_tensor,
        targets=[ClassifierOutputTarget(predicted_class)],
        aug_smooth=True,
        eigen_smooth=True
    )[0]

    visualization = show_cam_on_image(image_np, grayscale_cam, use_rgb=True, image_weight=0.4)

    plt.figure(figsize=(10, 4))
    plt.subplot(1, 2, 1)
    plt.imshow(image)
    plt.title("Original")
    plt.axis("off")
    plt.subplot(1, 2, 2)
    plt.imshow(visualization)
    plt.title(f"GradCAM → {prediction}")
    plt.axis("off")
    plt.show()


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python brain_prediction.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Using device:", device)

    model = load_model(device)

    report = predict_with_report(image_path, model, device)
    print("\n--- Prediction Report ---")
    for key, value in report.items():
        print(f"{key}: {value}")

    print("\n--- Grad-CAM Visualization ---")
    generate_gradcam(image_path, model, device)