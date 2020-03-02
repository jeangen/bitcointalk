import os
import time
import zmq
from datetime import datetime

def log(e):
    context = zmq.Context()
    logger = context.socket(zmq.PUSH)
    logger.connect('tcp://127.0.0.1:5858')
    subject = "Bitcointalk V2 parou de funcionar"
    body = f"{e}"
    message = {'subject': subject, 'body': body}
    logger.send_json(message)
    logger.close()

while True:
    try:
        os.system('scrapy crawl bitcointalk')
        print('=============================DONE=============================')
        time.sleep(600)

    except Exception as e:
        log(e)
        time.sleep(600)