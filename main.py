from module.image_helper import ImageManager
from module.coordinate import Coordinate, Rectangle
from module.detect_text import detect_text, save_text
FULL_SCREEN = "image/FullScreen.png"

SCREEN_COMPARE = "image/screen_compare.png"
SCREEN_LEGENDARY = "image/screen_legendary.png"
SCREEN_RARE = "image/screen_rare.png"
SCREEN_UNIQUE = "image/screen_unique.png"


UP_LEFT = ImageManager("ref_image/up_left.png")
DOWN_LEFT = ImageManager("ref_image/down_left.png")
UP_RIGHT = ImageManager("ref_image/up_right.png")
DOWN_RIGHT = ImageManager("ref_image/down_right.png")


def mark_top_bottom(image_path):
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
    # TODO: 1. 두 위치의 x값이 유사한지 확인
    # TODO: 2. y값도 일정범위내인지 확인
    # TODO: 검증에 통과 못한건 text 확인하지 말것
    image_manager.show_image()
    image_manager.draw_rect(rectangle).show_image()
    item_box = origin_image_manager.crop_imge(rectangle)
    item_box.show_image()
    return item_box



if __name__ == '__main__':
    # mark_4_corner(FULL_SCREEN)
    # mark_top_bottom(FULL_SCREEN)
    # mark_top_bottom(SCREEN_COMPARE)
    # mark_top_bottom(SCREEN_LEGENDARY)
    # mark_top_bottom(SCREEN_RARE)
    
    item_box = mark_top_bottom(SCREEN_UNIQUE)
    save_path = 'item_only.png'
    item_box.save_image(save_path)
    texts = detect_text(save_path)
    print('파싱 결과')
    print(texts)
    save_path = 'item_texts.txt'
    save_text(texts, save_path)
    
    
    
    
    
    
    
    
    




    




    



