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
        if "query" in kwargs:
            logger.info("Query: {0}".format(kwargs["query"]))
            query = kwargs["query"]

        dummyResult = [
            {
                "id": "1000",
                "description": "Aldinga North"
            },
            {
                "id": "2000",
                "description": "Aldinga South"
            },
            {
                "id": "3000",
                "description": "Lady Bay North"
            },
            {
                "id": "4000",
                "description": "Lady Bay South"
            },
            {
                "id": "5000",
                "description": "Hallett Cove"
            },
            {
                "id": "6000",
                "description": "Victor Harbor"
            },
            {
                "id": "7000",
                "description": "Beachport"
            },
            {
                "id": "8000",
                "description": "Robe"
            },
            {
                "id": "9000",
                "description": "Port Macdonnell"
            }
        ]

        return dummyResult


if __name__ == "__main__":
    pass
