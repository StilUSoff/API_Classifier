import os
import sys
import patoolib
import tempfile
from flask import Flask, request, jsonify
from classifier import main
import argparse

app = Flask(__name__)
temp_folder = tempfile.mkdtemp()

@app.route('/classify', methods=['POST'])
def classify_image():
    if 'image' in request.files:
        image = request.files['image']
        try:
            original_filename = image.filename
            original_filepath = os.path.join(temp_folder, original_filename)
            image.save(original_filepath)
            result = main(original_filepath)
        finally:
            os.remove(original_filepath)  # Удалить временный файл после обработки
        return jsonify({"result": result})
    elif 'archive' in request.files:
        archive = request.files['archive']
        try:
            archive.save(os.path.join(temp_folder, archive.filename))  # Сохраняем архив на сервере
            patoolib.extract_archive(os.path.join(temp_folder, archive.filename), outdir=temp_folder)  # Разархивируем архив с помощью patool
            os.remove(os.path.join(temp_folder, archive.filename))
            result = main(temp_folder)
        finally:
            print()
            [os.remove(os.path.join(temp_folder, f)) for f in os.listdir(temp_folder)]
        return jsonify({"result": result})
    else:
        return jsonify({"error": "Invalid request"})

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default="0.0.0.0", help="host address")
    parser.add_argument('--port', type=int, default=5000, help="port number")
    args = parser.parse_args()
    app.run(host=args.host, port=args.port)