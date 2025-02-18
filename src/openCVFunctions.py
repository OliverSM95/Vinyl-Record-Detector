import cv2
from glob import glob
import numpy as np


#----------Load Images-----------
def load_images_folder():
    # load photos
    record_images = glob('Test Photos/*.jpg')
    return  record_images

def load_image(images_folder,i):
    return cv2.imread(images_folder[i])


def detect_and_outline_squares(image):
    """Detects and outlines square objects in an image using OpenCV."""
    if image is None:
        print("❌ Error: Could not load image.")
        return



def edge_detector(image):
    #convert image to grayscale
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    # Apply GaussianBlur to remove noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply Canny Edge Detection
    canny = cv2.Canny(blurred, 50, 150)  # Adjust thresholds if needed
    return canny



