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
auditLogger = logging.getLogger("audit")

class FieldDayListHandler(BaseEntityListHandler):

    def initialize(self, persistentEntityListObj, persistentLocationEntityObj):
        self.__persistentEntityListObj__ = persistentEntityListObj
        self.__persistentLocationEntityObj__ = persistentLocationEntityObj

    def options(self, *args):
        allowedMethods = list(["OPTIONS", "GET"])
        try:
            user = self.get_current_user()
            if user and any(user):
                allowedMethods.extend(["POST"]) # PUT and DELETE to follow
        except Exception as ex:
            logger.error(ex)

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
        entityListGetter = self.__persistentEntityListObj__
        fieldDayList, totalRecordCount = yield entityListGetter.get(
            limit=limit,
            offset=offset
            )
        self.setResponseHeadersList(
            pageNum=pageNum,
            pageSize=pageSize,
            totalRecordCount=totalRecordCount
        )
        self.finish({"data": fieldDayList})

    @tornado.web.authenticated
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
            print "Preparing to verify location"
            verifiedLocation = yield locationGetter.get(locationId=fieldDayLocation)
            print "Verified Location: {}".format("verifiedLocation")
            if verifiedLocation:
                locationDescription = verifiedLocation["description"]
            else:
                raise ValueError("The location_id specified ({id}) is not valid".format(id=fieldDayLocation))

            fieldDay["location_id"] = fieldDayLocation
            fieldDay["location"] = locationDescription

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
        self.setResponseHeadersNewEntity(newFieldDayId)
        self.finish(
            {"message": "New Field Day ({0}) successfully created".format(newFieldDayId)}
        )
        self.auditLog.info(
            "CREATE FIELD DAY",
            extra={
                "user": self.userId,
                "what": "POST Field Day {} via {}".format(newFieldDayId, type(self).__name__),
                "path": self.request.path
            }
        )


class FieldDayHandler(BaseHandler):

    def initialize(self, persistentEntityObj):
        self.__persistentEntityObj__ = persistentEntityObj

    def options(self, *args):
        allowedMethods = list(["OPTIONS", "GET"])
        try:
            user = self.get_current_user()
            if user and any(user):
                allowedMethods.append("PUT") # DELETE to follow
        except Exception as ex:
            logger.error(ex)

        self.set_header("Access-Control-Allow-Methods", ",".join(allowedMethods))
        self.finish()

    @coroutine
    def get(self, fieldDayId):
        entityGetter = self.__persistentEntityObj__
        try:
            fieldDayEntity = yield entityGetter.get(fieldDayId=fieldDayId)
            if (not fieldDayEntity or not any(fieldDayEntity)):
                raise KeyError("The Field Day requested does not exist")
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

    @tornado.web.authenticated
    @coroutine
    def put(self, fieldDayId):
        self.finish()


