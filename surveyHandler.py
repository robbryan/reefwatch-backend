"""
    This is the Request handler for Surveys
"""

__author__    = "Paul Staszyc"
__copyright__ = "Copyright 2016"

from tornado.gen import coroutine

from baseHandler import BaseEntityListHandler

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logger.getEffectiveLevel())


class SurveyTypeListHandler(BaseEntityListHandler):

    def initialize(self, persistentSurveyListObj):
        self.__persistentSurveyListObj__ = persistentSurveyListObj

    def get(self):
        surveyListGetter = self.__persistentSurveyListObj__
        surveyList = surveyListGetter.get()
        self.write({"data": surveyList})


class FieldDaySurveyListHandler(BaseEntityListHandler):

    def initialize(self, persistentFieldDaySurveyListObj):
        self.__persistentFieldDaySurveyListObj__ = persistentFieldDaySurveyListObj

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
    def get(self, fieldDayId, siteId=None):
        try:
            pageSize, pageNum = self.getPageSizeAndNum()
        except ValueError as exPage:
            self.set_status(400)
            self.add_header("error", "{0}".format(exPage))
            self.finish({"message": "{0}".format(exPage)})
            return

        offset = (pageNum-1)*pageSize
        limit = pageSize
        entityListGetter = self.__persistentFieldDaySurveyListObj__
        try:
            fieldDaySurveyList, totalRecordCount = yield entityListGetter.get(
                fieldDayId=fieldDayId,
                limit=limit,
                offset=offset
            )
            if fieldDaySurveyList is None:
                raise KeyError("Surveys have not been recorded for this Site")
        except KeyError as exNotFound:
            errorMessage = exNotFound
            self.set_status(404)
            self.add_header("error", "{0}".format(errorMessage))
            self.finish({"message": "{0}".format(errorMessage)})
            return
        except Exception as ex:
            logger.error("{0}".format(ex))
            errorMessage = "An error occured while attempting to retireve the Surveys for a Field Day"
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

        self.finish({"data": fieldDaySurveyList})


if __name__ == "__main__":
    pass