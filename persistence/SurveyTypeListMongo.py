__author__ = "Paul Staszyc"
__copyright__ = "Copyright 2016, Paul Staszyc"

import tornado.concurrent

import logging
logger = logging.getLogger(__name__)


class PersistentSurveyTypeList(object):

    def __init__(self, mongoDbCollection):
        self.__mongoDbCollection__ = mongoDbCollection

    @tornado.concurrent.return_future
    def get(self, callback, limit=100, offset=0, **kwargs):
        assert(type(limit) == int)
        assert(limit > 0)
        assert(type(offset) == int)
        mongoQuery = {}
        if "query" in kwargs:
            mongoQuery = {}
            logger.info("Query: {0}".format(kwargs["query"]))
            query = kwargs["query"]
            if "name" in query:
                mongoQuery["name"] = {"regex": r"(?i){0}".format(query["name"])}

        surveyTypeCursor = self.__mongoDbCollection__.find(
            mongoQuery,
            {
                "survey_code": 1,
                "name": 1
            }
        )
        resultList = list()
        for result in surveyTypeCursor:
            surveyType = result
            # Replace ObjectId with string its representation
            surveyType["id"] = str(surveyType.pop("_id"))

            resultList.append(surveyType)

        callback((resultList[offset:(limit+offset)], self.__mongoDbCollection__.count()))


if __name__ == "__main__":
    pass
