"""
    This is the base Tornado Request handler from which others will be descenant
"""

__author__    = "Paul Staszyc"
__copyright__ = "Copyright 2016"


import tornado.web
import tornado.escape


class BaseHandler(tornado.web.RequestHandler):

    """ This will be used for functions which require a user context - most, if not all of them will """
    def get_current_user(self):
        user_json = self.get_secure_cookie("user")
        if not user_json:
            return None

        return tornado.escape.json_decode(user_json)


class BaseAuthenticatedHandler(BaseHandler):

    __user_id__ = None

    @tornado.web.authenticated
    def prepare(self):

        if "user_id" in self.current_user:
            self.__user_id__ = self.current_user["user_id"]


class BaseEntityListHandler(BaseHandler):

    def getLimitAndOffset(self, defaultLimit, defaultPageSize):
        try:
            pageNum = int(self.get_argument("page", defaultLimit))
            if pageNum < 1:
                raise ValueError
        except:
            raise ValueError("The 'page' parameter must be a positive integer")

        try:
            pageSize = int(self.get_argument("per_page", defaultPageSize))
            if pageSize < 1:
                raise ValueError
        except:
            raise ValueError("The 'per_page' parameter must be a positive integer")

        return ((pageNum-1)*pageSize, pageSize)


if __name__ == "__main__":
    pass
            
