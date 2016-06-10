#!/usr/bin/env python
import pika
import json
import socket
import os

RABBIT_MQ_SERVER = os.environ["RABBIT_MQ_SERVER"]
RABBIT_MQ_USER = os.environ["RABBIT_MQ_USER"]
RABBIT_MQ_PWD = os.environ["RABBIT_MQ_PWD"]

credentials = pika.PlainCredentials(RABBIT_MQ_USER, RABBIT_MQ_PWD)

connection = pika.BlockingConnection(pika.ConnectionParameters(
               RABBIT_MQ_SERVER, credentials = credentials))
channel = connection.channel()

def callback(ch, method, properties, body):
    req = json.loads(body)

    status = req["monitor"]["result"]["status"]
    if status != "ok" :
        key = req["monitor"]["notifier"]["type"]
        resp = json.dumps(req)
        channel.basic_publish(exchange='notifiers',
                          routing_key=key,
                          body=resp)

channel.basic_consume(callback,
                      queue='results',
                      no_ack=True)
channel.start_consuming()
