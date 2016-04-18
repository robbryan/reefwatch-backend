__author__ = "Paul Staszyc"
__copyright__ = "Copyright 2016, Paul Staszyc"

import logging
logger = logging.getLogger(__name__)


class PersistentSurveyBase(object):

    def __init__(self):
        logger.warning("Abstract class created")
        pass

    def save(self):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError


class PersistentServeyDummy(PersistentSurveyBase):

    def __init__(self):
        pass

    def save(self):
        pass

if __name__ == "__main__":
    pass
