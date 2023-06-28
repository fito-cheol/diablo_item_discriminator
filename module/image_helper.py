import cv2
import numpy as np
import matplotlib.pyplot as plt

UP_LEFT = "ref_image/up_left.png"
DOWN_LEFT = "ref_image/down_left.png"
UP_RIGHT = "ref_image/up_right.png"
DOWN_RIGHT = "ref_image/down_right.png"

class ImageManager:
    image = None
    def __init__(self, image_path="", image=None):
        if image is not None:
            self.image = image
            return
        if not image_path:
            raise Exception("유효한 경로가 아닙니다")

        self.image = cv2.imread(image_path)
        # cv2.IMREAD_COLOR
        # cv2.IMREAD_GRAYSCALE 이미지를 Grayscale로 읽어 들입니다. 실제 이미지 처리시 중간단계로 많이 사용합니다.
        # cv2.IMREAD_UNCHANGED 이미지파일을 alpha channel까지 포함하여 읽어 들입니다.

    def save_image(self, path):
        cv2.imwrite(path, self.image)

    def show_contour(self):

        image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        # Apply Canny edge detection
        edges = cv2.Canny(image, 100, 200)  # Adjust the threshold values as needed

        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Create a blank image to draw contours on
        contour_image = np.zeros_like(image)

        # Draw contours on the image
        cv2.drawContours(contour_image, contours, -1, (255, 255, 255), 2)  # Change color and thickness as needed

        # Display the original image, edges, and contour image
        cv2.imshow('Original Image', image)
        cv2.imshow('Edges', edges)
        cv2.imshow('Contours', contour_image)

        # Wait for key press and then close the windows
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def show_image(self):
        cv2.imshow('image', self.image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def make_gray_image(self):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        return self(image=gray)

    def make_canny_image(self):
        image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        # Apply Canny edge detection
        edges = cv2.Canny(image, 100, 200)  # Adjust the threshold values as needed

        return self(image = edges)

    def draw_rect(self, rectangle):
        new_image = self.image.copy()
        top_left = list(rectangle.get_left_top())
        bottom_right = list(rectangle.get_right_bottom())
        cv2.rectangle(new_image, top_left, bottom_right, (0, 0, 255), 2)

        return ImageManager(image=new_image)

    def image_finder(self, img_to_find, method_name='cv2.TM_SQDIFF_NORMED', use_gray=True):
        image = self.image
        template = cv2.imread(img_to_find)

        if use_gray:
            image = make_color_2_grey(image)
            template = make_color_2_grey(template)

        template_height, template_width = template.shape[:2]
        img_draw = image.copy()
        method = eval(method_name)
        # 템플릿 매칭   ---①
        res = cv2.matchTemplate(image, template, method)
        # 최솟값, 최댓값과 그 좌표 구하기 ---②
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        # TM_SQDIFF의 경우 최솟값이 좋은 매칭, 나머지는 그 반대 ---③
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
            match_val = 1 - min_val
        else:
            top_left = max_loc
            match_val = max_val

        # 매칭 좌표 구해서 사각형 표시   ---④
        bottom_right = (top_left[0] + template_width, top_left[1] + template_height)
        cv2.rectangle(img_draw, top_left, bottom_right, (0, 0, 255), 2)
        # 매칭 포인트 표시 ---⑤
        cv2.putText(img_draw, str(match_val), top_left, \
                    cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 1, cv2.LINE_AA)

        return ImageManager(image=img_draw), top_left, template_height, template_width

def save_image(image, path="result.png"):
    cv2.imwrite(path, image)

def show_image(image, grey=False):
    plt.subplot(1, 1, 1)
    try:
        img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    except Exception as e:
        print(e)
        plt.imshow(image)
        plt.show()
        return

    if grey:
        plt.imshow(img_gray)
    else:
        plt.imshow(img_rgb)

    plt.show()

def image_finder(image_path, img_to_find, method_name='cv2.TM_SQDIFF_NORMED', use_gray=True):
    img = cv2.imread(image_path)
    template = cv2.imread(img_to_find)

    if use_gray:
        img = make_color_2_grey(img)
        template = make_color_2_grey(template)

    template_height, template_width = template.shape[:2]
    img_draw = img.copy()
    method = eval(method_name)
    # 템플릿 매칭   ---①
    res = cv2.matchTemplate(img, template, method)
    # 최솟값, 최댓값과 그 좌표 구하기 ---②
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # TM_SQDIFF의 경우 최솟값이 좋은 매칭, 나머지는 그 반대 ---③
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
        match_val = 1 - min_val
    else:
        top_left = max_loc
        match_val = max_val

    # 매칭 좌표 구해서 사각형 표시   ---④
    bottom_right = (top_left[0] + template_width, top_left[1] + template_height)
    cv2.rectangle(img_draw, top_left, bottom_right, (0, 0, 255), 2)
    # 매칭 포인트 표시 ---⑤
    cv2.putText(img_draw, str(match_val), top_left, \
    cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 1, cv2.LINE_AA)

    return img_draw, top_left, template_height, template_width

def method_checker(image_path, img_to_find=UP_LEFT):
    img = cv2.imread(image_path)
    template = cv2.imread(img_to_find)
    th, tw = template.shape[:2]
    cv2.imshow('template', template)

    # 3가지 매칭 메서드 순회
    methods = ['cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR_NORMED', \
               'cv2.TM_SQDIFF_NORMED']

    for i, method_name in enumerate(methods):
        img_draw = img.copy()
        method = eval(method_name)
        # 템플릿 매칭   ---①
        res = cv2.matchTemplate(img, template, method)
        # 최솟값, 최댓값과 그 좌표 구하기 ---②
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        print(method_name, min_val, max_val, min_loc, max_loc)

        # TM_SQDIFF의 경우 최솟값이 좋은 매칭, 나머지는 그 반대 ---③
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
            match_val = 1 - min_val
        else:
            top_left = max_loc
            match_val = max_val
        # 매칭 좌표 구해서 사각형 표시   ---④
        bottom_right = (top_left[0] + tw, top_left[1] + th)
        cv2.rectangle(img_draw, top_left, bottom_right, (0, 0, 255), 2)
        # 매칭 포인트 표시 ---⑤
        cv2.putText(img_draw, str(match_val), top_left, \
                    cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 1, cv2.LINE_AA)
        cv2.imshow(method_name, img_draw)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

def make_color_2_grey(image, invert=False):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if invert:
        inverted_gray = 255 - gray # 반전
        return inverted_gray
    else:
        return gray

def crop_imge(image_path, x, y, w, h):
    img = cv2.imread(image_path)
    crop_img = img[y:y + h, x:x + w]
    cv2.imshow("cropped", crop_img)
    cv2.waitKey(0)

def find_rect_with_contour(image_path):
    # https://stackoverflow.com/questions/46486078/opencv-how-to-find-rectangle-contour-of-a-rectangle-with-round-corner
    image = cv2.imread(image_path, 1)
    gray = make_color_2_grey(image)
    gray_inv = cv2.bitwise_not(gray)
    points = cv2.findNonZero(gray)
    rect = cv2.boundingRect(points)

def image_color_2_canny(image_path):
    # Load the image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Apply Canny edge detection
    edges = cv2.Canny(image, 100, 200)  # Adjust the threshold values as needed

    return edges



def draw_contour(image_path):
    # Load the image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Apply Canny edge detection
    edges = cv2.Canny(image, 100, 200)  # Adjust the threshold values as needed

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create a blank image to draw contours on
    contour_image = np.zeros_like(image)

    # Draw contours on the image
    cv2.drawContours(contour_image, contours, -1, (255, 255, 255), 2)  # Change color and thickness as needed

    # Display the original image, edges, and contour image
    cv2.imshow('Original Image', image)
    cv2.imshow('Edges', edges)
    cv2.imshow('Contours', contour_image)

    # Wait for key press and then close the windows
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    draw_contour("image/FullScreen.png")