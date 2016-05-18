"""
    This is the base Tornado Request handler from which others will be descenant
"""

__author__    = "Paul Staszyc"
__copyright__ = "Copyright 2016"


import tornado.web
import tornado.escape

import math

class BaseHandler(tornado.web.RequestHandler):

    """ This will be used for functions which require a user context - most, if not all of them will """
    def get_current_user(self):
        user_json = self.get_secure_cookie("user")
        if not user_json:
            return None

        return tornado.escape.json_decode(user_json)

    def prepare(self):
        self.set_header("Access-Control-Allow-Origin", "*")


class BaseAuthenticatedHandler(BaseHandler):

    __user_id__ = None

    @tornado.web.authenticated
    def prepare(self):
        super(BaseAuthenticatedHandler, self).prepare()
        if "user_id" in self.current_user:
            self.__user_id__ = self.current_user["user_id"]

    @tornado.web.authenticated
    def get(self):
        self.finish("Hello, {user}".format(user=self.current_user["handle"]))


class BaseEntityListHandler(BaseHandler):

    def options(self, *args):
        self.set_header("Access-Control-Allow-Methods", "GET")
        self.finish()

    def prepare(self):
        super(BaseEntityListHandler, self).prepare()
        self.__fullyQualifiedRequestPath__ = "{prot}://{server}{path}".format(
            prot=self.request.protocol,
            server=self.request.host,
            path=self.request.path
            )

    def getPageSizeAndNum(self, defaultPageSize=25):
        try:
            pageNum = int(self.get_argument("page", 1))
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

        return (pageSize, pageNum)

    def setResponseHeadersList(self, pageNum, pageSize, totalRecordCount):
        self.set_header("page", "{page_num}".format(page_num = pageNum))
        self.set_header("per_page", "{page_size}".format(page_size = pageSize))

        lastPage = int(math.ceil(totalRecordCount / (pageSize * 1.0)))
        linkHeader = ['<{request_path}?page=1&per_page={page_size}>; rel="first"'.format(request_path = self.__fullyQualifiedRequestPath__, page_size = pageSize)]

        if pageNum > 1:
            linkHeader.append(
                '<{request_path}?page={page_num}&per_page={page_size}>; rel="previous"'.format(
                    request_path=self.__fullyQualifiedRequestPath__,
                    page_num=pageNum -1,
                    page_size=pageSize
                )
            )

        if pageNum < lastPage:
            linkHeader.append(
                '<{request_path}?page={page_num}&per_page={page_size}>; rel="next"'.format(
                    request_path=self.__fullyQualifiedRequestPath__,
                    page_num=pageNum +1,
                    page_size=pageSize
                )
            )

        linkHeader.append(
            '<{request_path}?page={last_page}&per_page={page_size}>; rel="last"'.format(
                request_path=self.__fullyQualifiedRequestPath__,
                last_page=lastPage,
                page_size=pageSize
                )
            )

        linkHeader.append(
            '<{request_path}?page={last_page}&per_page={page_size}>; rel="current"'.format(
                request_path=self.__fullyQualifiedRequestPath__,
                last_page=pageNum,
                page_size=pageSize
                )
            )
        self.set_header("link", ", ".join(linkHeader))
        self.set_header("X-Total-Count", "{0}".format(totalRecordCount))

        self.set_header("Access-Control-Expose-Headers", "X-Total-Count, link, page, per_page")

    def setResponseHeadersNewEntity(self, newId):
        self.set_header("id", "{0}".format(newId))

        linkHeader = ['<{request_path}/{id}>; rel="self"'.format(request_path=self.__fullyQualifiedRequestPath__, id=newId)]
        self.set_header("link", ", ".join(linkHeader))


if __name__ == "__main__":
    pass
