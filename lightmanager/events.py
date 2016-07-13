"""
Event subsystem of the lighting system

Author: Leonard de Vries
Created: 13-07-2016
"""
import random
import logging
import threading
import time

import datetime

import common.log

logger = logging.getLogger(__name__)


class EventListener:
    def __init__(self, callback):
        self.event_sources = list()
        self.callback = callback

    def register_event_source(self, source):
        self.event_sources.append(source(self.callback))


class Event:
    def __init__(self, name, value, **kwargs):
        self.name = name
        self.value = value
        self.timestamp = datetime.datetime.now()

    def __repr__(self):
        return "<Event {} ({}) @ {}>".format(self.name, self.value, self.timestamp)

    __str__ = __repr__


class DummyEventSource:
    def __init__(self, callback):
        self.possible_events = ['motion', 'presence', 'light_intensity']
        self.callback = callback
        self.event_generator_thread = threading.Thread(target=self.event_generator, name="dummy-event")
        self.event_generator_thread.daemon = True
        self.event_generator_thread.start()

    def event_generator(self):
        while True:
            choice = random.choice(self.possible_events)
            delay = random.randrange(1, 20)
            logger.debug("I chose to fire event '{}' after {} seconds".format(choice, delay))
            time.sleep(delay)
            self.callback(Event(name=choice, value=random.randint(1000, 9999)))

