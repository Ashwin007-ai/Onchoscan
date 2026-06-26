import os
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import pandas as pd
import torchvision.models as models

from PIL import Image
from sklearn.model_selection import train_test_split
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms


DATA_PATH = "data/skin"
METADATA_PATH = os.path.join(DATA_PATH, "HAM10000_metadata.csv")
IMAGE_FOLDER_1 = os.path.join(DATA_PATH, "HAM10000_images_part_1")
IMAGE_FOLDER_2 = os.path.join(DATA_PATH, "HAM10000_images_part_2")
MODEL_SAVE_PATH = "models/skin_model.pth"

MALIGNANT_CLASSES = ["mel", "bcc", "akiec"]

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])


class SkinDataset(Dataset):
    def __init__(self, dataframe, transform=None):
        self.data = dataframe
        self.transform = transform

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        img_path = self.data.iloc[idx]["path"]
        label = self.data.iloc[idx]["label"]
        image = Image.open(img_path).convert("RGB")
        if self.transform:
            image = self.transform(image)
        return image, label


def get_image_path(image_id):
    path1 = os.path.join(IMAGE_FOLDER_1, image_id + ".jpg")
    path2 = os.path.join(IMAGE_FOLDER_2, image_id + ".jpg")
    return path1 if os.path.exists(path1) else path2


def load_data():
    metadata = pd.read_csv(METADATA_PATH)
    metadata["label"] = metadata["dx"].apply(lambda x: 1 if x in MALIGNANT_CLASSES else 0)
    metadata["path"] = metadata["image_id"].apply(get_image_path)

    print("Class distribution:\n", metadata["dx"].value_counts())

    train_df, test_df = train_test_split(
        metadata, test_size=0.2, stratify=metadata["label"], random_state=42
    )

    train_dataset = SkinDataset(train_df, transform)
    test_dataset = SkinDataset(test_df, transform)

    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

    print(f"Training samples: {len(train_dataset)}")
    print(f"Testing samples: {len(test_dataset)}")

    return train_loader, test_loader


def build_model(device):
    model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
    model.fc = nn.Linear(model.fc.in_features, 2)
    return model.to(device)


def train_model(model, train_loader, device, epochs=20):
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    model.train()
    for epoch in range(epochs):
        running_loss, correct, total = 0, 0, 0
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
        print(f"Epoch {epoch+1} | Loss: {running_loss/len(train_loader):.4f} | Accuracy: {100*correct/total:.2f}%")


def evaluate_model(model, test_loader, device):
    model.eval()
    correct, total = 0, 0
    with torch.no_grad():
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)
            _, predicted = torch.max(model(images), 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    print(f"Test Accuracy: {100 * correct / total:.2f}%")


if __name__ == "__main__":
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Using device:", device)

    train_loader, test_loader = load_data()
    model = build_model(device)
    train_model(model, train_loader, device, epochs=10)
    evaluate_model(model, test_loader, device)

    os.makedirs("models", exist_ok=True)
    torch.save(model.state_dict(), MODEL_SAVE_PATH)
    print("Skin model saved to", MODEL_SAVE_PATH)
