import tornado.testing
import tornado.web
import tornado.escape

from authHandlerDummy import DummyLoginHandler
from authHandler import LogoutHandler
from baseHandler import BaseHandler

import logging
import Cookie


class LoginSuccessHandler(BaseHandler):

    def get(self):
        print "Login Success Handler"
        user = self.get_current_user()
        self.finish(
            user
        )


class LogoutSuccessHandler(BaseHandler):

    def get(self):
        print "Logout Success Handler"
        user = self.get_current_user()
        self.finish(
            user if user and any(user) else "USER NOT FOUND"
        )


class RequiresAuthHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.finish("Authenticated")


class TestDummyAuthHandler(tornado.testing.AsyncHTTPTestCase):

    __cookieSecret__ = "THIS_IS_THE_TEST_COOKIE_SECRET"

    def __init__(self, *rest):
        self.cookies = Cookie.SimpleCookie()
        tornado.testing.AsyncHTTPTestCase.__init__(self, *rest)

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def _update_cookies(self, headers):
        try:
            sc = headers['Set-Cookie']
            cookies = tornado.escape.native_str(sc)
            self.cookies.update(Cookie.SimpleCookie(cookies))
            while True:
                self.cookies.update(Cookie.SimpleCookie(cookies))
                if ',' not in cookies:
                    break
                cookies = cookies[cookies.find(',') + 1:]
        except KeyError:
            return
        print self.cookies

    def fetch(self, url, *r, **kw):
        if 'follow_redirects' not in kw:
            kw['follow_redirects'] = False
        header = {}
        hs = self.cookies.output()
        if hs != '':
            if ";" in hs:
                hs = ":".join(hs.split(":")[1:]).split(";")[0].strip()
            else:
                hs = hs.split(':')[1]
            header['Cookie'] = hs
            #print "URL: {}, Cookie: {}".format(url, header['Cookie'])
        resp = tornado.testing.AsyncHTTPTestCase.fetch(self, url, headers=header, *r, **kw)
        self._update_cookies(resp.headers)
        return resp

    def get_app(self):
        application = tornado.web.Application([
                (
                    r"/auth/login/dummy",
                    DummyLoginHandler
                ),
                (r'/auth/success', LoginSuccessHandler),
                (r'/auth/Logout', LogoutHandler),
                (r'/requires_auth', RequiresAuthHandler),
                (r'/', LogoutSuccessHandler)
                ]
            )
        application.settings = dict(
            cookie_secret=self.__cookieSecret__,
            login_url="/auth/login/dummy"
            )
        return application

    def test_loginWorkflow(self):
        """
            Test workflow from redirect when not authenticated to successfull authenticated request to successful logout
        """

        """ No redirect now that I'm authenticated """
        response = self.fetch("/requires_auth", follow_redirects=False)
        self.assertEqual(response.code, 302)

        requestQuery = "user_name={0}&user_handle={1}".format(
            tornado.escape.url_escape("test1"),
            tornado.escape.url_escape("Test user 1")
        )
        loginResponse = self.fetch("/auth/login/dummy?" + requestQuery, follow_redirects=False)
        self.assertEqual(loginResponse.code, 302)

        print "COOKIES: {0}".format(self.cookies.output())
        authenticatedResponse = self.fetch("/auth/success", follow_redirects=False)
        self.assertEqual(authenticatedResponse.code, 200)

        """ No redirect now that I'm authenticated """
        response = self.fetch("/requires_auth", follow_redirects=False)
        self.assertEqual(response.code, 200)

        print "COOKIES: {0}".format(self.cookies.output())
        logoutResponse = self.fetch('/auth/Logout', follow_redirects=False)
        self.assertEqual(logoutResponse.code, 302)

        print "COOKIES: {0}".format(self.cookies.output())
        authenticatedResponse = self.fetch("/", follow_redirects=False)
        print "Response: {0}".format(authenticatedResponse.body)
        self.assertEqual(authenticatedResponse.code, 200)
        self.assertIn('USER NOT FOUND', authenticatedResponse.body)


if __name__ == "__main__":
    tornado.testing.main()

