__author__ = "Paul Staszyc"
__copyright__ = "Copyright 2016, Paul Staszyc"

import tornado.concurrent
from bson.objectid import ObjectId
import bson.errors


import logging
logger = logging.getLogger(__name__)


class PersistentLocation(object):

    def __init__(self, mongoDbCollection):
        self.__mongoDbCollection__ = mongoDbCollection

    @tornado.concurrent.return_future
    def get(self, locationId, callback, **kwargs):
        if type(locationId) in [str, unicode]:
            try:
                locationId = ObjectId(locationId)
            except bson.errors.InvalidId as exId:
                pass

        mongoQuery = {"_id": locationId}
        result = self.__mongoDbCollection__.find_one(mongoQuery)
        if result:
            if "_id" in result:
                result["id"] = str(result.pop("_id"))

        callback(result)


if __name__ == "__main__":
    pass
