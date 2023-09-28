import cv2
import numpy as np


face_classifier = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

def face_in_frame(image:np.ndarray, cv2_format=False, scaledown_factor=1.1, min_neighbors=10, min_size=(40, 40), min_percentage_size=(50, 30)) -> bool:
    percentage = lambda full_length, length: (length/full_length)*100
    get_percentage_px = lambda full_length, percentage: int((full_length/100)*percentage)
    min_w, min_h = min_size
    img_w, img_h, *_ = image.shape
    per_w, per_h = min_percentage_size
    min_size = (
        min_w if percentage(img_w, min_w) > per_w else get_percentage_px(img_w, per_w),
        min_h if percentage(img_h, min_h) > per_h else get_percentage_px(img_h, per_h)
    )
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY if cv2_format else cv2.COLOR_RGB2GRAY)
    faces = face_classifier.detectMultiScale(gray_image, scaleFactor=scaledown_factor, minNeighbors=min_neighbors, minSize=min_size)
    for _ in faces:
        return True
    return False

