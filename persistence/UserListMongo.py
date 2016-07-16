__author__ = "Paul Staszyc"
__copyright__ = "Copyright 2016, Paul Staszyc"

import tornado.concurrent
from baseHandler import BaseEntityListHandler
from datetime import datetime
import pymongo.errors
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class PersistentUserList(BaseEntityListHandler):

    def __init__(self, mongoDbCollection):
        self.__mongoDbCollection__ = mongoDbCollection

    @tornado.concurrent.return_future
    def get(self, callback, limit=100, offset=0, **kwargs):
        assert(type(limit) == int)
        assert(limit > 0)
        assert(type(offset) == int)
        mongoQuery = {}
        if "query" in kwargs:
            logger.debug("Query: {0}".format(kwargs["query"]))
            query = kwargs["query"]
            if "full_name" in query:
                mongoQuery["full_name"] = query["full_name"]
            if "email" in query:
                mongoQuery["email_addresses"] = { "$elemMatch": { 'email': query["email"] } }

        """
        BEWARE!
        skip() and limit() are costly for large data sets. Beware
        See https://docs.mongodb.org/manual/reference/method/cursor.skip/#cursor.skip for more
        """
        userCursor = self.__mongoDbCollection__.find(
            mongoQuery,
            {
                "user_handle": 1,
                "full_name": 1,
                "email_addresses.email": 1
            }
        ).skip(((offset)*limit) if offset > 0 else 0).limit(limit)
        resultList = list()
        for result in userCursor:
            user = result
            # Replace ObjectId with string its representation
            user["id"] = str(user.pop("_id"))
            resultList.append(user)

        callback((resultList, self.__mongoDbCollection__.count()))

    @tornado.concurrent.return_future
    def add(self, callback, userFullName, userHandle, emailAddress, providerGeneratedId):
        logger.warning("Preparing to add user")
        user = {
            "user_handle": userHandle,
            "full_name": userFullName,
            "email_addresses": [
                {"email": emailAddress, "status": "active", "create_date_time": datetime.utcnow(), "provider_user_id": providerGeneratedId}
                ],
            "status": "active",
            "create_date_time": datetime.utcnow(),
            "roles": ['provisional']
        }
        try:
            result = self.__mongoDbCollection__.insert_one(user)
        except pymongo.errors.DuplicateKeyError as exDupKey:
            raise ValueError(
                "The User with ID '{id}' already exists".format(
                    id=user["_id"]
                )
            )

        callback(str(result.inserted_id))


if __name__ == "__main__":
    pass
