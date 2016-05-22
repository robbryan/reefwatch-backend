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
        "location_id": objectid.ObjectId('57419a1364cc93726de9e045'),
        "leader_id": "1000",
        "sites": []
    },
    {
        "_id": objectid.ObjectId("573e76b2c1ed602daf609009"),
        "date": "2015-10-12",
        "description": "Lady Bay North - October 2015",
        "location_id": objectid.ObjectId('57419a1b64cc93726de9e046'),
        "leader_id": "1000"
    },
    {
        "_id": objectid.ObjectId("573e76c0c1ed602daf60900a"),
        "date": "2015-12-03",
        "description": "Lady Bay South - December 2015",
        "location_id": objectid.ObjectId('57419a3764cc93726de9e047'),
        "leader_id": "1000",
        "tides": {}
    }
]

locationList = [
    {
        "_id": objectid.ObjectId('574199a764cc93726de9e044'),
        "description": "Aldinga North",
        "location_code": "AN",
        "sites": [
            {
                "site_code": "ANU",
                "description": "Upper"
            },
            {
                "site_code": "ANM",
                "description": "Middle"
            },
            {
                "site_code": "ANL",
                "description": "Lower"
            }
        ]
    },
    {
        "_id": objectid.ObjectId('57419a1364cc93726de9e045'),
        "description": "Aldinga South",
        "location_code": "AS",
        "sites": [
            {
                "site_code": "ASU",
                "description": "Upper"
            },
            {
                "site_code": "ASM",
                "description": "Middle"
            },
            {
                "site_code": "ASL",
                "description": "Lower"
            }
        ]
    },
    {
        "_id": objectid.ObjectId('57419a1b64cc93726de9e046'),
        "description": "Lady Bay North",
        "location_code": "LBN",
        "sites": [
            {
                "site_code": "LBNU",
                "description": "LBUpper"
            },
            {
                "site_code": "LBNM",
                "description": "Middle"
            },
            {
                "site_code": "LBNL",
                "description": "Lower"
            }
        ]
    },
    {
        "_id": objectid.ObjectId('57419a3764cc93726de9e047'),
        "description": "Lady Bay South",
        "location_code": "LBS",
        "sites": [
            {
                "site_code": "LBSU",
                "description": "Upper"
            },
            {
                "site_code": "LBSM",
                "description": "Middle"
            },
            {
                "site_code": "LBSL",
                "description": "Lower"
            }
        ]
    },
    {
        "_id": objectid.ObjectId('57419a4964cc93726de9e048'),
        "description": "Hallett Cove",
        "location_code": "HC",
        "sites": [
            {
                "site_code": "HCU",
                "description": "Upper"
            },
            {
                "site_code": "HCM",
                "description": "Middle"
            },
            {
                "site_code": "HCL",
                "description": "Lower"
            }
        ]
    },
    {
        "_id": objectid.ObjectId('57419a5864cc93726de9e049'),
        "description": "Victor Harbor",
        "location_code": "YB",
        "sites": [
            {
                "site_code": "YBU",
                "description": "Upper"
            },
            {
                "site_code": "YBM",
                "description": "Middle"
            },
            {
                "site_code": "YBL",
                "description": "Lower"
            }
        ]
    },
    {
        "_id": objectid.ObjectId('57419a6964cc93726de9e04a'),
        "description": "Beachport",
        "location_code": "B",
        "sites": [
            {
                "site_code": "BU",
                "description": "Upper"
            },
            {
                "site_code": "BM",
                "description": "Middle"
            },
            {
                "site_code": "BL",
                "description": "Lower"
            }
        ]
    },
    {
        "_id": objectid.ObjectId('57419a7964cc93726de9e04b'),
        "description": "Robe",
        "location_code": "R",
        "sites": [
            {
                "site_code": "RU",
                "description": "Upper"
            },
            {
                "site_code": "RM",
                "description": "Middle"
            },
            {
                "site_code": "RL",
                "description": "Lower"
            }
        ]
    },
    {
        "_id": objectid.ObjectId('57419a8c64cc93726de9e04c'),
        "description": "Port Macdonnell",
        "location_code": "PM",
        "sites": [
            {
                "site_code": "PMU",
                "description": "Upper"
            },
            {
                "site_code": "PMM",
                "description": "Middle"
            },
            {
                "site_code": "PML",
                "description": "Lower"
            }
        ]
    }
]