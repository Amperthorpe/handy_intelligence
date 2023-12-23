import logging
from configparser import ConfigParser

logger = logging.getLogger(__name__)

logger.info("Config Handler init")
config = ConfigParser()
config.read("config.cfg")
