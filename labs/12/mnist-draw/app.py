import base64
import io
import re
import tensorflow

import numpy as np
from PIL import Image
from flask import Flask, jsonify, render_template, request, send_from_directory
from keras.backend import set_session
from keras.engine.saving import load_model

app = Flask("MNIST")


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/predict", methods=["POST"])
def predict():
    global model, graph, session

    res = {"result": 0,
           "data": [],
           "error": ''}

    data = request.get_json()
    data = data["image"]
    img_str = re.search(r'base64,(.*)', data).group(1)
    image_bytes = io.BytesIO(base64.b64decode(img_str))
    im = Image.open(image_bytes)
    arr = np.squeeze(np.array(im)[:, :, 0:1])

    # Normalize and invert pixel values
    arr = (255 - arr) / 255.0

    # Predict class
    with session.as_default():
        with graph.as_default():
            predictions = model.predict(np.array([arr]))[0]

    # Return label data
    res['result'] = 1
    res['data'] = [float(num) for num in predictions]

    return jsonify(res)


if __name__ == "__main__":
    session = tensorflow.Session()
    graph = tensorflow.get_default_graph()

    set_session(session)
    model = load_model('../mnist.net')
    app.run('127.0.0.1', port=8080)
