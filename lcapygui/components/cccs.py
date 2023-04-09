from .controlledcomponent import ControlledComponent


class CCCS(ControlledComponent):

    type = "F"
    args = ('Control', 'Value')

    netitem_args = ['X']
