"""
    This is the Request handler for Surveys
"""

__author__    = "Paul Staszyc"
__copyright__ = "Copyright 2016"


from baseHandler import BaseHandler


class SurveyListHandler(BaseHandler):

    def initialize(self, persistentSurveyListObj):
        self.__persistentSurveyListObj__ = persistentSurveyListObj

    def get(self):
        surveyListGetter = self.__persistentSurveyListObj__
        surveyList = surveyListGetter.get()
        self.write({"data": surveyList})


if __name__ == "__main__":
    pass