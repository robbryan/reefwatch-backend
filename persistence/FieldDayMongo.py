__author__ = "Paul Staszyc"
__copyright__ = "Copyright 2016, Paul Staszyc"

import tornado.concurrent

from FieldDayPersistenceBase import PersistentFieldDayBase

from bson.objectid import ObjectId
import bson.errors
import logging
logger = logging.getLogger(__name__)


class PersistentFieldDay(PersistentFieldDayBase):

    def __init__(self, mongoDbCollection):
        self.__mongoDbCollection__ = mongoDbCollection

    @tornado.concurrent.return_future
    def get(self, fieldDayId, callback, **kwargs):
        if type(fieldDayId) in [str, unicode]:
            fieldDayId = ObjectId(fieldDayId)

        mongoQuery = {"_id": fieldDayId}
        result = self.__mongoDbCollection__.find_one(mongoQuery)
        if result:
            if "_id" in result:
                result["id"] = str(result.pop("_id"))
            if "location_id" in result and result["location_id"]:
                result["location_id"] = str(result["location_id"])
        callback(result)

    @tornado.concurrent.return_future
    def update(self, fieldDayId, callback, **kwargs):
        if type(fieldDayId) == str:
            fieldDayId = ObjectId(fieldDayId)

        mongoQuery = {
            "$set": {
            }
        }

        if "description" in kwargs:
            description = kwargs["description"]
            mongoQuery["$set"]["description"] = description

        if any(mongoQuery["$set"]):
            mongoQuery["$set"]["$currentDate"] = {
                "last_modified": True
            }
            result = self.__mongoDbCollection__.find_one_and_update(
                {"_id": fieldDayId},
                mongoQuery
            )
            callback(1 if result else 0)
        else:
            raise ValueError("No field day information to set")


class PersistentFieldDayTides(PersistentFieldDayBase):

    def __init__(self, mongoDbCollection):
        self.__mongoDbCollection__ = mongoDbCollection

    @tornado.concurrent.return_future
    def get(self, fieldDayId, callback, **kwargs):
        if type(fieldDayId) in [str, unicode]:
            try:
                fieldDayId = ObjectId(fieldDayId)
            except bson.errors.InvalidId as exId:
                pass

        mongoQuery = {"_id": fieldDayId}
        result = self.__mongoDbCollection__.find_one(mongoQuery, {"tides": 1})

        callback(result["tides"] if result and "tides" in result else None)

    @tornado.concurrent.return_future
    def update(self, fieldDayId, callback, **kwargs):
        if type(fieldDayId) in [str, unicode]:
            fieldDayId = ObjectId(fieldDayId)

        mongoQuery = {
            "$set": {
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
            result = self.__mongoDbCollection__.find_one_and_update({"_id": fieldDayId}, mongoQuery)
            callback(1 if result else 0)
        else:
            raise ValueError("No tide information to set")


if __name__ == "__main__":
    pass
