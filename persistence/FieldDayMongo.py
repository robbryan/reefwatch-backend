__author__ = "Paul Staszyc"
__copyright__ = "Copyright 2016, Paul Staszyc"

import tornado.concurrent

from FieldDayPersistenceBase import PersistentFieldDayBase

from bson.objectid import ObjectId
import logging
logger = logging.getLogger(__name__)


class PersistentFieldDay(PersistentFieldDayBase):

    def __init__(self, mongoDbCollection):
        self.__mongoDbCollection__ = mongoDbCollection

    @tornado.concurrent.return_future
    def get(self, fieldDayId, callback, **kwargs):
        if type(fieldDayId) == str:
            fieldDayId = ObjectId(fieldDayId)

        mongoQuery = {"_id": fieldDayId}
        result = self.__mongoDbCollection__.find_one(mongoQuery)
        if result and "_id" in result:
            result["id"] = str(result.pop("_id"))
        callback(result)

    @tornado.concurrent.return_future
    def update(self, fieldDayId, callback, **kwargs):
        if type(fieldDayId) == str:
            fieldDayId = ObjectId(fieldDayId)

        mongoQuery = {
            "$set": {
                "$currentDate": {
                    "last_modified": True
                }
            }
        }
        result = self.__mongoDbCollection__.update_one({"_id": fieldDayId}, mongoQuery)
        callback(result.modified_count)


class PersistentFieldTidesDay(PersistentFieldDayBase):

    def __init__(self, mongoDbCollection):
        self.__mongoDbCollection__ = mongoDbCollection

    @tornado.concurrent.return_future
    def get(self, fieldDayId, callback, **kwargs):
        if type(fieldDayId) == str:
            fieldDayId = ObjectId(fieldDayId)

        mongoQuery = {"_id": fieldDayId}
        result = self.__mongoDbCollection__.find_one(mongoQuery, {"tides": 1})

        callback(result["tides"] if "tides" in result else None)

    @tornado.concurrent.return_future
    def update(self, fieldDayId, callback, **kwargs):
        if type(fieldDayId) == str:
            fieldDayId = ObjectId(fieldDayId)

        mongoQuery = {
            "$set": {
            },
            "$currentDate": {
                "last_modified": True
            }
        }

        if "tides" in kwargs:
            tides = kwargs["tides"]
            mongoQuery["$set"]["tides"] = tides
        else:
            if "high" in kwargs:
                mongoQuery["$set"]["tides.high"] = kwargs["high"]
            if "low" in kwargs:
                mongoQuery["$set"]["tides.low"] = kwargs["low"]

        if any(mongoQuery["$set"]):
            result = self.__mongoDbCollection__.update_one({"_id": fieldDayId}, mongoQuery)
            callback(result.modified_count)
        else:
            raise ValueError("No tide information to set")

if __name__ == "__main__":
    pass
