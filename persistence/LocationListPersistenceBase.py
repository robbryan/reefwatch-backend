__author__ = "Paul Staszyc"
__copyright__ = "Copyright 2016, Paul Staszyc"

import logging
logger = logging.getLogger(__name__)


class PersistentLocationListBase(object):

    def __init__(self):
        logger.warning("Abstract class created")
        pass

    def add(self):
        raise NotImplementedError

    def get(self):
        raise NotImplementedError


class PersistentLocationListDummy(PersistentLocationListBase):

    def __init__(self):
        pass

    def get(self, limit=100, offset=0, **kwargs):
        logger.info("Limit: {0}\tOffset: {1}".format(limit, offset))
        assert(type(limit) == int)
        assert(limit > 0)
        assert(type(offset) == int)
        if "query" in kwargs:
            logger.info("Query: {0}".format(kwargs["query"]))
            query = kwargs["query"]

        dummyResult = [
            {
                "id": "1000",
                "description": "Aldinga North",
                "location_code": "AN"
            },
            {
                "id": "2000",
                "description": "Aldinga South",
                "location_code": "AS"
            },
            {
                "id": "3000",
                "description": "Lady Bay North",
                "location_code": "LBN"
            },
            {
                "id": "4000",
                "description": "Lady Bay South",
                "location_code": "LBS"
            },
            {
                "id": "5000",
                "description": "Hallett Cove",
                "location_code": "HC"
            },
            {
                "id": "6000",
                "description": "Victor Harbor",
                "location_code": "YB"
            },
            {
                "id": "7000",
                "description": "Beachport",
                "location_code": "B"
            },
            {
                "id": "8000",
                "description": "Robe",
                "location_code": "R"
            },
            {
                "id": "9000",
                "description": "Port Macdonnell",
                "location_code": "PM"
            }
        ]

        return (dummyResult[offset:(limit+offset)], len(dummyResult))


if __name__ == "__main__":
    pass
