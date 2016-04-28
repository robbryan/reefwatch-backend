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

        callback(result)


if __name__ == "__main__":
    pass
