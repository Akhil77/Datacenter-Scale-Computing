#
# Worker server
#
import pickle
import platform
import io
import os
import sys
import pika
import redis
import hashlib
import json
import requests
import hashlib

from flair.models import TextClassifier
from flair.data import Sentence


hostname = platform.node()

##
## Configure test vs. production
##
redisHost = os.getenv("REDIS_HOST") or "localhost"
rabbitMQHost = os.getenv("RABBITMQ_HOST") or "localhost"

print(f"Connecting to rabbitmq({rabbitMQHost}) and redis({redisHost})")

##
## Set up redis connections
##
db = redis.Redis(host=redisHost, db=1)                                                                           

##
## Set up rabbitmq connection
##
rabbitMQ = pika.BlockingConnection(
        pika.ConnectionParameters(host=rabbitMQHost))
rabbitMQChannel = rabbitMQ.channel()

rabbitMQChannel.exchange_declare(exchange='toWorker', exchange_type='direct')
result = rabbitMQChannel.queue_declare(queue='toWorker')
queue_name = result.method.queue

rabbitMQChannel.queue_bind(
        exchange='toWorker', queue=queue_name, routing_key="toWorker")



rabbitMQChannel.exchange_declare(exchange='logs', exchange_type='topic')
infoKey = f"{platform.node()}.worker.info"
debugKey = f"{platform.node()}.worker.debug"
def log_debug(message, key=debugKey):
    print("DEBUG:", message, file=sys.stdout)
    rabbitMQChannel.basic_publish(
        exchange='logs', routing_key=key, body=message)
def log_info(message, key=infoKey):
    print("INFO:", message, file=sys.stdout)
    rabbitMQChannel.basic_publish(
        exchange='logs', routing_key=key, body=message)


log_debug(queue_name, 'name')

##
## Your code goes here...
##


ALL_CLASSIFIERS = ["sentiment", "sentiment-fast","de-offensive-language"]
classifierModels = []

for cl in ALL_CLASSIFIERS:
    classifierModels.append(TextClassifier.load(cl))



def analyze(text, classifier = "sentiment"):
    if text == "" or text == None:
        raise Exception("Text is not provided.")

    if classifier not in ALL_CLASSIFIERS:
        raise Exception("Classifier provided is not available")
    sentence = Sentence(text)
    index = ALL_CLASSIFIERS.index(classifier)
    classifierModels[index].predict(sentence)
    return sentence.to_dict()


def get_hashed_key(sentence):
    sha256 = hashlib.sha256()
    sha256.update(sentence.encode('utf-8'))
    return sha256.hexdigest()

def on_receving_message(channel, method_frame, header_frame, body):
    request = json.loads(body)
    classifier = request['model']

 
    for sentence in request['sentences']:
        # Redis key <sentence-hash>:<classifer>
        hashed_sentence = get_hashed_key(sentence)
        key = classifier + ":" + hashed_sentence

        db_cached_value = db.get(key)
        if db_cached_value is None:
            log_debug("Analysing new sentences..",'Logging')
            output = analyze(sentence, classifier)
            value = json.dumps(output)
            db.set(key, value)
            db.sadd(classifier, hashed_sentence)

    log_debug('Added to DB', 'Logging')
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)

rabbitMQChannel.basic_consume('toWorker', on_receving_message)
try:
    rabbitMQChannel.start_consuming()
except KeyboardInterrupt:
    rabbitMQChannel.stop_consuming()
rabbitMQChannel.close()