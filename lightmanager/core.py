"""
Core module of the lighting system

The core module loads all dependant modules and runs the whole package.

Author: Leonard de Vries
Created: 12-07-2016
"""
import logging
import common.log


def run():
    common.log.setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("running core..")
