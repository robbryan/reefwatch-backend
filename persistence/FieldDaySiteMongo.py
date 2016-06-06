__author__ = "Paul Staszyc"
__copyright__ = "Copyright 2016, Paul Staszyc"

import tornado.concurrent

from bson.objectid import ObjectId
import logging
logger = logging.getLogger(__name__)


class PersistentFieldDaySite(object):

    def __init__(self, mongoDbCollection):
        self.__mongoDbCollection__ = mongoDbCollection

    @tornado.concurrent.return_future
    def get(self, fieldDayId, siteCode, callback, **kwargs):

        if type(fieldDayId) in [str, unicode]:
            fieldDayId = ObjectId(fieldDayId)

        mongoQuery = {"_id": fieldDayId, "sites.site_code": siteCode}
        result = self.__mongoDbCollection__.find_one(
            mongoQuery
        )

        if result:
            fieldDaySite = filter(lambda x: x["site_code"] == siteCode, result["sites"])[0]
            callback(fieldDaySite)
        else:
            callback(None)


if __name__ == "__main__":
    pass
