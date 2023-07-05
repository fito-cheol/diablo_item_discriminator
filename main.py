from module.image_helper import ImageManager
from module.coordinate import Coordinate, Rectangle
from module.detect_text import detect_text, save_text
from module.item_parser import Item
from module.capture import CaptureManager
import time
FULL_SCREEN = "image/FullScreen.png"

SCREEN_COMPARE = "image/screen_compare.png"
SCREEN_LEGENDARY = "image/screen_legendary.png"
SCREEN_RARE = "image/screen_rare.png"
SCREEN_UNIQUE = "image/screen_unique.png"


UP_LEFT = ImageManager("ref_image/up_left.png")
DOWN_LEFT = ImageManager("ref_image/down_left.png")
UP_RIGHT = ImageManager("ref_image/up_right.png")
DOWN_RIGHT = ImageManager("ref_image/down_right.png")

def main_process():
    game_process_name = "Diablo IV.exe"
    screenshot_path = "screenshots/"
    capture_key = "end"
    caputure_manager = CaptureManager(game_process_name, screenshot_path, capture_key)
    
    while True:
        print('입력대기')
        capture_happend = caputure_manager.ready_key()
        
        if capture_happend:
            start_time = time.time()
            image = caputure_manager.get_capture()
            
            file_path = caputure_manager.get_file_path()
            print("캡쳐 끝: %s 초" % (time.time() - start_time))
            
            handle_image(file_path)
            
        time.sleep(0.05)

def mark_top_bottom(image_path, debug = False):
    origin_image_manager = ImageManager(image_path=image_path)
    image_up = ImageManager(image_path='ref_image\legend_boundary_up.png')
    image_down = ImageManager(image_path='ref_image\legend_boundary_down.png')
    image_manager, top_left, template_height, template_width = origin_image_manager.image_finder(image_up)
    coordinate1 = Coordinate(top_left[0], top_left[1])
    coordinate2 = Coordinate(top_left[0] + template_width, top_left[1])

    image_manager, top_left, template_height, template_width = image_manager.image_finder(image_down)
    coordinate3 = Coordinate(top_left[0], top_left[1] + template_height)
    coordinate4 = Coordinate(top_left[0] + template_width, top_left[1] + template_height)
    rectangle = Rectangle(coordinate1, coordinate2, coordinate3, coordinate4)
    
    if not check_in_shape([rectangle.get_height(), rectangle.get_width()]):
        print(rectangle.get_height(), rectangle.get_width())
        return None
    
    item_box = origin_image_manager.crop_imge(rectangle)
    
    if debug:
        image_manager.show_image()    
        image_manager.draw_rect(rectangle).show_image()
        item_box.show_image()
    return item_box

def check_in_shape(shape):
    
    min_height = 330
    max_height = 900
    
    width = 524
    min_width = 0.9 * width
    max_width = 1.1 * width
    
    is_height_in_range = min_height <= shape[0] <= max_height
    is_width_in_range = min_width <= shape[1] <= max_width
    
    return is_height_in_range and is_width_in_range
    
def handle_image(file_path) -> None:
    start_time = time.time()
    item_box = mark_top_bottom(file_path, debug = False)
    
    if not item_box:
        print('Item Box Not Found')
        return 
    
    print("아이템 박스 잘라내기: %s 초" % (time.time() - start_time))
    save_path = 'item_only.png'
    item_box.save_image(save_path)
    print("이미지 저장: %s 초" % (time.time() - start_time))
    texts = detect_text(save_path)
    print("API 호출: %s 초" % (time.time() - start_time))
    
    save_path = 'item_texts.txt'
    save_text(texts, save_path)
    
    with open(save_path, 'r', encoding='utf-8') as f:
        text_parsed = f.readlines()
        item_instance = Item(text_parsed)
        
        print(item_instance)
    print("글자 파싱: %s 초" % (time.time() - start_time))


if __name__ == '__main__':
    main_process()
    
    # 597 옵션 3줄
    # 보석 박힌거 screen_unique
    # 일반아이템 

    
    
    
    
    
    
    
    




    




    



