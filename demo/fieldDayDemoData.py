from bson import objectid

fieldDayList = [
    {
        "_id": objectid.ObjectId("573e765fc1ed602daf609007"),
        "date": "2015-03-05",
        "description": "Aldinga North - March 2015",
        "location_id": objectid.ObjectId('574199a764cc93726de9e044'),
        "location": "Aldinga North",
        "tides": {
            "high": {"time": "04:40", "height": 1.94},
            "low": {"time": "10:30", "height": 0.53}
        },
        "leader_id": "1000",
        "sites": [
            {
                "site_code": "ANU",
                "observations": {
                    "time": "12:42:00",
                    "weather": {
                        "wind_direction": "NW",
                        "wind_force": 1,
                        "amount_of_cloud": 3,
                        "rainfall": 0,
                        "comments": "Weather Comments"
                    },
                    "volunteers": ["user1@gmail.com", "user2@gmail.com"]
                },
                "surveys": [
                    {
                        "survey_type": "PIT",
                        "comments": "Survey Comments"
                    }
                ]
            },
            {
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
        ]
    },
    {
        "_id": objectid.ObjectId("573e7696c1ed602daf609008"),
        "date": "2015-03-05",
        "description": "Aldinga South - March 2015",
        "location_id": objectid.ObjectId('57419a1364cc93726de9e045'),
        "location": "Aldinga South",
        "leader_id": "1000",
        "sites": [
            {
                "site_code": "ASU",
                "observations": {
                    "time": "10:20:00",
                    "weather": {
                        "wind_direction": "W",
                        "wind_force": 1,
                        "amount_of_cloud": 5,
                        "rainfall": 0,
                        "comments": "ASU - Weather Comments"
                    }
                },
                "surveys": [
                    {
                        "survey_type": "PIT",
                        "comments": "ASU PIT - Survey Comments"
                    }
                ]
            }
        ],
        "tides": {
            "high": {"time": "02:50:00", "height": 0.80},
            "low": {"time": "07:01:00", "height": 0.46}
        }
    },
    {
        "_id": objectid.ObjectId("573e76b2c1ed602daf609009"),
        "date": "2015-10-12",
        "description": "Lady Bay North - October 2015",
        "location_id": objectid.ObjectId('57419a1b64cc93726de9e046'),
        "location": "Lady Bay North",
        "leader_id": "1000"
    },
    {
        "_id": objectid.ObjectId("573e76c0c1ed602daf60900a"),
        "date": "2015-12-03",
        "description": "Lady Bay South - December 2015",
        "location_id": objectid.ObjectId('57419a3764cc93726de9e047'),
        "location": "Lady Bay South",
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
                "description": "Upper"
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

surveyTypeList = [
    {
        "_id": objectid.ObjectId('57429708c1ed60103845f42a'),
        "survey_code": "ITS",
        "name": "Intertidal Timed Search",
        "question": "How many different marine invertabrate species are found at this site?",
        "method": """Count intertidal species during a random search over a 10 minute period (per person). Volunteers should cover the area approximately 5-10 metres of each side of the transect to stay within the relevant intertidal zone."""
    },
    {
        "_id": objectid.ObjectId('574299bcc1ed60103845f42b'),
        "survey_code": "PIT",
        "name": "Intertidal Point Intercept Transect",
        "question": "How do cover and sediment depth vary over space and time?",
        "method": """Set up the 20 m transect at one of the permanent transect sites, parallel to the shoreline. Record the substrate cover (tick) and sedament depth (mm) every 20 cm."""
    },
    {
        "_id": objectid.ObjectId('57429ac9c1ed60103845f42c'),
        "survey_code": "SQS",
        "name": "Intertidal Mobile Species Quadrat Survey",
        "question": "How does the abundance of mobile reef animals change in the area over time?",
        "method": """2 x 20m transects, 50 cm apart, parallel to the shoreline. Equipment: two tape measures, or 20 m lengths of rope and 10 stakes (about 50 cm long).Sections are marked at 2 m intervals to make 10 rectangles of 2 m long x 50 cm wide. Individuals are counted on in five rectangles at 0-2, 4-6, 8-10, 12-14 and 16-18 m. Individuals are only counted if they are bigger than 5 mm in length."""
    }
]

userList = [
    {
        "_id": objectid.ObjectId('57849bdf64cc932fc08858d3'),
        "handle": "Billy Moon",
        "full_name": "Christopher Robin",
        "email_addresses": [
            {
                "email": "christopher.robin@hundred.acre.wood",
                "status": "active",
                "create_date_time": "2016-05-03 09:38:17",
                "provider_user_id": "2F49940F92295CAB2AC96896"
            }
        ],
        "status": "active",
        "create_date_time": "2016-05-03 09:38:17",
        "roles": ['admin']
    }
]