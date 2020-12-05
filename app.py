# Import libary yang diperlukan
from flask import Flask, request, Response
from fer import FER
import numpy
import cv2
import pandas as pd

app = Flask(__name__)

# Tipe file yang dibolehkan
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

# Fungsi untuk ccek tipe file


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Fungsi untuk url upload file


@app.route('/upload', methods=['POST'])
def hello_world():
    # Fungsi ini tujuan untuk menampilkan emosi dari gambar
    # Tanpa menyimpan file tersebut ke dalam penyimpanan
    top = request.form.get('top')

    # Cek jika form data terdapat image
    if 'image' not in request.files:
        return {'message': 'No File Part'}
    image = request.files['image']

    # Cek jika image memiliki nama
    if image.filename == '':
        return {'message': 'No Selected File'}

    # Cek jika image ada dan tipe file dibolehkan
    if image and allowed_file(image.filename):
        # Buat gambar menjadi string
        image_string = image.read()
        #  Ubah ke dalam numpy
        np_img = numpy.fromstring(image_string, numpy.uint8)
        # Simpan ke dalam cv2
        img = cv2.imdecode(np_img, cv2.IMREAD_UNCHANGED)

        # Siapkan pendeteksi
        detector = FER()

        # Top = 1 jika ingin menampilkan emosi tertinggi
        if top == '1':
            emotion, score = detector.top_emotion(img)
            data = {'emotion': emotion, 'score': float(score)}
        # Top = 0 jika ingin menampilkan peluang beberapa emosi
        else:
            result = detector.detect_emotions(img)
            data = pd.DataFrame(result).to_json()

        return data

    return 'Hello, World!'
