import cv2
import numpy as np
import matplotlib.pyplot as plt

class ImageManager:
    """ 이미지 처리기 """

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

    def get_image(self):
        return self.image.copy()

    def show_shape(self):
        print(np.shape(self.image))

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

    def show_image(self, title="Default"):
        blue, green, red = cv2.split(self.image)
        reversed_image = cv2.merge([red,green,blue])
        plt.subplot(1,1,1)
        plt.imshow(reversed_image)
        plt.title(title)
        plt.tight_layout()
        plt.show()
        
    def make_gray_image(self):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        return ImageManager(image=gray)

    def make_canny_image(self, min=80, max=150):
        image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(image, min, max)  # Adjust the threshold values as needed

        return ImageManager(image=edges)

    def draw_rect(self, rectangle):
        new_image = self.image.copy()
        top_left = list(rectangle.get_left_top())
        bottom_right = list(rectangle.get_right_bottom())
        cv2.rectangle(new_image, top_left, bottom_right, (0, 255, 100), 2)

        return ImageManager(image=new_image)

    def crop_imge(self, rectangle):
        top_left = rectangle.get_left_top()
        bottom_right = rectangle.get_right_bottom()
        
        image = self.image
        crop_img = image[top_left.y : bottom_right.y, top_left.x : bottom_right.x]
        return ImageManager(image=crop_img)
    
    def image_finder(self, img_to_find, method_name='cv2.TM_SQDIFF_NORMED'):
        image = self.image.copy()
        image_draw = self.image.copy()
        template = img_to_find.get_image()

        template_height, template_width = template.shape[:2]
        
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
        cv2.rectangle(image_draw, top_left, bottom_right, (0, 0, 255), 2)
        
        # 매칭 포인트 표시 ---⑤
        cv2.putText(image_draw, str(match_val), top_left, \
                    cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 1, cv2.LINE_AA)

        return ImageManager(image=image_draw), top_left, template_height, template_width


    def method_checker(self, image_to_find):
        image = self.image.copy()
        template = image_to_find.get_image()
        th, tw = template.shape[:2]
        cv2.imshow('template', template)

        # 3가지 매칭 메서드 순회
        methods = ['cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR_NORMED', \
                'cv2.TM_SQDIFF_NORMED']

        for method_name in methods:
            method = eval(method_name)
            # 템플릿 매칭   ---①
            res = cv2.matchTemplate(image, template, method)
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
            cv2.rectangle(image, top_left, bottom_right, (0, 0, 255), 2)
            # 매칭 포인트 표시 ---⑤
            cv2.putText(image, str(match_val), top_left, \
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 1, cv2.LINE_AA)
            cv2.imshow(method_name, image)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

