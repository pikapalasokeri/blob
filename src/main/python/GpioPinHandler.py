import RPi.GPIO as gpio


class GpioOutPin:
    def __init__(self, pin):
        self.pin = pin

    def setHigh(self):
        gpio.output(self.pin, 1)

    def setLow(self):
        gpio.output(self.pin, 0)


class GpioPinHandler:
    class __GpioHandler:
        def __init__(self):
            gpio.setmode(gpio.BCM)
            self._outPins = []

        def registerOutPin(self, pin):
            if pin not in self._outPins:
                gpio.setup(pin, gpio.OUT)
                self._outPins.append(pin)
            return GpioOutPin(pin)

    _instance = None

    def __init__(self):
        if not GpioPinHandler._instance:
            GpioPinHandler._instance = GpioPinHandler.__GpioHandler()

    def __getattr__(self, attr):
        return getattr(self._instance, attr)

    def close(self):
        gpio.cleanup()
        GpioPinHandler._instance = None
