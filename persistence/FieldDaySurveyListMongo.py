__author__ = "Paul Staszyc"
__copyright__ = "Copyright 2016, Paul Staszyc"

import tornado.concurrent
import pymongo.errors

from SurveyListPersistenceBase import PersistentFieldDaySurveyListBase

from bson.objectid import ObjectId
import logging
logger = logging.getLogger(__name__)


class PersistentFieldDaySurveyList(PersistentFieldDaySurveyListBase):

    def __init__(self, mongoDbCollection):
        self.__mongoDbCollection__ = mongoDbCollection

    @tornado.concurrent.return_future
    def get(self, fieldDayId, callback, limit=100, offset=0, **kwargs):
        assert(type(limit) == int)
        assert(limit > 0)
        assert(type(offset) == int)

        if type(fieldDayId) == str:
            fieldDayId = ObjectId(fieldDayId)

        """
            It would be possible to use aggregates, count and slice to do this
            but given the likely small number (upto 9) of elements expected,
            the most pragmatic way to code/debug/maintain this is with
            python array slicing
        """
        mongoQuery = {"_id": fieldDayId}
        result = self.__mongoDbCollection__.find_one(
            mongoQuery, {"surveys": 1}
        )

        if result and "surveys" in result and result["surveys"]:
            surveyList = result["surveys"]
            resultCount = len(surveyList)
            if resultCount > limit:
                surveyList = surveyList[offset:(limit+offset)]
        else:
            surveyList = None
            resultCount = 0

        callback((surveyList, resultCount))

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
