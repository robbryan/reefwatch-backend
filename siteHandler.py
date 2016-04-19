"""
    This is the Request handler for Sites
"""

__author__    = "Paul Staszyc"
__copyright__ = "Copyright 2016"


from baseHandler import BaseHandler


class SiteListHandler(BaseHandler):

    def initialize(self, persistentEntityListObj):
        self.__persistentEntityListObj__ = persistentEntityListObj

    def get(self, location=None):
        entityListGetter = self.__persistentEntityListObj__
        entityList, totalRecordCount = entityListGetter.get()
        self.write({"data": entityList})


if __name__ == "__main__":
    pass