__author__ = "Paul Staszyc"
__copyright__ = "Copyright 2016, Paul Staszyc"

import tornado.concurrent
import pymongo.errors

from persistence.LocationListPersistenceBase import PersistentLocationListBase

import logging
logger = logging.getLogger(__name__)


class PersistentLocationList(PersistentLocationListBase):

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
            if "description" in query:
                mongoQuery["description"] = {"regex": r"(?i){0}".format(query["description"])}

        """
        BEWARE!
        skip() and limit() are costly for large data sets. Beware
        See https://docs.mongodb.org/manual/reference/method/cursor.skip/#cursor.skip for more
        """
        locationCursor = self.__mongoDbCollection__.find(
            mongoQuery,
            {
                "location_code": 1,
                "description": 1
            }
        ).skip(((offset)*limit) if offset > 0 else 0).limit(limit)
        resultList = list()
        for result in locationCursor:
            reefwatchLocation = result
            # Replace ObjectId with string its representation
            reefwatchLocation["id"] = str(reefwatchLocation.pop("_id"))

            resultList.append(reefwatchLocation)

        callback((resultList, self.__mongoDbCollection__.count()))

    @tornado.concurrent.return_future
    def add(self, callback, fieldDay):
        try:
            result = self.__mongoDbCollection__.insert_one(fieldDay)
        except pymongo.errors.DuplicateKeyError as exDupKey:
            raise ValueError(
                "The Field Day with ID '{id}' already exists".format(
                    id=fieldDay["_id"]
                )
            )

        callback(str(result.inserted_id))


if __name__ == "__main__":
    pass
