"""
    This is the Request handler for Field Days - List, add, get, update
"""

__author__    = "Paul Staszyc"
__copyright__ = "Copyright 2016"

from tornado.gen import coroutine
from baseHandler import BaseHandler, BaseEntityListHandler

import logging
logger = logging.getLogger(__name__)


class FieldDayListHandler(BaseEntityListHandler):

    def initialize(self, persistentEntityListObj):
        self.__persistentEntityListObj__ = persistentEntityListObj

    @coroutine
    def get(self):
        try:
            pageSize, pageNum = self.getPageSizeAndNum()
        except ValueError as exPage:
            self.set_status(400)
            self.add_header("error", "{0}".format(exPage))
            self.finish({"message": "{0}".format(exPage)})
            return

        offset = (pageNum-1)*pageSize
        limit = pageSize
        entityListGetter = self.__persistentEntityListObj__
        fieldDayList, totalRecordCount = yield entityListGetter.get(
            limit=limit,
            offset=offset
            )
        self.setResponseHeaders(
            pageNum=pageNum,
            pageSize=pageSize,
            totalRecordCount=totalRecordCount
        )
        self.finish({"data": fieldDayList})


class FieldDayHandler(BaseHandler):

    def initialize(self, persistentEntityObj):
        self.__persistentEntityObj__ = persistentEntityObj

    @coroutine
    def get(self, fieldDayId):
        entityGetter = self.__persistentEntityObj__
        try:
            fieldDayEntity = yield entityGetter.get(fieldDayId=fieldDayId)
            logger.info(fieldDayEntity)
            if not (fieldDayEntity or any(fieldDayEntity)):
                raise KeyError("The Field Day you have requested does not exist")
        except KeyError as exNotFound:
            errorMessage = exNotFound
            self.set_status(404)
            self.add_header("error", "{0}".format(errorMessage))
            self.finish({"message": "{0}".format(errorMessage)})
            return
        except Exception as ex:
            logger.error("{0}".format(ex))
            errorMessage = "An error occured while attempting to retireve the requested Field Day"
            self.set_status(500)
            self.add_header(
                "error", "{0}".format(
                    errorMessage
                )
            )
            self.finish({"message": "{0}".format(errorMessage)})
            return
        else:
            self.finish(fieldDayEntity)

if __name__ == "__main__":
    pass
