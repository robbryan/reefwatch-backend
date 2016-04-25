__author__ = "Paul Staszyc"
__copyright__ = "Copyright 2016, Paul Staszyc"

import tornado.concurrent

from FieldDayListPersistenceBase import PersistentFieldDayListBase

import logging
logger = logging.getLogger(__name__)


class PersistentFieldDayList(PersistentFieldDayListBase):

    def __init__(self, mongoDbCollection):
        self.__mongoDbCollection__ = mongoDbCollection

    @tornado.concurrent.return_future
    def get(self, callback, limit=100, offset=0, **kwargs):
        assert(type(limit) == int)
        assert(limit > 0)
        assert(type(offset) == int)
        mongoQuery = {}
        if "query" in kwargs:
            mongoQuery = {}
            logger.info("Query: {0}".format(kwargs["query"]))
            query = kwargs["query"]
            if "location_id" in query:
                mongoQuery["location_id"] = query["location_id"]
            if "survey_type" in query:
                mongoQuery["sites.surveys.survey_type"] = query["survey_type"]

        """
        BEWARE!
        skip() and limit() are costly for large data sets. Beware
        See https://docs.mongodb.org/manual/reference/method/cursor.skip/#cursor.skip for more
        """
        fieldDayCursor = self.__mongoDbCollection__.find(mongoQuery).skip(((offset)*limit) if offset > 0 else 0).limit(limit)
        resultList = list()
        for result in fieldDayCursor:
            fieldDay = result
            # do transformations on fieldDay
            resultList.append(fieldDay)

        callback((resultList, self.__mongoDbCollection__.count()))

    @tornado.concurrent.return_future
    def add(self, callback, fieldDay):
        result = self.__mongoDbCollection__.insert_one(fieldDay)
        callback(str(result))


if __name__ == "__main__":
    pass
