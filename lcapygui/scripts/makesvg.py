from lcapygui.ui.uimodelbase import UIModelBase
from lcapygui.components.cpt_maker import cpt_make

for k, v in UIModelBase.component_map.items():

    cpt_type = v[1]
    cpt = cpt_make(cpt_type, '')
    print(cpt_type)

    kinds = cpt.kinds
    for kind in kinds:
        if kind != '':
            cpt = cpt_make(cpt_type, kind=kind)
            print(cpt_type, kind)
