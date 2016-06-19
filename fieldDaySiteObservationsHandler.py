"""
    This is the Request handler for Field Day Site Observations - get and update
"""

__author__    = "Paul Staszyc"
__copyright__ = "Copyright 2016"

from tornado.gen import coroutine
import tornado.web
from baseHandler import BaseHandler

from datetime import datetime
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logger.getEffectiveLevel())


class FieldDaySiteObservationsHandler(BaseHandler):

    def initialize(self, persistentFieldDaySiteEntityObj):
        self.__persistentEntityObj__ = persistentFieldDaySiteEntityObj

    def options(self, *args):
        allowedMethods = list(["OPTIONS", "GET"])
        self.set_header("Access-Control-Allow-Methods", ",".join(allowedMethods))
        self.finish()

    @coroutine
    def get(self, fieldDayId, siteCode):
        entityGetter = self.__persistentEntityObj__
        fieldDaySiteObservationsEntity = {}
        try:
            fieldDaySiteEntity = yield entityGetter.get(fieldDayId=fieldDayId, siteCode=siteCode)
            if (not fieldDaySiteEntity or not any(fieldDaySiteEntity)):
                raise KeyError("The Site for Field Day you have requested do not exist")
            elif "observations" in fieldDaySiteEntity:
                fieldDaySiteObservationsEntity = fieldDaySiteEntity["observations"] 
        except KeyError as exNotFound:
            errorMessage = exNotFound
            self.set_status(404)
            self.add_header("error", "{0}".format(errorMessage))
            self.finish({"message": "{0}".format(errorMessage)})
            return
        except Exception as ex:
            logger.error("{0}".format(ex))
            errorMessage = "An error occured while attempting to retireve the requested Field Day Site Observations"
            self.set_status(500)
            self.add_header(
                "error", "{0}".format(
                    errorMessage
                )
            )
            self.finish({"message": "{0}".format(errorMessage)})
            return
        else:
            self.finish(fieldDaySiteObservationsEntity)


if __name__ == "__main__":
    pass
