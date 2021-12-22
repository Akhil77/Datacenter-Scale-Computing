from __future__ import print_function

import base64
import io
import sys
from concurrent import futures
import grpc
from PIL import Image

import service_pb2
import service_pb2_grpc


def extract_dimensions(ioBuffer):
    img = Image.open(ioBuffer)

    response = {
        'width': img.size[0],
        'height': img.size[1]
    }

    return response


class MainServicer(service_pb2_grpc.MainServicer):

    def AddBothNumbers(self, request, context):
        sum = request.a + request.b
        return service_pb2.addReply(sum=sum)
    
    def GetRawDimensons(self, request, context):
        io_buffer = io.BytesIO(request.img)
        response = extract_dimensions(io_buffer)
        return service_pb2.imageReply(height=response['height'], width=response['width'])

    def GetDotProduct(self, request, context):
        dotproduct = 0
        try:
            a = request.a
            b = request.b

            if not (len(a) == len(b)):
                raise Exception
            for i in range(len(a)):
                dotproduct += a[i] * b[i]

            return service_pb2.dotProductReply(dotproduct=dotproduct)

        except:
            return service_pb2.dotProductReply(dotproduct=0)
    
    def GetJsonDimensons(self, request, context):
        base_64_string = request.img
        base_64_bytes = base_64_string.encode("ascii")
        img = base64.b64decode(base_64_bytes)
        io_buffer = io.BytesIO(img)

        response = extract_dimensions(io_buffer)
        return service_pb2.imageReply(height=response['height'], width=response['width'])


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    service_pb2_grpc.add_MainServicer_to_server(MainServicer(), server)

    server.add_insecure_port('[::]:50051')
    server.start()
    print('Server is running')
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
