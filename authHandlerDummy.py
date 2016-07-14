"""
    This is the Dummy version of the Authentication Handler.
    Use it only for *demos* where you don't have Google Auth configured
"""

__author__    = "Paul Staszyc"
__copyright__ = "Copyright 2016"

import tornado.web

from authHandler import AuthHandler

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logger.getEffectiveLevel())
logger.warning("DUMMY AUTHENTICATOR IN USE - Not ok for production!")


class DummyLoginHandler(AuthHandler):

    @tornado.gen.coroutine
    def get(self):
        try:
            userName = self.get_query_argument("user_name")
            userHandle = self.get_query_argument("user_handle", userName)
        except (ValueError, tornado.web.MissingArgumentError) as exArgument:
            errorMessage = exArgument
            self.set_status(400)
            self.add_header("error", "{0}".format(errorMessage))
            self.finish({"message": "{0}".format(errorMessage)})
            return
        user = {
            "id": "dummy_user_id",
            "provider": "DUMMY",
            "name": userName,
            "user_handle": userHandle
        }
        self.__setCookieAndRedirect__(userDetails=user, callback=lambda: None)

if __name__ == "__main__":
    pass
