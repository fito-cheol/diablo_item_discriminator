from module.image_helper import ImageManager

FULL_SCREEN = "image/FullScreen.png"

SCREEN_COMPARE = "image/screen_compare.png"
SCREEN_LEGENDARY = "image/screen_legendary.png"
SCREEN_RARE = "image/screen_rare.png"
SCREEN_UNIQUE = "image/screen_unique.png"

def mark_4_corner(image_path):
    
    path1 = "result/result1.png"
    path2 = "result/result2.png"
    path3 = "result/result3.png"
    path4 = "result/result4.png"

    UP_LEFT = "ref_image/up_left.png"
    DOWN_LEFT = "ref_image/down_left.png"
    UP_RIGHT = "ref_image/up_right.png"
    DOWN_RIGHT = "ref_image/down_right.png"

    image_manager = ImageManager(image_path)
    image_manager, *_ = image_manager.image_finder(UP_LEFT, use_gray=False)
    image_manager.save_image(path1)

    image_manager, *_ = image_manager.image_finder(DOWN_LEFT, use_gray=False)
    image_manager.save_image(path2)

    image_manager, *_ = image_manager.image_finder(UP_RIGHT, use_gray=False)
    image_manager.save_image(path3)

    image_manager, *_ = image_manager.image_finder(DOWN_RIGHT, use_gray=False)
    image_manager.save_image(path4)

if __name__ == '__main__':
    mark_4_corner(FULL_SCREEN)
    # image_with_rect = ItemFinder().mark_item_box(FULL_SCREEN)
    # show_image(image_with_rect)
    #
    # image_with_rect = ItemFinder().mark_item_box(SCREEN_COMPARE)
    # show_image(image_with_rect)
    # image_with_rect = ItemFinder().mark_item_box(SCREEN_LEGENDARY)
    # show_image(image_with_rect)
    # image_with_rect = ItemFinder().mark_item_box(SCREEN_RARE)
    # show_image(image_with_rect)
    # image_with_rect = ItemFinder().mark_item_box(SCREEN_UNIQUE)
    # show_image(image_with_rect)



