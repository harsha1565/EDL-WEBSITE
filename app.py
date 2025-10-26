import os
import tempfile
import numpy as np
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from image_compare import compare_images

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compare', methods=['POST'])
def compare():
    if 'img1' not in request.files or 'img2' not in request.files:
        return jsonify({'error': 'Both images (img1 and img2) are required.'}), 400

    f1 = request.files['img1']
    f2 = request.files['img2']

    if f1.filename == '' or f2.filename == '':
        return jsonify({'error': 'Empty filename submitted.'}), 400

    # save to temp files
    tmpdir = tempfile.mkdtemp()
    p1 = os.path.join(tmpdir, secure_filename(f1.filename))
    p2 = os.path.join(tmpdir, secure_filename(f2.filename))
    f1.save(p1)
    f2.save(p2)

    try:
        results = compare_images(p1, p2)
    except Exception as e:
        return jsonify({'error': 'Comparison failed', 'details': str(e)}), 500
    finally:
        # cleanup
        try:
            os.remove(p1)
            os.remove(p2)
            os.rmdir(tmpdir)
        except Exception:
            pass

    return jsonify(results)

if __name__ == '__main__':
    # run on 0.0.0.0:5000 by default
    app.run(host='0.0.0.0', port=5000, debug=True)
