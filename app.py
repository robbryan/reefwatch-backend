"""
    This is the main application file from which the ReefWatch backend is started
"""

__author__    = "Paul Staszyc"
__copyright__ = "Copyright 2016"


import tornado.ioloop
import tornado.web
import tornado.httpserver
from tornado.options import define, options

""" Local Settings """
try:
  import localSettings
except ImportError:
    print "'localSettings.py' NOT found. Using Dummy instead"

import logging

if not hasattr(options, "log_file"):
    define("log_file", default="access.log", help="Name of file to which to log")

logging.basicConfig(filename=options.log_file, format='%(asctime)-6s: %(name)s - %(levelname)s - %(message)s')

""" Field Days """
from fieldDayHandler import FieldDayListHandler, FieldDayHandler, FieldDayTidesHandler

""" Surveys """
from persistence.SurveyListPersistenceBase import PersistentSurveyListDummy as PersistentSurveyList
from surveyHandler import SurveyListHandler

""" Locations """
from persistence.LocationListPersistenceBase import PersistentLocationListDummy as PersistentLocationList
from persistence.LocationPersistenceDummy import PersistentLocationDummy as PersistentLocationEntity
from locationHandler import LocationListHandler

""" Sites """
from persistence.SiteListPersistenceBase import PersistentSiteListDummy as PersistentSiteList
from siteHandler import SiteListHandler

from baseHandler import BaseAuthenticatedHandler

import importlib

"""
    Determine which storage engine is specified in the user config and
    import the appropriate modules to support that
"""
try:
    persistenceOptions = options.group_dict("persistence")
except KeyError:
    raise
else:
    """ Mongo DB Persistence """
    if "mongo_instance" in persistenceOptions:
        from pymongo import MongoClient
        mongoClient = MongoClient(persistenceOptions["mongo_instance"])
        mongoDb = mongoClient[persistenceOptions["mongo_database"]]
        if "mongo_user" in persistenceOptions:
            mongoDb.authenticate(persistenceOptions["mongo_user"], persistenceOptions["mongo_password"])
    else:
        noMongoMessage = "Warning! No persistence engine was specified for Field Day List - See localSettings.py.sample for examples"
        print noMongoMessage
        print "Using Dummy persistence instead - That's ok for Demos"
        

        from mongomock import MongoClient
        mongoClient = MongoClient()
        mongoDb = mongoClient.db

    PersistentFieldDayListModule = importlib.import_module("persistence.FieldDayListMongo")
    try:
        fieldDayOptions = options.group_dict("field_day")
    except KeyError as exNoMongoOptions:
        fieldDayOptions = {}

    if "field_day_collection" not in fieldDayOptions:
        fieldDayOptions["field_day_collection"] = "field_day"

    PersistentFieldDayList = PersistentFieldDayListModule.PersistentFieldDayList(
        mongoDb[fieldDayOptions["field_day_collection"]]
    )

    PersistentFieldDayModule = importlib.import_module("persistence.FieldDayMongo")
    PersistentFieldDayEntity = PersistentFieldDayModule.PersistentFieldDay(
        mongoDb[fieldDayOptions["field_day_collection"]]
    )

    PersistentFieldDayTidesEntity = PersistentFieldDayModule.PersistentFieldDayTides(
        mongoDb[fieldDayOptions["field_day_collection"]]
    )


from authHandler import LogoutHandler


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world!")


class Application(tornado.web.Application):

    logger = logging.getLogger('ReefWatch Backend Event logger')

    def __init__(self):

        try:
            assert(hasattr(options, 'cookie_secret'))
            assert(options.cookie_secret)
        except AssertionError:
            print "You must specify a 'cookie_secret' for encrypting cookies."
            raise SystemExit("Exiting...")

        settings = dict(
            debug=options.debug if hasattr(options, 'debug') else False,
            cookie_secret=options.cookie_secret
        )

        self.logger.setLevel(
            logging.DEBUG if hasattr(options, 'debug') and options.debug else logging.INFO
        )

        """
            Regular Expression for matching GUIDs.
            Case-insensitive. With or without dashes. No curly braces
        """
        guidRegex = r"[0-9A-Fa-f]{8}-*[0-9A-Fa-f]{4}-*[0-9A-Fa-f]{4}-*[0-9A-Fa-f]{4}-*[0-9A-Fa-f]{12}"
        mongoIdRegex = r"[0-9A-Fa-f]{24}"

        handlers = [
            (r"/", MainHandler),
            (
                r"/field_days",
                FieldDayListHandler,
                dict(
                    persistentEntityListObj=PersistentFieldDayList,
                    persistentLocationEntityObj=PersistentLocationEntity()
                )
            ),
            (r"/field_days/({guid})/tides".format(guid=guidRegex), FieldDayTidesHandler, dict(persistentEntityObj=PersistentFieldDayTidesEntity)),
            (r"/field_days/({guid})".format(guid=guidRegex), FieldDayHandler, dict(persistentEntityObj=PersistentFieldDayEntity)),
            (r"/field_days/({id})".format(id=mongoIdRegex), FieldDayHandler, dict(persistentEntityObj=PersistentFieldDayEntity)),
            (r"/surveys", SurveyListHandler, dict(persistentSurveyListObj=PersistentSurveyList())),
            (r"/locations/({guid})/sites".format(guid=guidRegex), SiteListHandler, dict(persistentEntityListObj=PersistentSiteList())),
            (r"/locations", LocationListHandler, dict(persistentLocationListObj=PersistentLocationList())),
            (r"/auth/success", BaseAuthenticatedHandler),
            (r"/auth/logout", LogoutHandler)
        ]

        # Google OAuth2 Settings
        if hasattr(options, "google_client_id"):
            google_oauth = {"key": options.google_client_id, "secret": options.google_client_secret}
            settings["google_oauth"] = google_oauth
            from authHandler import GoogleLoginHandler
            handlers.append((
                r"/auth/login/google",
                GoogleLoginHandler,
                dict(callbackPath="auth/callback/google")
            ))
            handlers.append((
                r"/auth/callback/google",
                GoogleLoginHandler,
                dict(callbackPath="auth/callback/google")
            ))
        else:
            # Dummy Authentication
            print "Google OAuth2 authentication not set up. Using dummy instead"
            from authHandlerDummy import DummyLoginHandler
            handlers.append((
                r"/auth/login/dummy",
                DummyLoginHandler
            ))

        tornado.web.Application.__init__(self, handlers, **settings)


def main():
    if not hasattr(options, "port"):
        define("port", default="9880", help="Port on which the HTTP server will listen")

    if not hasattr(options, "debug"):
        define("debug", default=False, help="Set some logging options + auto-reload on file change")
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    print "Listening on port: {port}".format(port=options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
