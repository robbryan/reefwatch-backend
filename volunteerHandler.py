"""
    This is the Request handler for Volunteers - List, add, get, update
"""

__author__    = "Paul Staszyc"
__copyright__ = "Copyright 2016"

from tornado.gen import coroutine

from baseHandler import BaseEntityListHandler

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logger.getEffectiveLevel())


class VolunteerListHandler(BaseEntityListHandler):

    def initialize(self, persistentEntityListObj):
        self.__persistentEntityListObj__ = persistentEntityListObj

    def options(self, *args):
        allowedMethods = list(["OPTIONS", "GET"])

        self.set_header("Access-Control-Allow-Methods", ",".join(allowedMethods))
        self.finish()

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
        volunteerListGetter = self.__persistentEntityListObj__
        try:
            volunteerList, totalRecordCount = yield volunteerListGetter.get(
                limit=limit,
                offset=offset
                )
        except Exception as ex:
            logger.error("{0}".format(ex))
            errorMessage = "An error occured while attempting to retireve Volunteers"
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
        self.finish({"data": volunteerList})


if __name__ == "__main__":
    pass
