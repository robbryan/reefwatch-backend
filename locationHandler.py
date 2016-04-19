"""
    This is the Request handler for Locations - List, add, get, update
"""

__author__    = "Paul Staszyc"
__copyright__ = "Copyright 2016"


from baseHandler import BaseHandler


class LocationListHandler(BaseHandler):

    def initialize(self, persistentLocationListObj):
        self.__persistentLocationListObj__ = persistentLocationListObj

    def get(self):
        locationListGetter = self.__persistentLocationListObj__
        locationList = locationListGetter.get()
        self.write({"data": locationList})


if __name__ == "__main__":
    pass
