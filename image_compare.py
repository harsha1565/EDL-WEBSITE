import cv2
import numpy as np
from PIL import Image
import imagehash
from skimage.metrics import structural_similarity as ssim


def phash_similarity(path1, path2, thresh=10):
    a = Image.open(path1).convert('RGB')
    b = Image.open(path2).convert('RGB')
    h1 = imagehash.phash(a)
    h2 = imagehash.phash(b)
    dist = h1 - h2
    return 0 if dist <= thresh else 1


def color_hist_similarity(path1, path2, thresh=0.3):
    # Use HSV color histogram and Bhattacharyya distance
    a = cv2.imread(path1)
    b = cv2.imread(path2)
    if a is None or b is None:
        raise ValueError('Could not read one of the images for color histogram')
    a_hsv = cv2.cvtColor(a, cv2.COLOR_BGR2HSV)
    b_hsv = cv2.cvtColor(b, cv2.COLOR_BGR2HSV)
    histA = cv2.calcHist([a_hsv], [0, 1], None, [50, 60], [0, 180, 0, 256])
    histB = cv2.calcHist([b_hsv], [0, 1], None, [50, 60], [0, 180, 0, 256])
    cv2.normalize(histA, histA)
    cv2.normalize(histB, histB)
    d = cv2.compareHist(histA, histB, cv2.HISTCMP_BHATTACHARYYA)
    return 0 if d <= thresh else 1


def ssim_similarity(path1, path2, thresh=0.5):
    a = cv2.imread(path1, cv2.IMREAD_GRAYSCALE)
    b = cv2.imread(path2, cv2.IMREAD_GRAYSCALE)
    if a is None or b is None:
        raise ValueError('Could not read one of the images for SSIM')
    # resize to same size (small) to speed up
    if a.shape != b.shape:
        b = cv2.resize(b, (a.shape[1], a.shape[0]))
    score = ssim(a, b)
    return 0 if score >= thresh else 1


def keypoint_similarity(path1, path2, min_matches=10):
    a = cv2.imread(path1, cv2.IMREAD_GRAYSCALE)
    b = cv2.imread(path2, cv2.IMREAD_GRAYSCALE)
    if a is None or b is None:
        raise ValueError('Could not read one of the images for keypoint matching')
    # use ORB
    orb = cv2.ORB_create(5000)
    kp1, des1 = orb.detectAndCompute(a, None)
    kp2, des2 = orb.detectAndCompute(b, None)
    if des1 is None or des2 is None:
        return 1
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)
    matches = sorted(matches, key=lambda x: x.distance)
    good = [m for m in matches if m.distance < 70]
    return 0 if len(good) >= min_matches else 1


def edge_similarity(path1, path2, thresh=0.4):
    a = cv2.imread(path1, cv2.IMREAD_GRAYSCALE)
    b = cv2.imread(path2, cv2.IMREAD_GRAYSCALE)
    if a is None or b is None:
        raise ValueError('Could not read one of the images for edge similarity')
    # Canny edges
    a = cv2.resize(a, (500, 500)) if a.shape[0] > 500 or a.shape[1] > 500 else a
    b = cv2.resize(b, (a.shape[1], a.shape[0]))
    edgesA = cv2.Canny(a, 100, 200)
    edgesB = cv2.Canny(b, 100, 200)
    # compare edge maps with SSIM
    score = ssim(edgesA, edgesB)
    return 0 if score >= thresh else 1


def compare_images(path1, path2):
    features = {}
    features['perceptual_hash'] = phash_similarity(path1, path2)
    features['color_histogram'] = color_hist_similarity(path1, path2)
    features['ssim'] = ssim_similarity(path1, path2)
    features['keypoint_match'] = keypoint_similarity(path1, path2)
    features['edge_similarity'] = edge_similarity(path1, path2)

    matched = [k for k, v in features.items() if v == 0]
    result = {
        'features': features,
        'matched_count': len(matched),
        'matched_features': matched
    }
    return result
