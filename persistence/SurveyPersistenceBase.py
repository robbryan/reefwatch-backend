__author__ = "Paul Staszyc"
__copyright__ = "Copyright 2016, Paul Staszyc"

import logging
logger = logging.getLogger(__name__)


class PersistentSurveyTypeBase(object):

    def __init__(self):
        logger.warning("Abstract class created")
        pass

    def get(self):
        raise NotImplementedError

    def add(self):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError


class PersistentServeyTypeDummy(PersistentSurveyTypeBase):

    def __init__(self):
        pass

    def get(self):
        pass

if __name__ == "__main__":
    pass
