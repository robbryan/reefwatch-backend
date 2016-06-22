"""
    This is the Request handler for Field Day Sites - List, add, get, update
"""

__author__    = "Paul Staszyc"
__copyright__ = "Copyright 2016"

from tornado.gen import coroutine
import tornado.web
from baseHandler import BaseHandler, BaseEntityListHandler

from datetime import datetime
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logger.getEffectiveLevel())


class FieldDaySiteListHandler(BaseEntityListHandler):

    def initialize(
        self,
        persistentFieldDaySiteListObj,
        persistentLocationEntityObj,
        persistentFieldDayEntityObj
    ):
        self.__persistentFieldDaySiteListObj__ = persistentFieldDaySiteListObj
        self.__persistentLocationEntityObj__ = persistentLocationEntityObj
        self.__persistentFieldDayEntityObj__ = persistentFieldDayEntityObj

    def options(self, *args):
        allowedMethods = list(["OPTIONS", "GET"])
        try:
            user = self.get_current_user()
            if user and any(user):
                allowedMethods.append("POST")
        except Exception as ex:
            logger.error(ex)

        self.set_header("Access-Control-Allow-Methods", ",".join(allowedMethods))
        self.addAccessHeaders()
        self.finish()

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
        entityListGetter = self.__persistentFieldDaySiteListObj__
        try:
            fieldDaySiteList, totalRecordCount = yield entityListGetter.get(
                fieldDayId=fieldDayId,
                limit=limit,
                offset=offset
                )
            if not fieldDaySiteList:
                raise KeyError("There are no Sites for the Field Day you have requested")
        except KeyError as exNotFound:
            errorMessage = exNotFound
            self.set_status(404)
            self.add_header("error", "{0}".format(errorMessage))
            self.finish({"message": "{0}".format(errorMessage)})
            return
        except Exception as ex:
            logger.error("{0}".format(ex))
            errorMessage = "An error occured while attempting to retireve the requested Field Day Site"
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

    @tornado.web.authenticated
    @coroutine
    def post(self, fieldDayId):
        try:
            siteCode = self.get_body_argument("site_code")
        except (ValueError, tornado.web.MissingArgumentError) as exArgument:
            errorMessage = exArgument
            self.set_status(400)
            self.add_header("error", "{0}".format(errorMessage))
            self.finish({"message": "{0}".format(errorMessage)})
            return

        # Check that site code is valid for Field Day Location
        fieldDayGetter = self.__persistentFieldDayEntityObj__
        try:
            fieldDayEntity = yield fieldDayGetter.get(
                fieldDayId=fieldDayId
            )
            if not fieldDayEntity:
                raise KeyError("Unable to add Site to Field Day. Field Day not found")

            locationGetter = self.__persistentLocationEntityObj__
            locationEntity = yield locationGetter.get(
                locationId=fieldDayEntity["location_id"]
            )
            if siteCode not in [site["site_code"] for site in locationEntity["sites"]]:
                raise KeyError(
                    "Unable to add Site to Field Day. The Site ({site}) is not valid for the location ({loc})".format(
                        site=siteCode,
                        loc=locationEntity["description"] if "description" in locationEntity else locationEntity["id"]
                    )
                )
            siteSetter = self.__persistentFieldDaySiteListObj__
            updateCount = yield siteSetter.add(
                fieldDayId=fieldDayId,
                siteCode=siteCode
            )
            print "Update Count: {}".format(updateCount)
            if updateCount <= 0:
                raise Exception("Zero Field Days were updated")
        except KeyError as exNotFound:
            errorMessage = exNotFound
            self.set_status(404)
            self.add_header("error", "{0}".format(errorMessage))
            self.finish({"message": "{0}".format(errorMessage)})
            return
        except Exception as ex:
            logger.error("{0}".format(ex))
            errorMessage = "An error occured while attempting to add the Site"
            self.set_status(500)
            self.add_header(
                "error", "{0}".format(
                    errorMessage
                )
            )
            self.finish({"message": "{0}".format(errorMessage)})
            return

        self.set_status(201)
        self.setResponseHeadersNewEntity(siteCode)
        self.addAccessHeaders()
        self.finish(
            {"message": "New Site ({0}) successfully created for Field Day".format(siteCode)}
        )


class FieldDaySiteHandler(BaseHandler):

    def initialize(self, persistentFieldDaySiteEntityObj):
        self.__persistentEntityObj__ = persistentFieldDaySiteEntityObj

    def options(self, *args):
        allowedMethods = list(["OPTIONS", "GET"])
        self.set_header("Access-Control-Allow-Methods", ",".join(allowedMethods))
        self.finish()

    @coroutine
    def get(self, fieldDayId, siteCode):
        entityGetter = self.__persistentEntityObj__
        try:
            fieldDaySiteEntity = yield entityGetter.get(fieldDayId=fieldDayId, siteCode=siteCode)
            if (not fieldDaySiteEntity or not any(fieldDaySiteEntity)):
                raise KeyError("The Site for Field Day you have requested do not exist")
        except KeyError as exNotFound:
            errorMessage = exNotFound
            self.set_status(404)
            self.add_header("error", "{0}".format(errorMessage))
            self.finish({"message": "{0}".format(errorMessage)})
            return
        except Exception as ex:
            logger.error("{0}".format(ex))
            errorMessage = "An error occured while attempting to retireve the requested Field Day Site"
            self.set_status(500)
            self.add_header(
                "error", "{0}".format(
                    errorMessage
                )
            )
            self.finish({"message": "{0}".format(errorMessage)})
            return
        else:
            self.finish(fieldDaySiteEntity)


if __name__ == "__main__":
    pass
