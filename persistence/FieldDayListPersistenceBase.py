__author__ = "Paul Staszyc"
__copyright__ = "Copyright 2016, Paul Staszyc"

import tornado.concurrent

import logging
logger = logging.getLogger(__name__)


class PersistentFieldDayListBase(object):

    def __init__(self):
        logger.warning("Abstract class created")
        pass

    def add(self):
        raise NotImplementedError

    def get(self):
        raise NotImplementedError


class PersistentFieldDayListDummy(PersistentFieldDayListBase):

    def __init__(self):
        pass

    @tornado.concurrent.return_future
    def get(self, callback, limit=100, offset=0, **kwargs):
        logger.info("Limit: {0}\tOffset: {1}".format(limit, offset))
        assert(type(limit) == int)
        assert(limit > 0)
        assert(type(offset) == int)
        if "query" in kwargs:
            logger.info("Query: {0}".format(kwargs["query"]))
            query = kwargs["query"]

        dummyResult = [
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
                "sites": []
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

        callback ((dummyResult[offset:(limit+offset)], len(dummyResult)))


if __name__ == "__main__":
    pass
