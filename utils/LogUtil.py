import logging
import time
from typing import List

# FIXME 现在多个实例共用同一个LogUtil，应该分离
class LogUtil:
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    DATE_FORMAT = "%Y/%m/%d %H:%M:%S"

    logging.basicConfig(
        level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT
    )

    logAppendEvent = None

    logArray = []  # type: List[str]
    logLimit = 20

    def setDebugLevel(self):
        logging.getLogger().setLevel(logging.DEBUG)

    def onLogAppend(self, callback):
        self.logAppendEvent = callback

    def append(self, log):
        log = {
            "time": int(time.time()),
            "message": log
        }

        self.logArray.append(log)

        if len(self.logArray) > self.logLimit:
            self.logArray.pop(0)

        if self.logAppendEvent is not None:
            self.logAppendEvent(log)

    def debug(self, msg):
        logging.debug(msg)

    def info(self, msg):
        logging.info(msg)
        
        self.append(msg)

    def warning(self, msg):
        logging.warning(msg)

    def error(self, msg):
        logging.error(msg)

    def critical(self, msg):
        logging.critical(msg)


Log = LogUtil()
