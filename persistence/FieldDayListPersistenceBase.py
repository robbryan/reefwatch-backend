__author__ = "Paul Staszyc"
__copyright__ = "Copyright 2016, Paul Staszyc"

import logging
logger = logging.getLogger(__name__)


class PersistentFieldDayLocationListBase(object):

    def __init__(self):
        logger.warning("Abstract class created")
        pass

    def add(self):
        raise NotImplementedError

    def get(self):
        raise NotImplementedError


class PersistentFieldDayListDummy(PersistentFieldDayListBase):

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
                "date": "2015-03-05",
                "description": "Aldinga North - March 2015",
                "location_id": "1000",
                "leader_id" : "1000",
                "sites": []
            },
            {
                "id": "1100",
                "date": "2015-03-05",
                "description": "Aldinga South - March 2015",
                "location_id": "2000",
                "leader_id" : "1000",
                "sites": []
            },
            {
                "id": "1200",
                "date": "2015-10-12",
                "description": "Lady Bay North - October 2015",
                "location_id": "3000",
                "leader_id" : "1000",
                "sites": []
            },
            {
                "id": "1300",
                "date": "2015-12-03",
                "description": "Lady Bay South - December 2015",
                "location_id": "4000",
                "leader_id" : "1000",
                "sites": []
            }
        ]

        return (dummyResult[offset:(limit+offset)], len(dummyResult))


if __name__ == "__main__":
    pass
