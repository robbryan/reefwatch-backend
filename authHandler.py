import tornado.web
import tornado.auth
from baseHandler import BaseHandler

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
auditLog = logging.getLogger("audit")


class AuthHandler(BaseHandler):

    @tornado.concurrent.return_future
    def __onAuth__(self, user, callback):
        if not user:
            raise tornado.web.HTTPError(500, "OAuth authentication was not successful")

        else:
            if "given_name" in user and user["given_name"] != "":
                handle = user["given_name"]
            elif "screen_name" in user and user["screen_name"] != "":
                handle = user["screen_name"]
            else:
                handle = user["name"]

            user["user_handle"] = handle

            """ Check if user exists """
            self.__persistentUserListObj__.get(
                query={"email": user["email"]},
                callback=lambda (x, y): self.__onGetMatchingUserList__(userDetails=user, userList=x, callback=callback)
            )

    def __setCookieAndRedirect__(self, userDetails, callback):
        try:
            self.set_secure_cookie(
                "user",
                tornado.escape.json_encode(
                    {
                        "user_id": userDetails["id"],
                        "user_handle": userDetails["user_handle"]
                    }
                )
            )
            self.finish({"message": "Successfully authenticated as {}".format(userDetails["user_handle"])})
            auditLog.info(
                "AUTHENTICATE USER",
                extra={
                    "user": userDetails["id"],
                    "what": "Authenticate user {} via {}".format(userDetails["id"], type(self).__name__),
                    "path": self.request.path
                }
            )
            callback()
        except Exception as ex:
            logger.exception(ex)

    def __onCreateNewUser__(self, userDetails, callback):
        try:
            auditLog.info(
                "CREATE NEW USER",
                extra={
                    "user": userDetails["id"],
                    "what": "Create new user {} via {}".format(userDetails["id"], type(self).__name__),
                    "path": self.request.path
                }
            )
        except Exception as ex:
            logger.exception(ex)

        self.__setCookieAndRedirect__(userDetails=userDetails, callback=callback)

    def __onGetMatchingUserList__(self, userDetails, userList, callback):
        if len(userList) == 1:
            self.__setCookieAndRedirect__(userDetails=userList[0], callback=callback)
        else:
            try:
                assert len(userList) == 0, "Expected either zero or one matches for users with e-mail address {}".format(userDetails["email"])
                self.__persistentUserListObj__.add(
                    callback=lambda x: self.__onCreateNewUser__(
                        userDetails={
                            "user_handle": userDetails["user_handle"],
                            "id": x,
                            "full_name": userDetails["name"]
                        },
                        callback=callback
                    ),
                    userFullName=userDetails["name"],
                    userHandle=userDetails["user_handle"],
                    emailAddress=userDetails["email"],
                    providerGeneratedId=userDetails["provider_user_id"] if "provider_user_id" in userDetails else None
                )
            except Exception as ex:
                logger.exception(ex)

    def initialize(self, persistentUserListObj):
        self.__persistentUserListObj__ = persistentUserListObj


class LogoutHandler(BaseHandler):

    def get(self):
        self.clear_cookie("user")
        self.redirect("/")


class GoogleLoginHandler(AuthHandler, tornado.auth.GoogleOAuth2Mixin):

    def initialize(self, callbackPath, **kwargs):
        super(GoogleLoginHandler, self).initialize(kwargs.get("persistentUserListObj"))
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
