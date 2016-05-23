# reefwatch-backend

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
