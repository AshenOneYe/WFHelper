import logging
import sys
import time
from typing import Any, Callable, List


# TODO 现在多个实例共用同一个LogUtil，应该分离
class LogUtil:
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    DATE_FORMAT = "%Y/%m/%d %H:%M:%S"

    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT)

    logAppendEvent = None

    logArray = []  # type: List[Any]
    logLimit = 20

    def setDebugLevel(self):
        logging.getLogger().setLevel(logging.DEBUG)

    def onLogAppend(self, callback: Callable):
        self.logAppendEvent = callback

    def append(self, logdata: str):
        log = {"time": int(time.time()), "message": logdata}

        self.logArray.append(log)

        if len(self.logArray) > self.logLimit:
            self.logArray.pop(0)

        if self.logAppendEvent is not None:
            self.logAppendEvent(log)

    def debug(self, msg: str):
        logging.debug(msg)

    def info(self, msg: str):
        logging.info(msg)
        self.append(msg)

    def warning(self, msg: str):
        logging.warning(msg)

    def error(self, msg: str):
        logging.error(msg)
        sys.stderr.write(msg+"\n")
        sys.exit()

    def critical(self, msg: str):
        logging.critical(msg)
        sys.stderr.write(msg+"\n")
        sys.exit()


Log = LogUtil()
