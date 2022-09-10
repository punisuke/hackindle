import os

import pyautogui

from utils import get_logger

logger = get_logger(__name__)


class AutoGUI:
    def __init__(self):
        pass

    def get_window(self):
        screen_width, screen_height = pyautogui.size()
        logger.info(f"screen size: {screen_width}, {screen_height}")

    def take_screenshot(self, file_dir: str, file_name: str):
        screen_shot = pyautogui.screenshot()
        screen_shot.save(os.path.join(file_dir, file_name))


if __name__ == "__main__":
    ag = AutoGUI()
    ag.take_screenshot()
