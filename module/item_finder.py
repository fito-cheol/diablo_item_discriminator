from .image_helper import ImageManager
from .coordinate import Coordinate, Rectangle
 

class ItemFinder:
    """ Find ItemBox in Screenshot """
    UP_LEFT = "ref_image/up_left.png"
    DOWN_LEFT = "ref_image/down_left.png"
    UP_RIGHT = "ref_image/up_right.png"
    DOWN_RIGHT = "ref_image/down_right.png"

    def __init__(self):
        pass

    def mark_item_box(self, image_path: str):
        """ Return Image With Rectangle Added Where Item Box located"""
        rect_object = self.find_rectangle(image_path)
        image_manager = ImageManager(image_path)
        return image_manager.draw_rect(rect_object)

    def find_rectangle(self, image_path: str):
        """Return Rect Where Item Located """
        image_manager = ImageManager(image_path)

        _, up_left, _, _ = image_manager.image_finder(self.UP_LEFT)
        _, up_right, up_right_width, _ = image_manager.image_finder(self.UP_RIGHT)
        _, down_left, _, down_left_height = image_manager.image_finder(self.DOWN_LEFT)
        _, down_right, down_right_wight, down_right_height = image_manager.image_finder(self.DOWN_RIGHT)

        coordinate1 = Coordinate(up_left[0], up_left[1])
        coordinate2 = Coordinate(up_right[0], up_right[1]).add_x(up_right_width)
        coordinate3 = Coordinate(down_left[0], down_left[1]).add_y(down_left_height)
        coordinate4 = Coordinate(down_right[0], down_right[1]) + [down_right_wight, down_right_height]

        return Rectangle(coordinate1, coordinate2, coordinate3, coordinate4)

