"""
    This is the main application file from which the ReefWatch backend is started
"""

__author__    = "Paul Staszyc"
__copyright__ = "Copyright 2016"


import tornado.ioloop
import tornado.web
import tornado.httpserver
from tornado.options import define, options

""" Surveys """
from persistence.SurveyListPersistenceBase import PersistentSurveyListDummy as PersistentSurveyList
from surveyHandler import SurveyListHandler

""" Locations """
from persistence.LocationListPersistenceBase import PersistentLocationListDummy as PersistentLocationList
from locationHandler import LocationListHandler

import logging


if not hasattr(options, "log_file"):
    define("log_file", default="access.log", help="Name of file to which to log")

logging.basicConfig(filename=options.log_file, format='%(asctime)-6s: %(name)s - %(levelname)s - %(message)s')


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world!")


class Application(tornado.web.Application):

    logger = logging.getLogger('ReefWatch Backend Event logger')

    def __init__(self):
        settings = dict(
            debug=options.debug if 'debug' in options else False
        )

        handlers = [
            (r"/", MainHandler),
            (r"/surveys", SurveyListHandler, dict(persistentSurveyListObj=PersistentSurveyList())),
            (r"/locationss", LocationListHandler, dict(persistentLocationListObj=PersistentLocationList()))
        ]

        tornado.web.Application.__init__(self, handlers, **settings)


def main():
    define("port", default="9880", help="Port on which the HTTP server will listen")
    define("debug", default=False, help="Set some logging options + auto-reload on file change")
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
