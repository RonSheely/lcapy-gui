from lcapygui.ui.uimodelbase import UIModelBase
from lcapygui.components.cpt_maker import cpt_make

for k, v in UIModelBase.component_map.items():

    cpt_type = v[1]
    cpt = cpt_make(cpt_type, '')
    print(cpt_type)

    kinds = cpt.kinds
    for k, v in kinds.items():
        print(cpt_type, k, v)
        if k != '':
            cpt = cpt_make(cpt_type, kind=k)
