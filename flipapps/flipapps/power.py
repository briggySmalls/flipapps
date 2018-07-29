from typing import Dict

import RPi.GPIO as GPIO


class PowerManager(object):
    def __init__(self, pins: Dict[str, int]):
        GPIO.setmode(GPIO.BOARD)
        self.pins = pins

        # Configure the pins as outputs
        GPIO.setup(self.pins['sign'], GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.pins['light'], GPIO.OUT, initial=GPIO.LOW)

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        # Cleanup GPIO usage
        GPIO.cleanup()

    def light(self, status: bool):
        self._write_pin(self.pins['light'], status)

    def sign(self, status: bool):
        self._write_pin(self.pins['sign'], status)

    @staticmethod
    def _write_pin(pin: int, status: bool):
        GPIO.output(pin, 1 if status else 0)