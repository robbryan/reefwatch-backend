__author__ = "Paul Staszyc"
__copyright__ = "Copyright 2016, Paul Staszyc"

import tornado.concurrent

import logging
logger = logging.getLogger(__name__)


class PersistentLocationDummy(object):

    def __init__(self):
        logger.warning("Location Dummy class created")
        pass

    @tornado.concurrent.return_future
    def get(self, locationId, callback):
        dummyResult = {
                "id": "1000",
                "description": "Aldinga North",
                "location_code": "AN"
            }

        callback(dummyResult)
