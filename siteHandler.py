"""
    This is the Request handler for Sites
"""

__author__    = "Paul Staszyc"
__copyright__ = "Copyright 2016"

from tornado.gen import coroutine

from baseHandler import BaseEntityListHandler

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logger.getEffectiveLevel())

class SiteListHandler(BaseEntityListHandler):

    def initialize(self, persistentEntityListObj):
        self.__persistentEntityListObj__ = persistentEntityListObj

    def get(self, location=None):
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
        entityList, totalRecordCount = entityListGetter.get(
            limit=limit,
            offset=offset
            )
        self.setResponseHeadersList(
            pageNum=pageNum,
            pageSize=pageSize,
            totalRecordCount=totalRecordCount
        )
        self.write({"data": entityList})


class FieldDaySiteListHandler(BaseEntityListHandler):

    def initialize(self, persistentFieldDaySiteListObj):
        self.__persistentEntityListObj__ = persistentFieldDaySiteListObj

    @coroutine
    def get(self, fieldDayId):
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
        try:
            fieldDaySiteList, totalRecordCount = yield entityListGetter.get(
                fieldDayId=fieldDayId,
                limit=limit,
                offset=offset
            )
            if fieldDaySiteList is None:
                raise KeyError("Sites have not been recorded for this Field Day")
        except KeyError as exNotFound:
            errorMessage = exNotFound
            self.set_status(404)
            self.add_header("error", "{0}".format(errorMessage))
            self.finish({"message": "{0}".format(errorMessage)})
            return
        except Exception as ex:
            logger.error("{0}".format(ex))
            errorMessage = "An error occured while attempting to retireve the Sites for a Field Day"
            self.set_status(500)
            self.add_header(
                "error", "{0}".format(
                    errorMessage
                )
            )
            self.finish({"message": "{0}".format(errorMessage)})
            return

        self.setResponseHeadersList(
            pageNum=pageNum,
            pageSize=pageSize,
            totalRecordCount=totalRecordCount
        )
        self.finish({"data": fieldDaySiteList})


if __name__ == "__main__":
    pass
