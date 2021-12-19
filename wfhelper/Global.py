from .State import State
from .Config import Config
from ppadb.device import Device


GlobalState = State()
GlobalConfig = Config()
device: Device = None
