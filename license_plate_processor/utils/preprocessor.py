import cv2
import numpy as np
from scipy import ndimage as inter

def preprocess(img, height=50):
    output_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    output_image = cv2.normalize(output_image, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
    output_image = cv2.resize(output_image, dsize=(int(4.5*height), height), interpolation=cv2.INTER_CUBIC)
    output_image = _correct_skew(output_image)
    return output_image

    
def _correct_skew(image, delta=1, limit=12):
    def determine_score(arr, angle):
        data = inter.rotate(arr, angle, reshape=False, order=0)
        histogram = np.sum(data, axis=1, dtype=float)
        score = np.sum((histogram[1:] - histogram[:-1]) ** 2, dtype=float)
        return histogram, score

    scores = []
    angles = np.arange(-limit, limit + delta, delta)
    for angle in angles:
        _, score = determine_score(image, angle)
        scores.append(score)

    best_angle = angles[scores.index(max(scores))]

    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, best_angle, 1.0)
    corrected = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, \
            borderMode=cv2.BORDER_REPLICATE)
    
    return corrected

    

    