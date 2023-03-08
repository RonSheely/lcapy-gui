from lcapygui.ui.uimodelbase import UIModelBase
from lcapygui.components.cpt_maker import cpt_make


def make(cpt_type):

    cpt = cpt_make(cpt_type, '', create=True)
    print(cpt_type)

    kinds = cpt.kinds
    styles = cpt.styles
    for kind in kinds:
        if styles == {}:
            cpt = cpt_make(cpt_type, kind=kind, create=True)
            print(cpt_type, kind)
        else:
            for style in styles:
                cpt = cpt_make(cpt_type, kind=kind, style=style, create=True)
                print(cpt_type, kind, style)
    return cpt


def make_all():

    for k, v in UIModelBase.component_map.items():

        cpt_type = v[1]
        make(cpt_type)

    for k, v in UIModelBase.connection_map.items():

        cpt_type = v[1]
        make(cpt_type)
