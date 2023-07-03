import os
import time
import psutil
import keyboard
from PIL import ImageGrab

class CaptureManager:
    game_process_name = "Diablo IV.exe"
    screenshot_path = "screenshots/"
    capture_key = "F1"
    capture_in_progress = False
    
    def __init__(self, game_process_name, screenshot_path, capture_key) -> None:
        self.game_process_name = game_process_name
        self.screenshot_path = screenshot_path
        self.capture_key = capture_key
        
        if not os.path.exists(screenshot_path):
            os.makedirs(screenshot_path)
        
        keyboard.add_hotkey(capture_key, self.capture_screen)
        
    def capture_screen(self):
        if self.capture_in_progress:
            return

        self.capture_in_progress = True

        # Capture the screen image
        screenshot = ImageGrab.grab()
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"{self.screenshot_path}screenshot_{timestamp}.png"
        screenshot.save(filename)
        print(f"Screenshot saved: {filename}")

        self.capture_in_progress = False
    
    def ready(self):
        if self.is_game_running():
          # Check for keyboard events
          keyboard.wait()
    
    def is_game_running(self):
        for proc in psutil.process_iter():
            if proc.name() == self.game_process_name:
                return True
        return False


if __name__ == '__main__':
    
    game_process_name = "Diablo IV.exe"
    screenshot_path = "screenshots/"
    capture_key = "F1"
    caputure_manager = CaptureManager(game_process_name, screenshot_path, capture_key)
    
    while True:
        caputure_manager.ready()
        time.sleep(0.1)
