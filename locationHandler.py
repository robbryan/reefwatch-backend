"""
    This is the Request handler for Locations - List, add, get, update
"""

__author__    = "Paul Staszyc"
__copyright__ = "Copyright 2016"


from baseHandler import BaseEntityListHandler


class LocationListHandler(BaseEntityListHandler):

    def initialize(self, persistentLocationListObj):
        self.__persistentLocationListObj__ = persistentLocationListObj

    def get(self):
        pageSize, pageNum = self.getPageSizeAndNum()
        offset = (pageNum-1)*pageSize
        limit = pageSize
        locationListGetter = self.__persistentLocationListObj__
        locationList, totalRecordCount = locationListGetter.get(
            limit=limit,
            offset=offset
            )
        self.setResponseHeaders(
            pageNum=pageNum,
            pageSize=pageSize,
            totalRecordCount=totalRecordCount
        )
        self.write({"data": locationList})


if __name__ == "__main__":
    pass
