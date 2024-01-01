from .bipole import Bipole


class FerriteBead(Bipole):

    type = 'FB'
    has_value = False
    label_offset_pos = (0, -0.4)
    annotation_offset_pos = (0, 0.4)
