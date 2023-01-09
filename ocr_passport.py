# Імпортуємо необхідні модулі.
import sys

import pytesseract
import cv2
import imutils
from imutils.contours import sort_contours
import numpy as np

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract"
)


def ocr_passport(image) -> str:
    """
    Відокремити ділянку, що містить MRZ (машинозчитувану зону), 
    з фотографії паспорта та розпізнати її символи.
    """
    # Завантажимо вхідне зображення, перетворимо його на відтінки 
    # сірого та візьмемо його розміри.
    image = cv2.imread(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    (HEIGHT, WIDTH) = gray.shape

    # Ініціалізуємо прямокутне і квадратне структурне ядро.
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 7))
    sq_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 21))

    # Згладьмо зображення за допомогою 3х3 розмивання Гауса 
    # і застосуємо морфологічний оператор blackhat для знаходження 
    # темних областей на світлому фоні.
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, rect_kernel)
    # cv2.imshow("Blackhat", blackhat)
    
    # Підкреслимо контури шрифтів за допомогою градієнта.
    grad = cv2.Sobel(blackhat, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
    grad = np.absolute(grad)
    (min_val, max_val) = (np.min(grad), np.max(grad))
    grad = (grad - min_val) / (max_val - min_val)
    grad = (grad * 255).astype("uint8")

    grad = cv2.morphologyEx(grad, cv2.MORPH_CLOSE, rect_kernel)
    thresh = cv2.threshold(grad, 0, 255, 
        cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, sq_kernel)
    thresh = cv2.erode(thresh, None, iterations=2)
    # cv2.imshow("thresh", thresh)
    
    # Знайдімо контури на бінарному зображенні й відсортуймо їх 
    # знизу і догори (оскільки MRZ завжди внизу паспорта).
    contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, 
        cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    contours = sort_contours(contours, method="bottom-to-top")[0]

    # Ініціалізуймо змінну, пов'язану з MRZ.
    mrz_box = None

    # Переберемо отримані конури.
    for c in contours:
        # Обчислимо обмежувальну рамку навколо контуру, 
        # виведемо частину зображення, яку вона займає, 
        # і висоту цієї частини, і її ширину.
        (x, y, w, h) = cv2.boundingRect(c)
        percent_height = h / float(HEIGHT)
        percent_width = w / float(WIDTH)
        
        # Якщо обмежувальна рамка займає більше 80% ширини та 4% висоти 
        # зображення, то припустимо, що ми знайшли MRZ.
        if percent_width > 0.8 and percent_height > 0.04:
            mrz_box = (x, y, w, h)
            break

    # Якщо MRZ не було знайдене, то зупинімо програму.
    if mrz_box is None:
        print("Машинозчитувану зону не було знайдено.")
        sys.exit(0)

    # Збільшимо обмежувальну рамку, оскільки ми застосували ерозію, 
    # і тепер її потрібно відновити.
    (x, y, w, h) = mrz_box
    pad_x = int((x+w) * 0.03)
    pad_y = int((y+h) * 0.03)
    (x, y) = (x - pad_x, y - pad_y)
    (w, h) = (w + (pad_x*2), h + (pad_y*2))

    # Вилучимо отриману рамку з вхідного зображення.
    mrz = image[y:y + h, x:x + w]

    # Перетворимо знайдену ділянку з MRZ у текст, використовуючи 
    # Tesseract і видаляючи будь-які пробіли. 
    # Використаймо треновану на шрифті OCR-B модель Tesseract, 
    # аби поліпшити точність програми.
    mrz_text = pytesseract.image_to_string(mrz, lang="ocrb")
    mrz_text = mrz_text.replace(" ", "")
    # cv2.imshow("MRZ", mrz)
    # cv2.waitKey(0)
    
    return mrz_text


if __name__ == "__main__":
    print(ocr_passport(input("Введіть шлях до фото паспорта: ")))