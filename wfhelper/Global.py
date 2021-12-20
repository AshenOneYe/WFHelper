from .State import State
from .Config import Config
from ppadb.device import Device


class Global:
    device: Device = None
    state = State()
    config = Config()


WFGlobal = Global()
