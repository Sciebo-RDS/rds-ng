import logging

from .logger import Logger


logging.setLoggerClass(Logger)
logger = logging.getLogger("rds_logger")

logger.info("WELL HI THERE!")
logger.debug("DE...WHAT", scope="net", test=123)
logger.warning("UHUHUHOHOHOHOHOH :smile:")
logger.error("FUFUFU")
