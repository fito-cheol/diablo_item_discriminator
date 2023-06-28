# https://pi000.tistory.com/19
# install tesseract for window https://github.com/UB-Mannheim/tesseract/wiki
import numpy as np
from pytesseract import Output
import pytesseract
import cv2

from PIL import Image

"""
https://cloud.google.com/python/docs/reference/vision/latest
- project 만들기 billing 설정 건너뛰기
1. Cloud Vision API 사용
2. 사용자 인증 정보에서 서비스 계정 생성
3. 서비스 계정에서 키 생성
4. 환경변수로 생성된 json키 경로 할당
GOOGLE_APPLICATION_CREDENTIALS: C:/Users/dmsgh/AppData/Local/Google/CustomKey/diablo.json

"""


# https://cloud.google.com/python/docs/reference/vision/latest

def image_to_text(image_path, img_path_grey):
    config = ('kor')

    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    out = gray.copy()
    inverse_gray = 255 - out

    cv2.imwrite(img_path_grey, inverse_gray)

    img1 = np.array(Image.open(image_path))

    text = pytesseract.image_to_string(img1, lang='kor')
    return text

def detect_text(path):
    """Detects text in the file."""
    from google.cloud import vision

    client = vision.ImageAnnotatorClient()

    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print("Texts:")

    for text in texts:
        print(f'\n"{text.description}"')

        vertices = [
            f"({vertex.x},{vertex.y})" for vertex in text.bounding_poly.vertices
        ]

        print("bounds: {}".format(",".join(vertices)))

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )
    return texts


if __name__ == '__main__':


    google_file_path = '../image/FullScreen.png'
    text_result = detect_text(google_file_path)

    if len(text_result) == 0:
        exit(0)

    with open("../result_brief.text", "w+", encoding="utf8") as f:
        f.writelines(text_result[0].description)

    with open("result.text","w+", encoding="utf8") as f:
        for text in text_result:
            f.writelines(text.descripton)
            vertices = [
                f"({vertex.x},{vertex.y})" for vertex in text.bounding_poly.vertices
            ]
            f.writelines("bounds: {}".format(",".join(vertices)))

    # img_path = 'image/item_1.png'
    # img_path_grey = 'image/item_1_grey.png'
    # parsed_text = image_to_text(img_path, img_path_grey)
    # print(img_path, parsed_text)

    # 사용 가능한 언어 출력
    # langs = pytesseract.get_languages(config='')
    # print(langs)


"""
"마름병 이빨 달린 저승 낫
선조 전설 양손 낫
아이템 위력 806+25
업그레이드: 5/5
2,593 초당 공격력 (+61)
◆
◆
•
적중당 공격력 [2,306 - 3,458]
초당 공격 횟수 0.90 (느린 무기)
처치 시 생명력 +329 +[329]
감속 적에게 주는 피해 +58.5% [49.5 -
70,5]%
모든 능력치 +66 +[60 - 84]
기절 적에게 주는 피해 +64.5% [49.5 -
70.5]%
지속 암흑 피해 효과의 영향을 받는 적에게 주
는 피해 +42.0% [21.0 - 42.0]%
* 각인: 그림자 마름병 핵심 지속 효과가 적에게 10
번 피해를 준 후 6초 동안 주는 피해가 212%[x]
[100 - 240]% 증가합니다. (강령술사 전용)
지속 피해 +7.0%
지속 피해 +7.0%"
"""