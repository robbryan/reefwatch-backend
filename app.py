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
from surveyHandler import SurveyTypeListHandler, FieldDaySurveyListHandler

""" Locations """
from locationHandler import LocationListHandler, LocationHandler

""" Sites """
from siteHandler import SiteListHandler
from fieldDaySiteHandler import FieldDaySiteListHandler, FieldDaySiteHandler

""" Observations """
from fieldDaySiteObservationsHandler import FieldDaySiteObservationsHandler

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
        if "mongo_user" in persistenceOptions and persistenceOptions["mongo_user"]:
            mongoDb.authenticate(persistenceOptions["mongo_user"], persistenceOptions["mongo_password"])
    else:
        noMongoMessage = "Warning! No persistence engine was specified for Field Day List - See localSettings.py.sample for examples"
        print noMongoMessage
        print "Using Dummy persistence instead - That's ok for Demos"

        from mongomock import MongoClient
        mongoClient = MongoClient()

        mongoDb = mongoClient.db
        try:
            import demo.fieldDayDemoData
            if hasattr(options, "field_day_collection"):
                fieldDayCollection = mongoDb[options.field_day_collection]
            else:
                fieldDayCollection = mongoDb["field_day"]
            for fieldDay in demo.fieldDayDemoData.fieldDayList:
                fieldDayCollection.insert(fieldDay)

            if hasattr(options, "location_collection"):
                locationCollection = mongoDb[options.location_collection]
            else:
                locationCollection = mongoDb["reefwatch_location"]
            for reefwatchLocation in demo.fieldDayDemoData.locationList:
                locationCollection.insert(reefwatchLocation)

            if hasattr(options, "survey_type_collection"):
                surveyTypeCollection = mongoDb[options.survey_type_collection]
            else:
                surveyTypeCollection = mongoDb["survey_type"]
            for surveyType in demo.fieldDayDemoData.surveyTypeList:
                surveyTypeCollection.insert(surveyType)

        except ImportError:
            print "Unable to locate fieldDayDemoData in demo. No Demo data available" 
        except Exception as ex:
            print ex
            print "Unable to load fieldDayList from fieldDayDemoData. No Demo data available"

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

    PersistentFieldDaySurveyListModule = importlib.import_module("persistence.FieldDaySurveyListMongo")
    PersistentFieldDaySurveyList = PersistentFieldDaySurveyListModule.PersistentFieldDaySurveyList(
        mongoDb[fieldDayOptions["field_day_collection"]]
    )

    PersistentFieldDaySiteListModule = importlib.import_module("persistence.FieldDaySiteListMongo")
    PersistentFieldDaySiteList = PersistentFieldDaySiteListModule.PersistentFieldDaySiteList(
        mongoDb[fieldDayOptions["field_day_collection"]]
    )

    PersistentFieldDaySiteModule = importlib.import_module("persistence.FieldDaySiteMongo")
    PersistentFieldDaySite = PersistentFieldDaySiteModule.PersistentFieldDaySite(
        mongoDb[fieldDayOptions["field_day_collection"]]
    )

    PersistentFieldDaySurveyListModule = importlib.import_module("persistence.FieldDaySurveyListMongo")
    PersistentFieldDaySurveyList = PersistentFieldDaySurveyListModule.PersistentFieldDaySurveyList(
        mongoDb[fieldDayOptions["field_day_collection"]]
    )

    try:
        reefwatchLocationOptions = options.group_dict("location")
    except KeyError as exNoMongoOptions:
        reefwatchLocationOptions = {}

    if "location_collection" not in fieldDayOptions:
        reefwatchLocationOptions["location_collection"] = "reefwatch_location"

    PersistentLocationListModule = importlib.import_module("persistence.LocationListMongo")
    PersistentLocationList = PersistentLocationListModule.PersistentLocationList(
        mongoDb[reefwatchLocationOptions["location_collection"]]
    )

    PersistentLocationEntityModule = importlib.import_module("persistence.LocationMongo")
    PersistentLocationEntity = PersistentLocationEntityModule.PersistentLocation(
        mongoDb[reefwatchLocationOptions["location_collection"]]
    )

    PersistentLocationSiteListModule = importlib.import_module("persistence.LocationSiteListMongo")
    PersistentLocationSiteList = PersistentLocationSiteListModule.PersistentLocationSiteList(
        mongoDb[reefwatchLocationOptions["location_collection"]]
    )

    try:
        surveyTypeOptions = options.group_dict("survey_type")
    except KeyError as exNoMongoOptions:
        surveyTypeOptions = {}

    if "survey_type_collection" not in fieldDayOptions:
        reefwatchLocationOptions["survey_type_collection"] = "survey_type"

    PersistentLocationListModule = importlib.import_module("persistence.SurveyTypeListMongo")
    PersistentSurveyTypeList = PersistentLocationListModule.PersistentSurveyTypeList(
        mongoDb[reefwatchLocationOptions["survey_type_collection"]]
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

        if hasattr(options, 'logging'):
            if options.logging.upper() == 'DEBUG':
                self.logger.setLevel(logging.DEBUG)
            elif options.logging.upper() == 'WARNING':
                self.logger.setLevel(logging.WARNING)
            else:
                self.logger.setLevel(logging.INFO)
        elif hasattr(options, 'debug') and options.debug:
            self.logger.setLevel(logging.DEBUG)

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
                    persistentLocationEntityObj=PersistentLocationEntity
                )
            ),
            (
                r"/field_days/({id})/tides".format(id=mongoIdRegex),
                FieldDayTidesHandler,
                dict(persistentEntityObj=PersistentFieldDayTidesEntity)
            ),
            (
                r"/field_days/({field_day_id})/sites/({site_code})/surveys".format(
                    field_day_id=mongoIdRegex,
                    site_code=r"[a-zA-Z]{2,}"
                ),
                FieldDaySurveyListHandler,
                dict(
                    persistentFieldDaySurveyListObj=PersistentFieldDaySurveyList
                )
            ),
            (
                r"/field_days/({field_day_id})/sites/({site_code})/observations".format(
                    field_day_id=mongoIdRegex,
                    site_code=r"[a-zA-Z]{2,}"
                ),
                FieldDaySiteObservationsHandler,
                dict(
                    persistentFieldDaySiteEntityObj=PersistentFieldDaySite
                )
            ),
            (
                r"/field_days/({field_day_id})/sites/({site_code})".format(field_day_id=mongoIdRegex, site_code=r"[a-zA-Z]{2,}"),
                FieldDaySiteHandler,
                dict(
                    persistentFieldDaySiteEntityObj=PersistentFieldDaySite
                )
            ),
            (
                r"/field_days/({id})/sites".format(id=mongoIdRegex),
                FieldDaySiteListHandler,
                dict(
                    persistentFieldDaySiteListObj=PersistentFieldDaySiteList,
                    persistentLocationEntityObj=PersistentLocationEntity,
                    persistentFieldDayEntityObj=PersistentFieldDayEntity
                )
            ),
            (r"/field_days/({id})".format(id=mongoIdRegex), FieldDayHandler, dict(persistentEntityObj=PersistentFieldDayEntity)),
            (r"/locations/({id})/sites".format(id=mongoIdRegex), SiteListHandler, dict(persistentEntityListObj=PersistentLocationSiteList)),
            (r"/locations/({id})".format(id=mongoIdRegex), LocationHandler, dict(persistentLocationEntityObj=PersistentLocationEntity)),
            (r"/locations", LocationListHandler, dict(persistentLocationListObj=PersistentLocationList)),
            (r"/surveys", SurveyTypeListHandler, dict(persistentSurveyListObj=PersistentSurveyTypeList)),
            (r"/auth/success", BaseAuthenticatedHandler),
            (r"/auth/logout", LogoutHandler)
        ]

        # Google OAuth2 Settings
        if hasattr(options, "google_client_id"):
            google_oauth = {"key": options.google_client_id, "secret": options.google_client_secret}
            settings["google_oauth"] = google_oauth
            if hasattr(options, "google_auth_callback"):
                googleAuthCallback = options.google_auth_callback
            else:
                googleAuthCallback = "auth/callback/google"
            from authHandler import GoogleLoginHandler
            handlers.append((
                r"/auth/login/google",
                GoogleLoginHandler,
                dict(callbackPath=googleAuthCallback)
            ))
            handlers.append((
                r"/auth/callback/google",
                GoogleLoginHandler,
                dict(callbackPath=googleAuthCallback)
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
    http_server.xheaders = True
    http_server.listen(options.port)
    print "Listening on port: {port}".format(port=options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
