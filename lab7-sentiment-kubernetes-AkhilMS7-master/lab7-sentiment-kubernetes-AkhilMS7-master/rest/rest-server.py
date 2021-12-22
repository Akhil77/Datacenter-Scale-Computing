##
from flask import Flask, request, Response, jsonify
import platform
import io, os, sys
import pika, redis
import hashlib, requests
import json

redisHost = os.getenv("REDIS_HOST") or "localhost"
rabbitMQHost = os.getenv("RABBITMQ_HOST") or "localhost"

print("Connecting to rabbitmq({}) and redis({})".format(rabbitMQHost, redisHost))

infoKey = f"{platform.node()}.worker.info"
debugKey = f"{platform.node()}.worker.debug"

db = redis.Redis(host=redisHost, db=1, decode_responses=True)

app = Flask("Server")

def log_debug(rabbitMQChannel,message, key=debugKey):
    print("DEBUG:", message, file=sys.stderr)
    rabbitMQChannel.basic_publish(
        exchange='logs', routing_key=key, body=message)


def get_hashed_key(sentence):
    sha256 = hashlib.sha256()
    sha256.update(sentence.encode('utf-8'))
    return sha256.hexdigest()


def response_sentence(text, analysis):
    #Response sentence
    sentence_resp = {
        "analysis": analysis,
        "text": text
    }
    return sentence_resp


@app.route('/', methods=['GET'])
def hello():
    return '<h1> Sentiment Server</h1><p> Use a valid endpoint </p>'


@app.route("/apiv1/analyze", methods=['POST'])
def analyze():
    data = request.json
    message_body = json.dumps(data)

    rabbitMQ = pika.BlockingConnection(
    pika.ConnectionParameters(host=rabbitMQHost))
    rabbitMQChannel = rabbitMQ.channel()

    rabbitMQChannel.exchange_declare(exchange='toWorker', exchange_type='direct')
    rabbitMQChannel.exchange_declare(exchange='logs', exchange_type='topic')

    log_debug(rabbitMQChannel, f"Sending request {message_body}")
    rabbitMQChannel.basic_publish(exchange='toWorker', routing_key='toWorker', body=message_body.encode())
    rabbitMQChannel.close()
    return json.dumps({
        "action": "queued"
    })


@app.route("/apiv1/cache/<model>", methods=['GET'])
def cache(model):
    sentences = db.smembers(model)
    keys = []
    for s in sentences:
        keys.append(model + ":" + s)

    values = db.mget(keys)
    response = {
        'model': model,
        'sentences': []
    }

    for val in values:
        if val:
            analysis = {
                'model': model,
                'result': json.loads(val)
            }
            response['sentences'].append(analysis)
    return json.dumps(response)


@app.route("/apiv1/sentence", methods=["POST"])
def sentence():
    data = request.json
    model = data['model']
    keys = []

    for s in data["sentences"]:
        keys.append(model + ":" + get_hashed_key(s))
    values = db.mget(keys)

    response = {
        "model": "",
        "sentences": []
    }
    analysis_list = []
    for i, val in enumerate(values):
        analysis = None
        if val:
            analysis = json.loads(val)
        analysis_list.append(response_sentence(data['sentences'][i], analysis))
    response['sentences'] = analysis_list
    response['model'] = model
    return json.dumps(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
