"""
Core module of the lighting system

The core module loads all dependent modules and runs the whole package.

Author: Leonard de Vries
Created: 12-07-2016
"""
import logging
import time
from Queue import Queue
from threading import Thread

import websocket
import common.log
import common.config
import events

common.log.setup_logging()
logger = logging.getLogger(__name__)
common.config.load_config(__file__)
config = common.config.config

class LightManager:
    def __init__(self):
        self.events = events.EventListener(callback=self.event_callback)
        self.events.register_event_source(events.DummyEventSource)
        self.pool = Queue(maxsize=100)
        self.con_client = Thread(target=self.communication_client)
        self.con_client.daemon = True
        self.con_client.start()

    def event_callback(self, event):
        logger.info("Got event: {}".format(event))
        self.pool.put_nowait(event)

    def run(self):
        while True:
            time.sleep(10)

    def communication_client(self):
        ws = WebSocketClient()
        while True:
            message = self.pool.get()
            ws.send(str(message))


class WebSocketClient:
    def __init__(self):
        self.url = config.get("remote", "host", default="ws://localhost:8888/ws")
        self.key = config.get("remote", "key")
        Thread(target=self.connect).start()

    def connect(self):
        while True:
            self.ws = websocket.WebSocketApp(url=self.url, on_open=self.on_open, on_message=self.on_message)
            self.ws.run_forever()
            time.sleep(5)

    def on_open(self, ws):
        logger.info('opened connection to {}!'.format(self.url))

    def on_message(self, ws, message):
        if "AUTH_OK" in message:
            logger.info("Authentication successful!")
        elif "AUTH" in str(message):
            logger.info("Got authentication request, trying authentication..")
            self.ws.send("KEY:{}".format(self.key))
        else:
            logger.info("Received message: {}".format(message))

    def on_close(self, ws, code=1000, *reason):
        pass

    def send(self, message):
        self.ws.send(message)


def run():
    logger.info("running core..")

    lm = LightManager()
    lm.run()

run()
