from bson import objectid

fieldDayList = [
    {
        "_id": objectid.ObjectId("573e765fc1ed602daf609007"),
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
        "_id": objectid.ObjectId("573e7696c1ed602daf609008"),
        "date": "2015-03-05",
        "description": "Aldinga South - March 2015",
        "location_id": "2000",
        "leader_id": "1000",
        "sites": []
    },
    {
        "_id": objectid.ObjectId("573e76b2c1ed602daf609009"),
        "date": "2015-10-12",
        "description": "Lady Bay North - October 2015",
        "location_id": "3000",
        "leader_id": "1000"
    },
    {
        "_id": objectid.ObjectId("573e76c0c1ed602daf60900a"),
        "date": "2015-12-03",
        "description": "Lady Bay South - December 2015",
        "location_id": "4000",
        "leader_id": "1000",
        "sites": []
    }
]
