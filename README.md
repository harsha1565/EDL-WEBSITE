# Image Comparator

Simple Flask app that compares two uploaded images using five features:

- Perceptual hash (phash)
- Color histogram (HSV + Bhattacharyya)
- SSIM (grayscale structural similarity)
- Keypoint matching (ORB + BFMatcher)
- Edge similarity (Canny edges + SSIM)

Each feature returns 0 if images are similar, 1 if not. The API also returns a summary with matched_count and matched_features.

## Setup (Windows PowerShell)

1. Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the app:

```powershell
python app.py
```

4. Open http://127.0.0.1:5000 in your browser.

## API

POST /compare
- Form fields: `img1` (file), `img2` (file)
- Response JSON:
  - features: object with featureName: 0/1
  - matched_count: number of features that returned 0
  - matched_features: array of feature names that matched

## Notes

- Thresholds are conservative defaults. Tweak thresholds in `image_compare.py` for your use-case.
- For large images the app resizes internally for certain comparisons to improve speed.
