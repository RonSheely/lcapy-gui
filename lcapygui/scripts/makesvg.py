from lcapygui.ui.uimodelbase import UIModelBase
from lcapygui.components.cpt_maker import cpt_make


def make(cpt_type):

    cpt = cpt_make(cpt_type, '')
    print(cpt_type)

    kinds = cpt.kinds
    for kind in kinds:
        if kind != '':
            cpt = cpt_make(cpt_type, kind=kind)
            print(cpt_type, kind)


for k, v in UIModelBase.component_map.items():

    cpt_type = v[1]
    make(cpt_type)


for k, v in UIModelBase.connection_map.items():

    cpt_type = v[1]
    make(cpt_type)
