# reefwatch-backend
[![Build Status](https://travis-ci.org/pablo-libre/reefwatch-backend.svg?branch=master)](https://travis-ci.org/pablo-libre/reefwatch-backend)

## Setup
You will need [Tornado](https://tornadoweb.org) light-weight, non-blocking webserver installed and some libraries

```
sudo apt-get install python-setuptools
sudo easy_install tornado
```

For Mongo DB support, you will need pymongo as well as mongomock for unit testing
```
sudo easy_install pymongo mongomock
```

## Configuration
Some reasonable defaults are defined in localSettings.py.sample for you to use. You might like to copy that file to localSettings.py and edit it to your liking.

At the very least, you must specify a 'cookie_secret' for encrypting secure cookies.
Look for the line "define("cookie_secret", default=None, help="Encryption key used for ecrypting secure cookies")" and replace the default with your own value.

If you wish to use **MongoDB**, you must define the relevant options in localSettings.py.
There are some sane defaults in the localSettings.py.sample provided. Start with those
```
""" Define MongoDB connection and database details """
define("mongo_instance", type=str, group="persistence", default=None, help="host:port for MongoDB instance")
define("mongo_database", type=str, group="persistence", default="reefwatch_dev", help="Name of the Reef Watch database on the MongoDB instance")
define("mongo_user", type=str, group="persistence", default=None, help="Username used to authenticate to MongoDB")
define("mongo_password", type=str, group="persistence", default=None, help="Password used to authenticate to MongoDB")

""" Define Mongo collection 
define("field_day_collection", type=str, group="field_day", default="field_day", help="Name of Field Day collection on MongoDB")
define("survey_location_collection", type=str, group="location", default="survey_location", help="Name of Survey Location collection on MongoDB")
define("survey_site_collection", type=str, group="site", default="survey_site", help="Name of Survey Site collection on MongoDB")
```
## Running

Most simply, you can just run the app with python and background it
```
python app.py &
```
You can then check that it is running by using curl or your favourite browser
```
curl http://localhost:9880
```
Settings are loaded from localSettings.py (see localSettings.py.sample for examples)

There is also a multitude of command-line options you can pass too - Check documentation at http://tornadoweb.org for details
```
python app.py --port=8888 --logging=debug --debug=1 &
```
## Calling the API
The purpose of the API is to facilitate the collection and management of observations undertaken as part of Conservation SA's Reefwatch program.

The structure of of the API creates a hierarchy of location-and-date -> site -> survey -> discrete observations
```
- Location & Date
| - Tides
| - Sites
| | - Site 1
| | | - Survey 1
| | | | - Survey Type
| | | | - Weather
| | | | - Observations
| | | | | - discrete observation
| | - Site 2
```
The API is RESTful and so most branches in the hierarchy can be used to retrieve a collection/list or an individual item using its ID

For example, you can get a list of field days like this
```
http://localhost:9881/field_days
```
and get an individual field day using its ID
```
http://localhost:9881/field_days/573e765fc1ed602daf609007
```

List of routes
```
/field_days
/field_days/{id}
/field_days/{id}/tides
/field_days/{id}/sites
/locations
/locations/{id}
```
