#!/usr/bin/env python3
from __future__ import print_function

import base64
import json
import random
import sys
import time

import jsonpickle
import requests


def doRawImage(addr, debug=False):
    # prepare headers for http request
    headers = {'content-type': 'image/png'}
    img = open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb').read()
    image_url = addr + '/api/rawimage'
    response = requests.post(image_url, data=img, headers=headers)
    if debug:
        # decode response
        print("Response is", response)
        print(json.loads(response.text))


def doAdd(addr, debug=False):
    headers = {'content-type': 'application/json'}
    add_url = addr + "/api/add/5/10"
    response = requests.post(add_url, headers=headers)
    if debug:
        # decode response
        print("Response is", response)
        print(json.loads(response.text))


def doDotProduct(addr, debug=False):
    headers = {'content-type': 'application/json'}
    dotProductUrl = addr + "/api/dotproduct"

    a = [random.random()] * 100
    b = [random.random()] * 100

    vectors = {
        'a': a,
        'b': b
    }
    response = requests.post(dotProductUrl, data=jsonpickle.encode(vectors), headers=headers)
    if debug:
        # decode response
        print("Response is", response)
        print(json.loads(response.text))


def doJsonImage(addr, debug=False):
    headers = {'content-type': 'application/json'}
    json_image_url = addr + "/api/jsonimage"
    img = open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb').read()

    base_64_encoded = base64.b64encode(img)
    base_64_string_form = base_64_encoded.decode("ascii")
    body = {
        'image': base_64_string_form
    }

    response = requests.post(json_image_url, data=jsonpickle.encode(body), headers=headers)
    if debug:
        # decode response
        print("Response is", response)
        print(json.loads(response.text))


if len(sys.argv) < 3:
    print(f"Usage: {sys.argv[0]} <server ip> <cmd> <reps>")
    print(f"where <cmd> is one of add, rawImage, sum or jsonImage")
    print(f"and <reps> is the integer number of repititions for measurement")

host = sys.argv[1]
cmd = sys.argv[2]
reps = int(sys.argv[3])

addr = f"http://{host}:5000"
print(f"Running {reps} reps against {addr}")

if cmd == 'rawImage':
    start = time.perf_counter()
    for x in range(reps):
        doRawImage(addr, debug=False)
    delta = ((time.perf_counter() - start) / reps) * 1000
    print("Took", delta, "ms per operation")
elif cmd == 'add':
    start = time.perf_counter()
    for x in range(reps):
        doAdd(addr, debug=False)
    delta = ((time.perf_counter() - start) / reps) * 1000
    print("Took", delta, "ms per operation")
elif cmd == 'jsonImage':
    start = time.perf_counter()
    for x in range(reps):
        doJsonImage(addr, debug=False)
    delta = ((time.perf_counter() - start) / reps) * 1000
    print("Took", delta, "ms per operation")
elif cmd == 'dotProduct':
    start = time.perf_counter()
    for x in range(reps):
        doDotProduct(addr, debug=False)
    delta = ((time.perf_counter() - start) / reps) * 1000
    print("Took", delta, "ms per operation")
else:
    print("Unknown option", cmd)
