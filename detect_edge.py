import numpy as np
from PIL import Image


def detect_edge(image_path: str):
    img = Image.open(image_path)
    img = np.array(img)
    height, width, _ = img.shape
    center = width / 2
    for i in range(int(center)):
        ave1 = img[:, i, :].mean()
        ave2 = img[:, i + 1, :].mean()
        if ave1 != ave2:
            break
    left = i
    right = center + (center - left)
    return left, right, height


if __name__ == "__main__":
    res = detect_edge("./images/CleanCoder/0001.jpg")
