#!/usr/bin/env python3

import base64
import io

import jsonpickle
from PIL import Image
##
## Sample Flask REST server implementing two methods
##
## Endpoint /api/image is a POST method taking a body containing an image
## It returns a JSON document providing the 'width' and 'height' of the
## image that was provided. The Python Image Library (pillow) is used to
## proce#ss the image
##
## Endpoint /api/add/X/Y is a post or get method returns a JSON body
## containing the sum of 'X' and 'Y'. The body of the request is ignored
##
##
from flask import Flask, request, Response

# Initialize the Flask application
app = Flask(__name__)

import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG)


def extract_dimensions(ioBuffer):
    img = Image.open(ioBuffer)
    response = {
        'width': img.size[0],
        'height': img.size[1]
    }
    return response


@app.route('/api/add/<int:a>/<int:b>', methods=['GET', 'POST'])
def add(a, b):
    response = {'sum': str(a + b)}
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")


# route http posts to this method
@app.route('/api/rawimage', methods=['POST'])
def rawimage():
    r = request
    raw_image = r.data
    ioBuffer = io.BytesIO(raw_image)
    response = extract_dimensions(ioBuffer)
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")


@app.route('/api/dotproduct', methods=['POST'])
def dotproduct():
    r = request.get_json()
    dotproduct = 0
    try:
        a = r['a']
        b = r['b']

        if not (len(a) == len(b)):
            raise Exception
        for i in range(len(a)):
            dotproduct += a[i] * b[i]

        response = {
            "dotproduct": dotproduct
        }
        response_pickled = jsonpickle.encode(response)
        return Response(response=response_pickled, status=200, mimetype="application/json")

    except:
        return Response(response="Bad Request, Check your input vectors", status=400)


# route http posts to this method
@app.route('/api/jsonimage', methods=['POST'])
def jsonimage():
    try:
        r = request.get_json()

        base_64_string = r['image']
        base_64_bytes = base_64_string.encode("ascii")

        img = base64.b64decode(base_64_bytes)

        ioBuffer = io.BytesIO(img)
        response = extract_dimensions(ioBuffer)
        response_pickled = jsonpickle.encode(response)

        return Response(response=response_pickled, status=200, mimetype="application/json")

    except:
        return Response(response="Bad Request, Check your input", status=400)


# start flask app
app.run(host="0.0.0.0", port=5000)
