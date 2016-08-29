__author__ = "Paul Staszyc"
__copyright__ = "Copyright 2016, Paul Staszyc"

import tornado.concurrent

from bson.objectid import ObjectId
import logging
logger = logging.getLogger(__name__)


class PersistentFieldDaySite(object):

    def __init__(self, mongoDbCollection):
        self.__mongoDbCollection__ = mongoDbCollection

    @tornado.concurrent.return_future
    def get(self, fieldDayId, siteCode, callback, **kwargs):

        if type(fieldDayId) in [str, unicode]:
            fieldDayId = ObjectId(fieldDayId)

        mongoQuery = {"_id": fieldDayId, "sites.site_code": siteCode}
        result = self.__mongoDbCollection__.find_one(
            mongoQuery
        )

        if result:
            fieldDaySite = filter(lambda x: x["site_code"] == siteCode, result["sites"])[0]
            callback(fieldDaySite)
        else:
            callback(None)

    @tornado.concurrent.return_future
    def update(self, fieldDayId, siteCode, callback, **kwargs):
        if type(fieldDayId) in [str, unicode]:
            fieldDayId = ObjectId(fieldDayId)

        mongoSelector = {"_id": fieldDayId, "sites.site_code": siteCode}
        mongoUpdates = {
            "$set": {}
        }
        if "observations" in kwargs:
            mongoUpdates["$set"] = {"sites.$.observations": kwargs["observations"]}

        if any(mongoUpdates["$set"]):
            logger.debug(mongoUpdates)
            mongoUpdates["$set"]["$currentDate"] = {
                "last_modified": True
            }
            result = self.__mongoDbCollection__.find_one_and_update(
                mongoSelector,
                mongoUpdates
            )
            callback(1 if result else 0)
        else:
            raise ValueError("No field day observation information to set")


if __name__ == "__main__":
    pass
