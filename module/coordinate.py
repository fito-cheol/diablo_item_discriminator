
class Coordinate:
    """ Common Coordinate  """

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'({self.x}, {self.y})'

    def __iter__(self):
        yield self.x
        yield self.y

    def add_y(self, y: int):
        """
        y 변경 함수입니다
        y (int): decimal number
        """
        new_y = self.y + y
        return Coordinate(self.x, new_y)

    def add_x(self, x: int):
        """
        x 변경 함수입니다
        x (int): decimal number
        """
        new_x = self.x + x
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
            raise TypeError(f"unsupported operand type(s) for +: {self.__class__} and { type(other)}")
        
    def __radd__(self, other):
        if isinstance(other, self.__class__):
            x = self.x + other.x
            y = self.y + other.y
            return Coordinate(x, y)
        elif isinstance(other, list):
            x = self.x + other[0]
            y = self.y + other[1]
            return Coordinate(x, y)
        else:
            raise TypeError(f"unsupported operand type(s) for +: {self.__class__} and { type(other)}")

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
            raise TypeError(f"unsupported operand type(s) for +: {self.__class__} and { type(other)}")
        
    def __rsub__(self, other):
        if isinstance(other, self.__class__):
            x = self.x + other.x
            y = self.y + other.y
            return Coordinate(x, y)
        elif isinstance(other, list):
            x = self.x - other[0]
            y = self.y - other[1]
            return Coordinate(x, y)
        else:
            raise TypeError(f"unsupported operand type(s) for +: {self.__class__} and { type(other)}")


class Rectangle:
    """ Recieve Coordinates and Make Rect that contain Coordinates """

    def __init__(self, coordinate1, coordinate2, coordinate3, coordinate4):
        coordinates = (coordinate1, coordinate2, coordinate3, coordinate4)
        x_coordinate = [coordinate.x for coordinate in coordinates]
        y_coordinate = [coordinate.y for coordinate in coordinates]

        self.top = min(y_coordinate)
        self.bottom = max(y_coordinate)
        self.left = min(x_coordinate)
        self.right = max(x_coordinate)

    def get_left_top(self):
        """ 좌상단 Coordinate """
        return Coordinate(self.left, self.top)

    def get_right_bottom(self):
        """ 우하단 Coordinate """
        return Coordinate(self.right, self.bottom)

    def get_width(self):
        """ 너비 """
        return self.right - self.left

    def get_height(self):
        """ 높이 """
        return self.bottom - self.top
