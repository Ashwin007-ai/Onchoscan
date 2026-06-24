import sys
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


MODEL_PATH = "models/skin_model.pth"
CLASS_NAMES = ["benign", "malignant"]

predict_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])


def load_model(device):
    model = models.resnet18(weights=None)
    model.fc = nn.Linear(model.fc.in_features, 2)
    model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
    model.to(device).eval()
    print("Skin model loaded successfully")
    return model


def predict_skin(image_path, model, device):
    image = Image.open(image_path).convert("RGB").resize((224, 224))
    image_np = np.array(image) / 255.0
    input_tensor = predict_transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = model(input_tensor)

    probs = torch.softmax(outputs, dim=1)
    predicted_class = torch.argmax(outputs, dim=1).item()
    confidence = probs[0][predicted_class].item()
    prediction = CLASS_NAMES[predicted_class]

    print(f"Prediction: {prediction}")
    print(f"Confidence: {round(confidence * 100, 2)}%")

    if prediction == "benign":
        plt.figure(figsize=(5, 4))
        plt.imshow(image)
        plt.title(f"Prediction: benign | Confidence: {round(confidence*100,2)}%")
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
    if len(sys.argv) < 2:
        print("Usage: python skin_prediction.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Using device:", device)

    model = load_model(device)
    predict_skin(image_path, model, device)