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
    callback = None

    def setDebugLevel(self):
        logging.getLogger().setLevel(logging.DEBUG)

    def setLastLog(self, log):
        if self.callback is not None:
            self.callback(
                {
                    "time": int(time.time()),
                    "data": log
                }
            )

        log = str(
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        ) + " {}".format(log)

        self.lastLog = log
        self.logArray.append(log)

        if len(self.logArray) > self.logLimit:
            self.logArray.pop(0)

    def debug(self, msg):
        logging.debug(msg)

    def info(self, msg):
        self.setLastLog(msg)
        logging.info(msg)

    def warning(self, msg):
        logging.warning(msg)

    def error(self, msg):
        logging.error(msg)

    def critical(self, msg):
        logging.critical(msg)

    def setCallback(self, callback):
        self.callback = callback


Log = LogUtil()
