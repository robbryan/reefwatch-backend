__author__ = "Paul Staszyc"
__copyright__ = "Copyright 2016, Paul Staszyc"

import tornado.concurrent

from persistence.FieldDayPersistenceBase import PersistentFieldDayBase
from persistence.FieldDayListPersistenceBase import PersistentFieldDayListBase

import uuid
import logging
logger = logging.getLogger(__name__)

class PersistentFieldDayListDummy(PersistentFieldDayListBase):

    def __init__(self):
        pass

    @tornado.concurrent.return_future
    def add(self, callback, fieldDay):
        callback(str(uuid.uuid1()))

    @tornado.concurrent.return_future
    def get(self, callback, limit=100, offset=0, **kwargs):
        logger.info("Limit: {0}\tOffset: {1}".format(limit, offset))
        assert(type(limit) == int)
        assert(limit > 0)
        assert(type(offset) == int)
        if "query" in kwargs:
            logger.info("Query: {0}".format(kwargs["query"]))
            query = kwargs["query"]

        dummyResult = __dummyData__

        callback ((dummyResult[offset:(limit+offset)], len(dummyResult)))


class PersistentFieldDayDummy(PersistentFieldDayBase):

    def __init__(self):
        pass

    @tornado.concurrent.return_future
    def get(self, fieldDayId, callback, **kwargs):

        filteredList = filter(lambda x: x["id"] == fieldDayId, __dummyData__)

        callback(filteredList[0] if len(filteredList) > 0 else None)


class PersistentFieldDayTidesDummy(PersistentFieldDayBase):

    def __init__(self):
        pass

    @tornado.concurrent.return_future
    def get(self, fieldDayId, callback, **kwargs):

        filteredList = filter(lambda x: x["id"] == fieldDayId, __dummyData__)

        tides = None
        if len(filteredList) > 0:
            fieldDay = filteredList[0]
            tides = fieldDay["tides"] if "tides" in fieldDay else None

        callback(tides)


__dummyData__ = [
    {
        "id": "1000",
        "date": "2015-03-05",
        "description": "Aldinga North - March 2015",
        "location_id": "1000",
        "tides": {
            "high": {"time": "04:40", "height": 1.94},
            "low": {"time": "10:30", "height": 0.53}
        },
        "leader_id": "1000",
        "sites": [
            {
                "site_id": "1000",
                "site_code": "ANU",
                "surveys": [
                    {
                        "survey_type": "PIT",
                        "time": "12:30:00",
                        "weather": {
                            "wind_direction": "NW",
                            "wind_force": 1,
                            "amount_of_cloud": 3,
                            "rainfall": 0,
                            "comments": "Weather Comments"
                        },
                        "sea_state": 2,
                        "comments": "Survey Comments"
                    }
                ]
            },
            {
                "site_id": "2000",
                "site_code": "ANM",
                "surveys": [
                    {
                        "survey_type": "Timed Search",
                        "time": "13:00:00",
                        "weather": {
                            "wind_direction": "NW",
                            "wind_force": 1,
                            "amount_of_cloud": 3,
                            "rainfall": 0,
                            "comments": "Weather Comments"
                        },
                        "comments": "Survey Comments"
                    },
                    {
                        "survey_type": "MSQ Search",
                        "time": "13:30:00",
                        "weather": {
                            "wind_direction": "NW",
                            "wind_force": 2,
                            "amount_of_cloud": 5,
                            "rainfall": 1,
                            "comments": "Weather Comments"
                        },
                        "comments": "Survey Comments"
                    }
                ]
            }
        ],
        "volunteers": [] # calculated from child-surveys
    },
    {
        "id": "1100",
        "date": "2015-03-05",
        "description": "Aldinga South - March 2015",
        "location_id": "2000",
        "leader_id": "1000",
        "sites": [],
        "tides": {"high": {"time": "04:17", "height": 2.01}}
    },
    {
        "id": "1200",
        "date": "2015-10-12",
        "description": "Lady Bay North - October 2015",
        "location_id": "3000",
        "leader_id": "1000",
        "sites": []
    },
    {
        "id": "1300",
        "date": "2015-12-03",
        "description": "Lady Bay South - December 2015",
        "location_id": "4000",
        "leader_id": "1000",
        "sites": []
    }
]


if __name__ == "__main__":
    pass
