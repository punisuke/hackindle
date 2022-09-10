import numpy as np
from PIL import Image, ImageOps


def detect_rectangle(image_path: str):
    img = np.array(Image.open(image_path))
    img = ImageOps.grayscale(img)
    print(img.shape)


if __name__ == "__main__":
    detect_rectangle("./images/CleanCoder/0001.jpg")
