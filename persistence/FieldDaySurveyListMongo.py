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
    def get(self, fieldDayId, siteCode, callback, limit=100, offset=0, **kwargs):
        assert(type(limit) == int)
        assert(limit > 0)
        assert(type(offset) == int)

        if type(fieldDayId) in [str, unicode]:
            fieldDayId = ObjectId(fieldDayId)

        mongoQuery = {"_id": fieldDayId, "sites.site_code": siteCode}
        result = self.__mongoDbCollection__.find_one(
            mongoQuery, {"sites": 1}
        )

        surveyList = None
        resultCount = 0
        if result and "sites" in result and type(result["sites"]) == list:
            site = filter(lambda x: x["site_code"] == siteCode, result["sites"])[0]
            if "surveys" in site and type(site["surveys"]) == list:
                surveyList = site["surveys"][offset:(limit+offset)]
                resultCount = len(site["surveys"])

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
