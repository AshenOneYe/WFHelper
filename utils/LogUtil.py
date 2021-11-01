import logging

class LogUtil():
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    DATE_FORMAT = "%Y/%m/%d %H:%M:%S"

    logging.basicConfig(level=logging.DEBUG,format=LOG_FORMAT,datefmt=DATE_FORMAT)

    def debug(self,msg):
         logging.debug(msg)
    
    def info(self,msg):
         logging.info(msg)

    def warning(self,msg):
         logging.warning(msg)

    def error(self,msg):
         logging.error(msg)

    def critical(self,msg):
         logging.critical(msg)

    def __init__(self) -> None:
        pass

Log = LogUtil()