from .transistor import Transistor


class JFET(Transistor):

    type = "J"
    label_offset = 0
    can_stretch = True
    angle_offset = 90

    kinds = {}

    # TODO: add gate offset
