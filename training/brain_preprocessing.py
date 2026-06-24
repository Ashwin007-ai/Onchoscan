import torch
import numpy as np
import matplotlib.pyplot as plt
import torchvision.models as models
import torch.nn as nn
import torch.optim as optim

from torchvision import datasets, transforms
from torch.utils.data import DataLoader, WeightedRandomSampler


TRAIN_PATH = "data/brain/Training"
TEST_PATH = "data/brain/Testing"
MODEL_SAVE_PATH = "models/brain_model.pth"


train_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(15),
    transforms.RandomResizedCrop(224, scale=(0.8, 1.0)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

test_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])


def load_data():
    train_dataset = datasets.ImageFolder(root=TRAIN_PATH, transform=train_transform)
    test_dataset = datasets.ImageFolder(root=TEST_PATH, transform=test_transform)

    targets = train_dataset.targets
    class_count = np.bincount(targets)
    class_weights = 1.0 / class_count
    sample_weights = torch.from_numpy(class_weights[targets]).float()
    sampler = WeightedRandomSampler(sample_weights, len(sample_weights))

    train_loader = DataLoader(train_dataset, batch_size=32, sampler=sampler, num_workers=2, pin_memory=True)
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False, num_workers=2, pin_memory=True)

    print("Classes:", train_dataset.classes)
    print("Training images:", len(train_dataset))
    print("Testing images:", len(test_dataset))

    return train_loader, test_loader, train_dataset


def build_model(device):
    model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
    model.fc = nn.Linear(model.fc.in_features, 4)
    return model.to(device)


def train_model(model, train_loader, device, epochs=5):
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    model.train()
    for epoch in range(epochs):
        running_loss = 0
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()
            loss = criterion(model(images), labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
        print(f"Epoch {epoch+1}, Loss: {running_loss/len(train_loader):.4f}")


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


def visualize_samples(train_loader, train_dataset):
    images, labels = next(iter(train_loader))
    plt.figure(figsize=(10, 5))
    for i in range(6):
        plt.subplot(2, 3, i + 1)
        img = images[i].permute(1, 2, 0).numpy()
        img = img * np.array([0.229, 0.224, 0.225]) + np.array([0.485, 0.456, 0.406])
        plt.imshow(img.clip(0, 1))
        plt.title(train_dataset.classes[labels[i]])
        plt.axis("off")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Using device:", device)

    train_loader, test_loader, train_dataset = load_data()
    visualize_samples(train_loader, train_dataset)

    model = build_model(device)
    train_model(model, train_loader, device, epochs=5)
    evaluate_model(model, test_loader, device)

    import os
    os.makedirs("models", exist_ok=True)
    torch.save(model.state_dict(), MODEL_SAVE_PATH)
    print("Model saved to", MODEL_SAVE_PATH)