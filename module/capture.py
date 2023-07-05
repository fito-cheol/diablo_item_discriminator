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
    image = None
    
    def __init__(self, game_process_name, screenshot_path, capture_key) -> None:
        self.game_process_name = game_process_name
        self.screenshot_path = screenshot_path
        self.capture_key = capture_key
        if not os.path.exists(screenshot_path):
            os.makedirs(screenshot_path)
        
        
    def capture_screen(self):
        if self.capture_in_progress:
            return

        self.capture_in_progress = True

        # Capture the screen image
        self.capture = ImageGrab.grab().resize((2560, 1440))
        print(self.capture.width, self.capture.height)
        
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        self.file_path = f"{self.screenshot_path}screenshot_{timestamp}.png"
        self.capture.save(self.file_path)
        print(f"Screenshot saved: {self.file_path}")

        self.capture_in_progress = False
    
    def get_capture(self):
        return self.capture
    
    def get_file_path(self):
        return self.file_path
    
    def ready(self):
        if self.is_game_running():
          # Check for keyboard events
          keyboard.wait()
    
    def ready_key(self):
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN and event.name == self.capture_key:
            if not self.is_game_running():
                print("게임이 실행중이지 않습니다")
                return False
            
            print('Keyboard Event: 캡쳐 시작')
            self.capture_screen()
            return True
        return False
    
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
