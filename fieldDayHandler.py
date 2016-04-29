"""
    This is the Request handler for Field Days - List, add, get, update
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


class FieldDayListHandler(BaseEntityListHandler):

    def initialize(self, persistentEntityListObj, persistentLocationEntityObj):
        self.__persistentEntityListObj__ = persistentEntityListObj
        self.__persistentLocationEntityObj__ = persistentLocationEntityObj

    def options(self, *args):
        self.set_header("Access-Control-Allow-Methods", "GET, POST")
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

    @coroutine
    def post(self):
        fieldDay = {}
        try:
            fieldDayDateStr = self.get_body_argument("date")
            try:
                fieldDayDate = datetime.strptime(fieldDayDateStr, "%Y-%m-%d").date()
            except Exception as exDate:
                raise ValueError(
                    "The specified 'date', ({0}) must be a valid date in yyyy-mm-dd format".format(
                    fieldDayDateStr
                    )
                )
            fieldDay["date"] = fieldDayDateStr
            fieldDayLocation = self.get_body_argument("location_id")
            
            """ Check that location exists """
            locationGetter = self.__persistentLocationEntityObj__
            verifiedLocation = yield locationGetter.get(locationId=fieldDayLocation)
            if verifiedLocation:
                locationDescription = verifiedLocation["description"]
            else:
                raise ValueError("The location_id specified ({id}) is not valid".format(id=fieldDayLocation))

            fieldDay["location"] = fieldDayLocation
            
            """ Get or synthesise Description """
            fieldDayDescription = self.get_body_argument("description", None)
            if not fieldDayDescription:
                fieldDayDescription = "{loc} - {date}".format(loc=locationDescription, date=fieldDayDateStr)
            fieldDay["description"] = fieldDayDescription
            logger.debug("Description: {0}".format(fieldDayDescription))
        except (ValueError, tornado.web.MissingArgumentError) as exArgument:
            errorMessage = exArgument
            self.set_status(400)
            self.add_header("error", "{0}".format(errorMessage))
            self.finish({"message": "{0}".format(errorMessage)})
            return
        except Exception as ex:
            logger.error("{0}".format(ex))
            errorMessage = "An error occured while attempting to process the new Field Day"
            self.set_status(500)
            self.add_header(
                "error", "{0}".format(
                    errorMessage
                )
            )
            self.finish({"message": "{0}".format(errorMessage)})
            return

        fieldDaySetter = self.__persistentEntityListObj__
        newFieldDayId = yield fieldDaySetter.add(
            fieldDay=fieldDay
            )

        self.set_status(201)
        self.add_header("field_day_id", "{}".format(
                newFieldDayId
            )
        )
        self.finish(
            {"message": "New Field Day ({0}) successfully created".format(newFieldDayId)}
        )


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
