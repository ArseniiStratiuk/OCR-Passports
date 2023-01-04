# Import the necessary packages.
import sys
import time

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
    Separate the area containing MRZ (Machine Readable Zone) 
    from the passport photo and OCR it.
    """
    # Завантажимо вхідне зображення, перетворимо його на відтінки 
    # сірого та візьмемо його розміри.
    image = cv2.imread(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    (H, W) = gray.shape

    # Ініціалізуємо прямокутне і квадратне структурне ядро.
    rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 7))
    sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 21))

    # Smooth the image using a 3x3 Gaussian blur and then apply a 
    # blackhat morpholigical operator to find dark regions on a light 
    # background.
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, rectKernel)
    
    # Підкреслимо контури шрифтів за допомогою градієнта.
    grad = cv2.Sobel(blackhat, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
    grad = np.absolute(grad)
    (minVal, maxVal) = (np.min(grad), np.max(grad))
    grad = (grad - minVal) / (maxVal - minVal)
    grad = (grad * 255).astype("uint8")

    grad = cv2.morphologyEx(grad, cv2.MORPH_CLOSE, rectKernel)
    thresh = cv2.threshold(grad, 0, 255, 
        cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, sqKernel)
    thresh = cv2.erode(thresh, None, iterations=2)

    # Find contours in the thresholded image and sort them from bottom 
    # to top (since the MRZ will always be at the bottom of the passport).
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, 
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sort_contours(cnts, method="bottom-to-top")[0]

    # Initialize the bounding box associated with the MRZ.
    mrzBox = None

    # Loop over the contours.
    for c in cnts:
        # Compute the bounding box of the contour and then derive the 
        # how much of the image the bounding box occupies in terms of 
        # both width and height.
        (x, y, w, h) = cv2.boundingRect(c)
        percentWidth = w / float(W)
        percentHeight = h / float(H)
        
        # If the bounding box occupies > 80% width and > 4% height of the 
        # image, then assume we have found the MRZ.
        if percentWidth > 0.8 and percentHeight > 0.04:
            mrzBox = (x, y, w, h)
            break

    # If the MRZ was not found, exit the script.
    if mrzBox is None:
        print("[INFO] MRZ could not be found")
        sys.exit(0)

    # Pad the bounding box since we applied erosions and now need to re-grow it.
    (x, y, w, h) = mrzBox
    pX = int((x+w) * 0.03)
    pY = int((y+h) * 0.03)
    (x, y) = (x - pX, y - pY)
    (w, h) = (w + (pX*2), h + (pY*2))

    # Extract the padded MRZ from the image.
    mrz = image[y:y + h, x:x + w]

    # OCR the MRZ region of interest using Tesseract, 
    # removing any occurrences of spaces. 
    # Use Tesseract trained on the ocrb font for improved accuracy.
    mrzText = pytesseract.image_to_string(mrz, lang="ocrb")
    mrzText = mrzText.replace(" ", "")
    return mrzText


if __name__ == "__main__":
    print(ocr_passport(input("Введіть шлях до фото паспорта: ")))