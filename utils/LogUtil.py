import logging
import time

from typing import List


class LogUtil:
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    DATE_FORMAT = "%Y/%m/%d %H:%M:%S"

    logging.basicConfig(
        level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT
    )

    lastLog = None

    logArray = []  # type: List[str]
    logLimit = 20

    def setLastLog(self, log):
        log = str(
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        ) + " " + log

        self.lastLog = log
        self.logArray.append(log)

        if len(self.logArray) > self.logLimit:
            self.logArray.pop(0)

    def debug(self, msg):
        self.setLastLog(msg)
        logging.debug(msg)

    def info(self, msg):
        self.setLastLog(msg)
        logging.info(msg)

    def warning(self, msg):
        self.setLastLog(msg)
        logging.warning(msg)

    def error(self, msg):
        self.setLastLog(msg)
        logging.error(msg)

    def critical(self, msg):
        self.setLastLog(msg)
        logging.critical(msg)


Log = LogUtil()
