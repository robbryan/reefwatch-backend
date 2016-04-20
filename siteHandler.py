"""
    This is the Request handler for Sites
"""

__author__    = "Paul Staszyc"
__copyright__ = "Copyright 2016"


from baseHandler import BaseEntityListHandler


class SiteListHandler(BaseEntityListHandler):

    def initialize(self, persistentEntityListObj):
        self.__persistentEntityListObj__ = persistentEntityListObj

    def get(self, location=None):
        limit, offset = self.getLimitAndOffset()
        entityListGetter = self.__persistentEntityListObj__
        entityList, totalRecordCount = entityListGetter.get(
            limit=limit,
            offset=offset
            )
        self.write({"data": entityList})


if __name__ == "__main__":
    pass