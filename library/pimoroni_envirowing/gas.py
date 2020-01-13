import time, board, digitalio, analogio
import pimoroni_physical_feather_pins

_is_setup = False

class Mics6814Reading(object):
    __slots__ = 'oxidising', 'reducing', 'nh3'

    def __init__(self, ox, red, nh3):
        self.oxidising = ox
        self.reducing = red
        self.nh3 = nh3

    def __repr__(self):
        fmt = """Oxidising: {ox:05.03f} Volts
Reducing: {red:05.03f} Volts
NH3: {nh3:05.03f} Volts"""
        return fmt.format(
            ox=self.oxidising,
            red=self.reducing,
            nh3=self.nh3)

    __str__ = __repr__


def setup():
    global _is_setup, enable, OX, RED, NH3
    if _is_setup:
        return
    _is_setup = True


    #enable = digitalio.DigitalInOut(board.A4)
    enable = digitalio.DigitalInOut(pimoroni_physical_feather_pins.pin9())
    enable.direction = digitalio.Direction.OUTPUT
    enable.value = True

    #OX = analogio.AnalogIn(board.A2)
    OX = analogio.AnalogIn(pimoroni_physical_feather_pins.pin7())
    #RED = analogio.AnalogIn(board.A1)
    RED = analogio.AnalogIn(pimoroni_physical_feather_pins.pin6())
    #NH3 = analogio.AnalogIn(board.A0)
    NH3 = analogio.AnalogIn(pimoroni_physical_feather_pins.pin5())


def cleanup():
    enable.value = False


def read_all():
    """Return gas resistance for oxidising, reducing and NH3"""
    setup()

    try:
        ox = OX.value * (OX.reference_voltage / 65535)
    except ZeroDivisionError:
        ox = 0

    try:
        red = RED.value * (RED.reference_voltage / 65535)
    except ZeroDivisionError:
        red = 0

    try:
        nh3 = NH3.value * (NH3.reference_voltage / 65535)
    except ZeroDivisionError:
        nh3 = 0

    return Mics6814Reading(ox, red, nh3)


def read_oxidising():
    """Return gas resistance for oxidising gases.
    Eg chlorine, nitrous oxide
    """
    setup()
    return read_all().oxidising


def read_reducing():
    """Return gas resistance for reducing gases.
    Eg hydrogen, carbon monoxide
    """
    setup()
    return read_all().reducing


def read_nh3():
    """Return gas resistance for nh3/ammonia"""
    setup()
    return read_all().nh3