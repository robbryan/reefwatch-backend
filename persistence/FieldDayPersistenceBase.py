__author__ = "Paul Staszyc"
__copyright__ = "Copyright 2016, Paul Staszyc"

import tornado.concurrent

import logging
logger = logging.getLogger(__name__)


class PersistentFieldDayBase(object):

    def __init__(self):
        logger.warning("Abstract class created")
        pass

    def get(self):
        raise NotImplementedError


class PersistentFieldDayDummy(PersistentFieldDayBase):

    def __init__(self):
        pass

    @tornado.concurrent.return_future
    def get(self, fieldDayId, callback, **kwargs):

        dummyResult = {
            "id": str(fieldDayId),
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
        }

        callback(dummyResult)


if __name__ == "__main__":
    pass
