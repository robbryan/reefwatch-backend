__author__ = "Paul Staszyc"
__copyright__ = "Copyright 2016, Paul Staszyc"

import tornado.concurrent

import logging
logger = logging.getLogger(__name__)


class PersistentFieldDayBase(object):

    def __init__(self):
        logger.warning("Abstract class created")
        pass

    @tornado.concurrent.return_future
    def get(self, fieldDayId, callback):
        raise NotImplementedError

    @tornado.concurrent.return_future
    def update(self, fieldDayId, callback):
        raise NotImplementedError


if __name__ == "__main__":
    pass