class FieldDayTidesHandler(BaseHandler):

    auditLog = logging.getLogger("audit")

    def initialize(self, persistentEntityObj):
        self.__persistentEntityObj__ = persistentEntityObj

    def options(self, *args):
        allowedMethods = list(["OPTIONS", "GET"])
        try:
            user = self.get_current_user()
            if user and any(user):
                allowedMethods.append("POST")
        except Exception as ex:
            logger.error(ex)

        self.set_header("Access-Control-Allow-Methods", ",".join(allowedMethods))
        self.finish()

    @coroutine
    def get(self, fieldDayId):
        entityGetter = self.__persistentEntityObj__
        try:
            fieldDayTidesEntity = yield entityGetter.get(fieldDayId=fieldDayId)
            if (not fieldDayTidesEntity or not any(fieldDayTidesEntity)):
                raise KeyError("The Tides for Field Day you have requested do not exist")
        except KeyError as exNotFound:
            errorMessage = exNotFound
            self.set_status(404)
            self.add_header("error", "{0}".format(errorMessage))
            self.finish({"message": "{0}".format(errorMessage)})
            return
        except Exception as ex:
            logger.error("{0}".format(ex))
            errorMessage = "An error occured while attempting to retireve the requested Field Day Tides"
            self.set_status(500)
            self.add_header(
                "error", "{0}".format(
                    errorMessage
                )
            )
            self.finish({"message": "{0}".format(errorMessage)})
            return
        else:
            self.finish(fieldDayTidesEntity)

    def __validateTideObject__(self, tideObj):
        isValid = True
        message = "Valid Tide"
        missingItems = [mandatoryItem for mandatoryItem in ['time', 'height'] if (mandatoryItem not in tideObj.iterkeys())]
        if len(missingItems) > 0:
            return (False, "\"height\" and \"time\" are required")

        extraneousItems = [extraItem for extraItem in tideObj.iterkeys() if (extraItem not in ['time', 'height'])]
        if len(extraneousItems) > 0:
            return (False, "Only \"height\" and \"time\" may be specified")

        return (isValid, message)

    @tornado.web.authenticated
    @coroutine
    def post(self, fieldDayId):
        fieldDayTides = dict()
        try:
            tidesStr = self.get_body_argument("tides", None)
            try:
                if tidesStr:
                    tides = tornado.escape.json_decode(tidesStr)
                    for tide in tides:
                        isValid, msg = self.__validateTideObject__(tides[tide])
                        if not isValid:
                            raise ValueError(msg)

                    fieldDayTides["tides"] = tides

            except Exception as exTides:
                logger.warning("Error parsing tides ({tides}): {ex}".format(tides=tidesStr, ex=exTides))
                raise ValueError(
                    "The correct format for the 'tides' argument is a form-encoded object in the form {[\"high|low\"]: {\"height\": f, \"time\": \"hh:mm:ss\"}}"
                )
            highTideStr = self.get_body_argument("high", None)
            if highTideStr:
                if tidesStr:
                    raise ValueError("If 'tides' is provided, neither 'high' nor 'low' may be individually specified")

                try:
                    highTide = tornado.escape.json_decode(highTideStr)
                    isValid, msg = self.__validateTideObject__(highTide)
                    if not isValid:
                        raise ValueError(msg)
                    fieldDayTides["high"] = highTide
                except Exception as exTides:
                    logger.warning("Error parsing high ({tide}): {ex}".format(tide=highTideStr, ex=exTides))
                    raise ValueError(
                        "The correct format for the 'high' argument is a form-encoded object in the form {\"height\": f, \"time\": \"hh:mm:ss\"}"
                    )

            lowTideStr = self.get_body_argument("low", None)
            if lowTideStr:
                if tidesStr:
                    raise ValueError("If 'tides' is provided, neither 'high' nor 'low' may be individually specified")

                try:
                    lowTide = tornado.escape.json_decode(lowTideStr)
                    isValid, msg = self.__validateTideObject__(lowTide)
                    if not isValid:
                        raise ValueError(msg)
                    fieldDayTides["low"] = lowTide
                except Exception as exTides:
                    logger.warning("Error parsing low ({tide}): {ex}".format(tide=lowTideStr, ex=exTides))
                    raise ValueError(
                        "The correct format for the 'low' argument is a form-encoded object in the form {\"height\": f, \"time\": \"hh:mm:ss\"}"
                    )

            if not any(fieldDayTides):
                raise tornado.web.MissingArgumentError("One of \"tides\", \"high\" or  \"low\" must be specified")
        except (ValueError, tornado.web.MissingArgumentError) as exArgument:
            errorMessage = exArgument
            self.set_status(400)
            self.add_header("error", "{0}".format(errorMessage))
            self.finish({"message": "{0}".format(errorMessage)})
            return

        entitySetter = self.__persistentEntityObj__
        try:
            print fieldDayTides
            updateCount = yield entitySetter.update(
                fieldDayId=fieldDayId,
                **fieldDayTides # dict of args "tides" or "high" and/or "low"
            )
            if updateCount <= 0:
                raise Exception("Zero Field Days were updated")
        except Exception as ex:
            logger.error("{0}".format(ex))
            errorMessage = "An error occured while attempting to update the requested Field Day Tides"
            self.set_status(500)
            self.add_header(
                "error", "{0}".format(
                    errorMessage
                )
            )
            self.finish({"message": "{0}".format(errorMessage)})
            return

        self.finish(
            {"message": "Tides for Field Day ({0}) successfully updated".format(fieldDayId)}
        )
        auditLogger.info(
            "UPDATE FIELD DAY TIDES",
            extra={
                "user": self.userId,
                "what": "{method} Field Day {id} TIDES via {func}".format(method=self.request.method, id=fieldDayId, func=type(self).__name__),
                "path": self.request.path
            }
        )


if __name__ == "__main__":
    pass
