__author__ = "Paul Staszyc"
__copyright__ = "Copyright 2016, Paul Staszyc"

import logging
logger = logging.getLogger(__name__)


class PersistentSurveyTypeListBase(object):

    def __init__(self):
        logger.warning("Abstract class created")
        pass

    def add(self):
        raise NotImplementedError

    def get(self):
        raise NotImplementedError


class PersistentFieldDaySurveyListBase(object):

    def __init__(self):
        logger.warning("Abstract class created")
        pass

    def add(self):
        raise NotImplementedError

    def get(self):
        raise NotImplementedError


class PersistentSurveyTypeListDummy(PersistentSurveyTypeListBase):

    def __init__(self):
        pass

    def get(self, limit=100, offset=0, **kwargs):
        logger.info("Limit: {0}\tOffset: {1}".format(limit, offset))
        if "query" in kwargs:
            logger.info("Query: {0}".format(kwargs["query"]))
            query = kwargs["query"]

        dummyResult = [
            {
                "id": 1000,
                "description": "Survey 1000"
            },
            {
                "id": 2000,
                "description": "Survey 2000"
            },
            {
                "id": 3000,
                "description": "Survey 3000"
            }
        ]

        return dummyResult


if __name__ == "__main__":
    pass
