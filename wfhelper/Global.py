from .State import State
from .Config import Config
from ppadb.device import Device


GlobalState = State()
GlobalConfig = Config()


class WFDevice:
    _device: Device = None

    def setDevice(self, _device: Device):
        self._device = _device

    def getDevice(self) -> Device:
        return self._device


device = WFDevice()
