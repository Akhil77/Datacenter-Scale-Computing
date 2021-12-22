#!/usr/bin/env python3
from __future__ import print_function

import base64
import random
import sys
import time

import grpc

import service_pb2
import service_pb2_grpc


def doRawImage(addr, debug=False):
    stub = service_pb2_grpc.MainStub(channel)
    img = open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb').read()
    response = stub.GetRawDimensons(service_pb2.rawImageMsg(img=img))

    if debug:
        print("Response : \n", response)


def doAdd(addr, debug=False):
    stub = service_pb2_grpc.MainStub(channel)

    response = stub.AddBothNumbers(service_pb2.addMsg(a=5, b=10))

    if debug:
        # decode response
        print("Response : \n", response)


def doDotProduct(addr, debug=False):
    stub = service_pb2_grpc.MainStub(channel)

    a = [random.random()] * 100
    b = [random.random()] * 100
    response = stub.GetDotProduct(service_pb2.dotProductMsg(a=a, b=b))

    if debug:
        # decode response
        print("Response : \n", response)


def doJsonImage(addr, debug=False):
    stub = service_pb2_grpc.MainStub(channel)

    img = open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb').read()
    base_64_encoded = base64.b64encode(img)
    base_64_string_form = base_64_encoded.decode("ascii")

    response = stub.GetJsonDimensons(service_pb2.jsonImageMsg(img=base_64_string_form))

    if debug:
        # decode response
        print("Response : \n", response)


if len(sys.argv) < 3:
    print(f"Usage: {sys.argv[0]} <server ip> <cmd> <reps>")
    print(f"where <cmd> is one of add, rawImage, sum or jsonImage")
    print(f"and <reps> is the integer number of repititions for measurement")

host = sys.argv[1]
cmd = sys.argv[2]
reps = int(sys.argv[3])

addr = f"{host}:50051"
print(f"Running {reps} reps against {addr}")

channel = grpc.insecure_channel(addr)

with channel:
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
