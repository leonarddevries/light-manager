"""
Core module of the lighting system

The core module loads all dependent modules and runs the whole package.

Author: Leonard de Vries
Created: 12-07-2016
"""
import logging
import time
from Queue import Queue, Full
from threading import Thread

import websocket
import common.log
import common.config
import events

common.log.setup_logging()
logger = logging.getLogger("core")
common.config.load_config(__file__)
config = common.config.config


class LightManager:
    def __init__(self):
        self.events = events.EventListener(callback=self.event_callback)
        self.events.register_event_source(events.DummyEventSource)
        self.ws = WebSocketClient()

    def event_callback(self, event):
        logger.info("Got event: {}".format(event))
        self.ws.send(message=str(event))

    def run(self):
        while True:
            time.sleep(10)


class WebSocketClient:
    def __init__(self):
        self.logger = logging.getLogger("core.websocketclient")
        self.authenticated = False
        self.url = config.get("remote", "host", default="ws://localhost:8888/ws")
        self.key = config.get("remote", "key")
        self.pool = Queue(maxsize=config.get("client", "message_pool_size", default=10))
        self.logger.info("Init websockets; pool size {}; server @ {}".format(
            config.get("client", "message_pool_size", default=10),
            self.url
        ))
        self._kc = Thread(target=self._keep_connected, name="websocket_connection")
        self._kc.daemon = True
        self._kc.start()
        self.logger.info("Launched connection daemon")
        self._mb = Thread(target=self._message_broker, name="message_broker")
        self._mb.daemon = True
        self._mb.start()
        self.logger.info("Launched message broker")

    def _keep_connected(self):
        time.sleep(1)
        while True:
            try:
                self.logger.info("Opening websocket connection to {}...".format(self.url))
                self.ws = websocket.WebSocketApp(url=self.url,
                                                 on_open=self.on_open,
                                                 on_message=self.on_message)
                self.ws.run_forever()
                time.sleep(5)
            except:
                self.logger.exception("Unhandled exception")
            finally:
                self.logger.info("Connection closed")
                self.authenticated = False

    def _message_broker(self):
        time.sleep(1)
        message = None
        while True:
            try:
                message = self.pool.get()
                self.ws.send(str(message))
            except websocket.WebSocketConnectionClosedException:
                if message:
                    self.pool.put(message)
                time.sleep(10)
            except:
                logger.exception("Unhandled exception")
                if message:
                    self.pool.put(message)
                time.sleep(10)
            finally:
                self.pool.task_done()

    def on_open(self, ws):
        self.logger.info("Connection opened")

    def on_message(self, ws, message):
        if not self.authenticated:
            if "AUTH_OK" in message:
                self.logger.info("Authentication successful!")
                self.authenticated = True
            elif "AUTH" in str(message):
                self.logger.info("Got authentication request, trying authentication..")
                self.ws.send("KEY:{}".format(self.key))
            else:
                self.logger.warning("Got message from server while not authenticated")
                self.ws.close()
        else:
            self.logger.info("msg: {}".format(message))

    def on_close(self, ws, code=1000, *reason):
        self.logger.info("Connection closed (code={}, reason={})".format(code, str(reason)))

    def send(self, message):
        try:
            self.pool.put_nowait(message)
        except Full:
            self.logger.error("Queue full, message {} lost".format(message))


def run():
    logger.info("running core..")

    lm = LightManager()
    lm.run()

run()
