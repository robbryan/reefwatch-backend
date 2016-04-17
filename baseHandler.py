"""
    This is the base Tornado Request handler from which others will be descenant
"""

__author__    = "Paul Staszyc"
__copyright__ = "Copyright 2016"


import tornado.web


class BaseHandler(tornado.web.RequestHandler):

    """ This will be used for functions which require a user context - most, if not all of them will """
    def get_current_user(self):
        user_json = self.get_secure_cookie("user")
        if not user_json: return None
        return tornado.escape.json_decode(user_json)