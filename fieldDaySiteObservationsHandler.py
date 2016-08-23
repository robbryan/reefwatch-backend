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

    def __validateWeatherObject__(self, tideObj):
        isValid = True
        message = "Valid Weather Observation"
        mandatoryItems = ['wind_force', 'wind_direction', 'amount_of_cloud', 'rainfall']
        missingItems = [mandatoryItem for mandatoryItem in mandatoryItems if (mandatoryItem not in tideObj.iterkeys())]
        if len(missingItems) > 0:
            return (False, "{} are required".format(", ".join(map(lambda x: "\"{}\"".format(x), mandatoryItems))))

        acceptableItems = mandatoryItems + ["comments"]
        extraneousItems = [extraItem for extraItem in tideObj.iterkeys() if (extraItem not in acceptableItems)]
        if len(extraneousItems) > 0:
            return (False, "Only {} may be specified".format(", ".join(map(lambda x: "\"{}\"".format(x), acceptableItems))))

        return (isValid, message)

    @coroutine
    @tornado.web.authenticated
    def post(self, fieldDayId, siteCode):
        """
        curl -X POST --cookie cookies.txt -F "weather={\"wind_force\": 2, \"wind_direction\": \"S\", \"amount_of_cloud\": 3}" http://localhost:9880/field_days/573e765fc1ed602daf609007/sites/ANL/observations
        """
        try:
            weatherStr = self.get_body_argument("weather")
        except (ValueError, tornado.web.MissingArgumentError) as exArgument:
            errorMessage = exArgument
            self.set_status(400)
            self.add_header("error", "{0}".format(errorMessage))
            self.finish({"message": "{0}".format(errorMessage)})
            return

        try:
            try:
                weather = tornado.escape.json_decode(weatherStr)
                isValid, weatherValidationMsg = self.__validateWeatherObject__(weather)
                if not isValid:
                    raise ValueError(weatherValidationMsg)
            except Exception as exWeather:
                logger.warning(
                    "Error parsing weather ({weather}): {ex}".format(
                        weather=weatherStr,
                        ex=exWeather
                    )
                )
                raise ValueError(
                    "The correct format for the 'weather' argument is a form-encoded object in the form {\"wind_force\"]: f, \"wind_direction\": \"s\", \"amount_of_cloud\": f}"
                )
        except (ValueError, tornado.web.MissingArgumentError) as exArgument:
            errorMessage = exArgument
            self.set_status(400)
            self.add_header("error", "{0}".format(errorMessage))
            self.finish({"message": "{0}".format(errorMessage)})
            return

        try:
            observationTime = self.get_body_argument("observation_time")
        except (ValueError, tornado.web.MissingArgumentError) as exArgument:
            errorMessage = exArgument
            self.set_status(400)
            self.add_header("error", "{0}".format(errorMessage))
            self.finish({"message": "{0}".format(errorMessage)})
            return

if __name__ == "__main__":
    pass
