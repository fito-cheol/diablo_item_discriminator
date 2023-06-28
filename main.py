from module.image_helper import  save_image, show_image, ImageManager

FULL_SCREEN = "image/FullScreen.png"

SCREEN_COMPARE = "image/screen_compare.png"
SCREEN_LEGENDARY = "image/screen_legendary.png"
SCREEN_RARE = "image/screen_rare.png"
SCREEN_UNIQUE = "image/screen_unique.png"

class Coordinate:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return '({0}, {1})'.format(self.x, self.y)

    def __iter__(self):
        yield self.x
        yield self.y
    def add_height(self, height):
        new_y = self.y + height
        return Coordinate(self.x, new_y)

    def add_width(self, width):
        new_x = self.x + width
        return Coordinate(new_x, self.y)

    def __add__(self, other):
        if isinstance(other, self.__class__):
            x = self.x + other.x
            y = self.y + other.y
            return Coordinate(x, y)
        elif isinstance(other, list):
            x = self.x + other[0]
            y = self.y + other[1]
            return Coordinate(x, y)
        else:
            raise TypeError("unsupported operand type(s) for +: '{}' and '{}'").format(self.__class__, type(other))


    def __sub__(self, other):
        if isinstance(other, self.__class__):
            x = self.x + other.x
            y = self.y + other.y
            return Coordinate(x, y)
        elif isinstance(other, list):
            x = self.x - other[0]
            y = self.y - other[1]
            return Coordinate(x, y)
        else:
            raise TypeError("unsupported operand type(s) for -: '{}' and '{}'").format(self.__class__, type(other))
        return

class Rectangle:

    def __init__(self, coordinate1, coordinate2, coordinate3, coordinate4):
        coordinates = (coordinate1, coordinate2, coordinate3, coordinate4)
        x_coordinate = [coordinate.x for coordinate in coordinates]
        y_coordinate = [coordinate.y for coordinate in coordinates]

        self.top = min(y_coordinate)
        self.bottom = max(y_coordinate)
        self.left = min(x_coordinate)
        self.right = max(x_coordinate)

    def get_left_top(self):
        return Coordinate(self.left, self.top)

    def get_right_bottom(self):
        return Coordinate(self.right, self.bottom)

    def get_width(self):
        return self.right - self.left

    def get_height(self):
        return self.bottom - self.top

class ItemFinder:
    UP_LEFT = "ref_image/up_left.png"
    DOWN_LEFT = "ref_image/down_left.png"
    UP_RIGHT = "ref_image/up_right.png"
    DOWN_RIGHT = "ref_image/down_right.png"

    def __init__(self):
        pass

    def mark_item_box(self, image_path):
        rect_object = self.find_rectangle(image_path)
        image_manager = ImageManager(image_path)
        return image_manager.draw_rect(rect_object)

    def find_rectangle(self, image_path):
        image_manager = ImageManager(image_path)

        _, up_left, _, _ = image_manager.image_finder(self.UP_LEFT)
        _, up_right, up_right_width, _ = image_manager.image_finder(self.UP_RIGHT)
        _, down_left, _, down_left_height = image_manager.image_finder(self.DOWN_LEFT)
        _, down_right, down_right_wight, down_right_height = image_manager.image_finder(self.DOWN_RIGHT)

        coordinate1 = Coordinate(up_left[0], up_left[1])
        coordinate2 = Coordinate(up_right[0], up_right[1]).add_width(up_right_width)
        coordinate3 = Coordinate(down_left[0], down_left[1]).add_height(down_left_height)
        coordinate4 = Coordinate(down_right[0], down_right[1]) + [down_right_wight, down_right_height]

        return Rectangle(coordinate1, coordinate2, coordinate3, coordinate4)




if __name__ == '__main__':
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

    path1 = "result1.png"
    path2 = "result2.png"
    path3 = "result3.png"
    path4 = "result4.png"

    UP_LEFT = "ref_image/up_left.png"
    DOWN_LEFT = "ref_image/down_left.png"
    UP_RIGHT = "ref_image/up_right.png"
    DOWN_RIGHT = "ref_image/down_right.png"

    image_manager = ImageManager(FULL_SCREEN)
    image_manager, *_ = image_manager.image_finder(UP_LEFT, use_gray=False)
    image_manager.save_image(path1)

    image_manager, *_ = image_manager.image_finder(DOWN_LEFT, use_gray=False)
    image_manager.save_image(path2)

    image_manager, *_ = image_manager.image_finder(UP_RIGHT, use_gray=False)
    image_manager.save_image(path3)

    image_manager, *_ = image_manager.image_finder(DOWN_RIGHT, use_gray=False)
    image_manager.save_image(path4)


