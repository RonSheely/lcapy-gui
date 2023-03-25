from lcapygui.ui.uimodelbase import UIModelBase
from lcapygui.components.cpt_maker import cpt_sketch_make, cpt_make_from_type


def make(cpt_type):

    print(cpt_type)
    cpt = cpt_make_from_type(cpt_type)
    cpt_sketch_make(cpt)

    kinds = cpt.kinds
    styles = cpt.styles
    for kind in kinds:
        if styles == {}:
            print(cpt_type, kind)
            cpt = cpt_make_from_type(cpt_type, kind=kind)
            sketch = cpt_sketch_make(cpt)
        else:
            for style in styles:
                print(cpt_type, kind, style)
                cpt = cpt_make_from_type(cpt_type, kind=kind, style=style)
                sketch = cpt_sketch_make(cpt)
    return sketch


def make_all():

    for k, v in UIModelBase.component_map.items():

        cpt_type = v[1]
        make(cpt_type)

    for k, v in UIModelBase.connection_map.items():

        cpt_type = v[1]
        make(cpt_type)
