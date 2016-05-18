import tornado.web
import tornado.auth
from baseHandler import BaseHandler

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logger.getEffectiveLevel())


class AuthHandler(BaseHandler):

    @tornado.concurrent.return_future
    def __onAuth__(self, user, callback):
        if not user:
            raise tornado.web.HTTPError(500, "OAuth authentication was not successful")

        else:
            if "name" in user and user["name"] != "":
                handle = user["name"]
            elif "screen_name" in user and user["screen_name"] != "":
                handle = user["screen_name"]
            else:
                handle = "Reefwatch User"

            self.set_secure_cookie("user", tornado.escape.json_encode({"user_id": user["provider_user_id"], "handle": handle}))
            self.redirect("/auth/success")


class LogoutHandler(BaseHandler):

    def get(self):
        self.clear_cookie("user")
        self.redirect("/")


class GoogleLoginHandler(AuthHandler, tornado.auth.GoogleOAuth2Mixin):

    def initialize(self, callbackPath):
        callbackUri = "{prot}://{host}/{path}".format(
            prot=self.request.protocol,
            host=self.request.host,
            path=callbackPath
            )
        self.__callbackUri__ = callbackUri

    @tornado.gen.coroutine
    def get(self):
        if self.get_argument('code', False):
            try:
                access = yield self.get_authenticated_user(
                    redirect_uri=self.__callbackUri__,
                    code=self.get_argument('code'))
                user = yield self.oauth2_request(
                    "https://www.googleapis.com/oauth2/v1/userinfo",
                    access_token=access["access_token"]
                )
                user["provider_user_id"] = user["id"]
                self.__onAuth__(user)

            except Exception as exAuth:
                logger.error(exAuth)
                raise tornado.web.HTTPError(500, 'Google authentication failed')

        else:
            logger.debug("Google Authorise Redirect - {redirect}".format(redirect=self.__callbackUri__))
            yield self.authorize_redirect(
                redirect_uri=self.__callbackUri__,
                client_id=self.settings['google_oauth']['key'],
                scope=['profile', 'email'],
                response_type='code',
                extra_params={'approval_prompt': 'auto'})



if __name__=="__main__":
    pass;
