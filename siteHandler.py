"""
    This is the Request handler for Sites
"""

__author__    = "Paul Staszyc"
__copyright__ = "Copyright 2016"

from tornado.gen import coroutine

from baseHandler import BaseEntityListHandler, BaseHandler

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logger.getEffectiveLevel())


class SiteListHandler(BaseEntityListHandler):

    def initialize(self, persistentEntityListObj):
        self.__persistentEntityListObj__ = persistentEntityListObj

    def options(self, *args):
        allowedMethods = list(["OPTIONS", "GET"])
        try:
            user = self.get_current_user()
            if user and any(user):
                pass #allowedMethods.extend(["POST"]) # PUT and DELETE to follow
        except Exception as ex:
            logger.error(ex)

        self.set_header("Access-Control-Allow-Methods", ",".join(allowedMethods))
        self.finish()

    @coroutine
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
        try:
            entityList, totalRecordCount = yield entityListGetter.get(
                locationId=location,
                limit=limit,
                offset=offset
                )
            if entityList is None:
                raise KeyError("Sites have not been recorded for this Location")
        except KeyError as exNotFound:
            errorMessage = exNotFound
            self.set_status(404)
            self.add_header("error", "{0}".format(errorMessage))
            self.finish({"message": "{0}".format(errorMessage)})
            return
        except Exception as ex:
            logger.error("{0}".format(ex))
            errorMessage = "An error occured while attempting to retireve the Sites for this Location: {}".format(location)
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
        self.finish({"data": entityList})


if __name__ == "__main__":
    pass
