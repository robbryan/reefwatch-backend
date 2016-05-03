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
from fieldDayHandler import FieldDayListHandler, FieldDayHandler

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

        PersistentFieldDayListModule = importlib.import_module("persistence.FieldDayListMongo")
        fieldDayOptions = options.group_dict("field_day")
        PersistentFieldDayList = PersistentFieldDayListModule.PersistentFieldDayList(
            mongoDb[fieldDayOptions["field_day_collection"]]
        )
        PersistentFieldDayModule = importlib.import_module("persistence.FieldDayMongo")
        PersistentFieldDayEntity = PersistentFieldDayModule.PersistentFieldDay(mongoDb[fieldDayOptions["field_day_collection"]])

try:
    if PersistentFieldDayList:
        pass
except NameError:
    print "Warning! No persistence engine was specified for Field Day List - See localSettings.py.sample for examples"
    print "Using Dummy persistence instead - That's ok for Demos"
    from persistence.FieldDayPersistenceDummy import PersistentFieldDayListDummy
    PersistentFieldDayList = PersistentFieldDayListDummy()

try:
    if PersistentFieldDayEntity:
        pass
except NameError:
    print "Warning! No persistence engine was specified for Field Day - See localSettings.py.sample for examples"
    print "Using Dummy persistence instead - That's ok for Demos"
    from persistence.FieldDayPersistenceDummy import PersistentFieldDayDummy
    PersistentFieldDayEntity = PersistentFieldDayDummy()


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world!")


class Application(tornado.web.Application):

    logger = logging.getLogger('ReefWatch Backend Event logger')

    def __init__(self):
        settings = dict(
            debug=options.debug if hasattr(options, 'debug') else False
        )

        self.logger.setLevel(
            logging.DEBUG if hasattr(options, 'debug') and options.debug else logging.INFO
        )

        """
            Regular Expression for matching GUIDs.
            Case-insensitive. With or without dashes. No curly braces
        """
        guidRegex = r"[0-9A-Fa-f]{8}-*[0-9A-Fa-f]{4}-*[0-9A-Fa-f]{4}-*[0-9A-Fa-f]{4}-*[0-9A-Fa-f]{12}"

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
            (r"/field_days/({guid})".format(guid=guidRegex), FieldDayHandler, dict(persistentEntityObj=PersistentFieldDayEntity)),
            (r"/surveys", SurveyListHandler, dict(persistentSurveyListObj=PersistentSurveyList())),
            (r"/locations/({guid})/sites".format(guid=guidRegex), SiteListHandler, dict(persistentEntityListObj=PersistentSiteList())),
            (r"/locations", LocationListHandler, dict(persistentLocationListObj=PersistentLocationList()))
        ]

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
