import logging
import logging.handlers
import os
from os.path import expanduser
import sys


def setup_logging():
    try:
        # Set up a specific logger with our desired output level
        home_dir = expanduser("~")
        logfile = os.path.join(home_dir, "log", "lightmanager.log")
        if not os.path.isdir(os.path.dirname(logfile)):
            os.mkdir(os.path.dirname(logfile))
        if not os.path.isfile(logfile):
            with open(logfile, 'w'):
                pass

        # Initiate root logger
        logger = logging.root
        logger.setLevel(logging.DEBUG)

        logger.handlers = []
        # Add the log message handler to the logger
        handler = logging.handlers.RotatingFileHandler(logfile, maxBytes=10 * 1024 * 1024, backupCount=5)  # 10MB
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s [%(name)s][%(threadName)s] -> %(message)s"))

        handler2 = logging.StreamHandler(stream=sys.stdout)
        handler2.setFormatter(logging.Formatter(
            "%(asctime)s %(levelname)s [%(name)s][%(threadName)s] -> %(message)s"))

        logger.addHandler(handler)
        logger.addHandler(handler2)
        return True
    except:
        print("Unable to initialize logging properly, see traceback")
        raise
