import cv2
import numpy as np
from PIL import Image
import os


def preprocess_image(image):

    # Convert PIL image into NumPy array
    image = np.array(image)

    # Convert RGB image into grayscale
    if len(image.shape) == 3:
        image = cv2.cvtColor(
            image,
            cv2.COLOR_RGB2GRAY
        )

    # Remove noise from image
    image = cv2.GaussianBlur(
        image,
        (3, 3),
        0
    )

    # Improve text visibility
    image = cv2.threshold(
        image,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]

    return Image.fromarray(image)