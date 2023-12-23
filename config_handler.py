import logging
from configparser import ConfigParser

logger = logging.getLogger(__name__)

logger.log("Config Handler init")
config = ConfigParser()
config.read("config.cfg")
