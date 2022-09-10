import glob
import os
import time
from datetime import datetime

import click
import numpy as np
import pyautogui
from PIL import Image

from detect_edge import detect_edge
from utils import get_logger

logger = get_logger(__name__)


class AutoGUI:
    def __init__(self):
        pass

    def get_window_size(self):
        screen_width, screen_height = pyautogui.size()
        logger.info(f"screen size: {screen_width}, {screen_height}")
        return screen_width, screen_height

    def take_screenshot(self, file_dir: str, file_name: str):
        screen_shot = pyautogui.screenshot()
        screen_shot.save(os.path.join(file_dir, file_name))

    def press_key(self, key):
        pyautogui.press(key)

    def focus(self):
        screen_width, screen_height = self.get_window_size()
        pyautogui.moveTo(screen_width // 2, screen_height // 2)
        pyautogui.click()


def check_same_image(dir_path: str, img_name: str, prev_name: str) -> bool:
    img = np.array(Image.open(os.path.join(dir_path, img_name)))
    prev_img = np.array(Image.open(os.path.join(dir_path, prev_name)))
    return (img == prev_img).all()


def create_pdf(image_dir: str, pdf_dir: str, pdf_name: str, left: int, right: int, height: int):
    files = glob.glob(os.path.join(image_dir, "*.jpg"))
    logger.info(f"detected {len(files)} pages")
    pdf_path = os.path.join(pdf_dir, pdf_name)
    images = []
    for f in files:
        img = Image.open(f)
        img = img.convert("RGB")
        img = img.crop((left, 0, right, height))
        images.append(img)
    images[0].save(pdf_path, save_all=True, append_images=images[1:])
    logger.info(f"saved_pdf to {pdf_path}")


@click.command()
@click.option("--book_name", "-n", default=datetime.strftime(datetime.now(), "%Y%m%d_%H%M%S"), help="Name of Book")
@click.option("--direction", "-d", default="left", help="Direction to read book")
def main(book_name: str, direction: str):
    dir_name = f"./images/{book_name}"
    os.makedirs(dir_name, exist_ok=True)
    for i in range(3, 0, -1):
        time.sleep(1)
        logger.info(f"starts in {i} seconds...")

    ag = AutoGUI()
    ag.focus()
    time.sleep(0.5)
    # full screen mode
    ag.press_key("f11")
    time.sleep(2)
    opposite_direction = "right" if direction == "left" else "left"
    logger.info("returning to first page...")
    for _ in range(50):
        ag.press_key(opposite_direction)
        time.sleep(0.1)

    for i in range(3600):
        img_name = f"{i:0>4}.jpg"
        prev_name = f"{i-1:0>4}.jpg"
        ag.take_screenshot(dir_name, img_name)
        ag.press_key(direction)
        time.sleep(0.3)
        if i == 0:
            continue
        if check_same_image(dir_name, img_name, prev_name):
            logger.info(f"exit as {img_name} and {prev_name} are same")
            ag.press_key("esc")
            break

    logger.info("detect edge")
    left, right, height = detect_edge(os.path.join(dir_name, img_name))

    logger.info("create pdf file")
    create_pdf(dir_name, "./pdf/", f"{book_name}.pdf", left, right, height)


if __name__ == "__main__":
    main()
