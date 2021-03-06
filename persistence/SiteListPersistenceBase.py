__author__ = "Paul Staszyc"
__copyright__ = "Copyright 2016, Paul Staszyc"

import logging
logger = logging.getLogger(__name__)


class PersistentSiteListBase(object):

    def __init__(self):
        logger.warning("Abstract class created")
        pass

    def add(self):
        raise NotImplementedError

    def get(self):
        raise NotImplementedError


class PersistentFieldDaySiteListBase(object):

    def __init__(self):
        logger.warning("Abstract class created")
        pass

    def add(self):
        raise NotImplementedError

    def get(self):
        raise NotImplementedError


class PersistentSiteListDummy(PersistentSiteListBase):

    def __init__(self):
        pass

    def get(self, limit=100, offset=0, **kwargs):
        assert(type(limit) == int)
        assert(limit > 0)
        assert(type(offset) == int)
        logger.info("Limit: {0}\tOffset: {1}".format(limit, offset))
        if "query" in kwargs:
            logger.info("Query: {0}".format(kwargs["query"]))
            query = kwargs["query"]
            
        if "location" in kwargs:
            location = kwargs["location"]
        else:
            location = ""

        dummyResult = [
            {
                "id": 1000,
                "description": "Upper",
                "site_code": "{l}{s}".format(l=location,s="U"),
                "latitude": None,
                "longitude": None
            },
            {
                "id": 2000,
                "description": "Middle",
                "site_code": "{l}{s}".format(l=location,s="M"),
                "latitude": None,
                "longitude": None
            },
            {
                "id": 3000,
                "description": "Lower",
                "site_code": "{l}{s}".format(l=location,s="L"),
                "latitude": None,
                "longitude": None
            }
        ]

        return (dummyResult[offset:(limit+offset)], len(dummyResult))


if __name__ == "__main__":
    pass
