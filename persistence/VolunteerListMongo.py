__author__ = "Paul Staszyc"
__copyright__ = "Copyright 2016, Paul Staszyc"

import tornado.concurrent
from baseHandler import BaseEntityListHandler
from datetime import datetime
import pymongo.errors
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class PersistentVolunteerList(BaseEntityListHandler):

    def __init__(self, mongoDbCollection):
        self.__mongoDbCollection__ = mongoDbCollection

    @tornado.concurrent.return_future
    def get(self, callback, limit=100, offset=0):
        assert(type(limit) == int)
        assert(limit > 0)
        assert(type(offset) == int)

        volunteerList = self.__mongoDbCollection__.distinct("sites.observations.volunteers")[offset:(limit+offset)]

        callback((volunteerList, self.__mongoDbCollection__.count()))


if __name__ == "__main__":
    pass
