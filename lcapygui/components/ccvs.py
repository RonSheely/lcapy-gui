from .controlledcomponent import ControlledComponent


class CCVS(ControlledComponent):

    type = "H"
    args = ('Control', 'Value')

    netitem_args = ['X']
