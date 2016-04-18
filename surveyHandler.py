"""
    This is the Request handler for Surveys
"""

__author__    = "Paul Staszyc"
__copyright__ = "Copyright 2016"


from baseHandler import BaseHandler


class SurveyListHandler(BaseHandler):

    def get(self):
        self.write([])


if __name__ == "__main__":
    pass