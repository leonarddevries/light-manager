"""
Core module of the lighting system

The core module loads all dependent modules and runs the whole package.

Author: Leonard de Vries
Created: 12-07-2016
"""
import logging
import common.log
import events
import time

common.log.setup_logging()
logger = logging.getLogger(__name__)


class LightManager:
    def __init__(self):
        self.events = events.EventListener(callback=self.event_callback)
        self.events.register_event_source(events.DummyEventSource)

    def event_callback(self, event):
        logger.info("Got event: {}".format(event))

    def run(self):
        while True:
            time.sleep(10)


def run():
    logger.info("running core..")

    lm = LightManager()
    lm.run()

run()
