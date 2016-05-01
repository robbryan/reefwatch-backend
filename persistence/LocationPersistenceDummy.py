__author__ = "Paul Staszyc"
__copyright__ = "Copyright 2016, Paul Staszyc"

import tornado.concurrent

import logging
logger = logging.getLogger(__name__)


class PersistentLocationDummy(object):

    __dummy_list__ = {
            "1000": {
                "id": "1000",
                "description": "Aldinga North",
                "location_code": "AN"
            },
            "2000": {
                "id": "2000",
                "description": "Aldinga South",
                "location_code": "AS"
            },
            "3000": {
                "id": "3000",
                "description": "Lady Bay North",
                "location_code": "LBN"
            },
            "4000": {
                "id": "4000",
                "description": "Lady Bay South",
                "location_code": "LBS"
            },
            "5000": {
                "id": "5000",
                "description": "Hallett Cove",
                "location_code": "HC"
            },
            "6000": {
                "id": "6000",
                "description": "Victor Harbor",
                "location_code": "YB"
            },
            "7000": {
                "id": "7000",
                "description": "Beachport",
                "location_code": "B"
            },
            "8000": {
                "id": "8000",
                "description": "Robe",
                "location_code": "R"
            },
            "9000": {
                "id": "9000",
                "description": "Port Macdonnell",
                "location_code": "PM"
            }
    }

    def __init__(self):
        logger.warning("Location Dummy class created")
        pass

    @tornado.concurrent.return_future
    def get(self, locationId, callback):
        if locationId in PersistentLocationDummy.__dummy_list__:
            callback(PersistentLocationDummy.__dummy_list__[locationId])
        else:
            callback({})
