__author__ = "Paul Staszyc"
__copyright__ = "Copyright 2016, Paul Staszyc"

import tornado.concurrent
import pymongo.errors

from SiteListPersistenceBase import PersistentFieldDaySiteListBase

from bson.objectid import ObjectId
import bson.errors
import logging
logger = logging.getLogger(__name__)


class PersistentFieldDaySiteList(PersistentFieldDaySiteListBase):

    def __init__(self, mongoDbCollection):
        self.__mongoDbCollection__ = mongoDbCollection

    @tornado.concurrent.return_future
    def get(self, fieldDayId, callback, limit=100, offset=0, **kwargs):
        assert(type(limit) == int)
        assert(limit > 0)
        assert(type(offset) == int)

        if type(fieldDayId) in [str, unicode]:
            try:
                fieldDayId = ObjectId(fieldDayId)
            except bson.errors.InvalidId as exId:
                pass
        """
            It would be possible to use aggregates, count and slice to do this
            but given the likely small number of elements (upto 3) expected,
            the most pragmatic way to code/debug/maintain this is with
            python array slicing
        """
        mongoQuery = {"_id": fieldDayId}
        result = self.__mongoDbCollection__.find_one(
            mongoQuery
        )

        if result and "sites" in result and type(result["sites"]) == list:
            siteList = result["sites"]
            resultCount = len(siteList)
            if resultCount > limit:
                siteList = siteList[offset:(limit+offset)]
        else:
            siteList = None
            resultCount = 0

        callback((siteList, resultCount))

    @tornado.concurrent.return_future
    def add(self, callback, fieldDayId, siteCode, **kwargs):
        if type(fieldDayId) in [str, unicode]:
            try:
                fieldDayId = ObjectId(fieldDayId)
            except bson.errors.InvalidId as exId:
                pass

        result = self.__mongoDbCollection__.find_one_and_update(
            {"_id": fieldDayId, "sites.site_code": {"$nin": [siteCode]}},
            {"$push": {"sites": {"site_code": siteCode}}}
        )
        callback(1 if result else 0)


if __name__ == "__main__":
    pass
