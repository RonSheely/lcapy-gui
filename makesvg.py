from lcapygui.ui.uimodelbase import UIModelBase
from lcapygui.components.sketch import Sketch
from lcapygui.components.cpt_maker import cpt_make_from_type


def cpt_sketch_make(cpt, dstyle):

    Sketch.create(cpt.sketch_key, cpt.sketch_net, dstyle)


def make1(cpt_type, dstyle):

    print(cpt_type)
    cpt = cpt_make_from_type(cpt_type)
    cpt_sketch_make(cpt, dstyle)

    kinds = cpt.kinds
    styles = cpt.styles
    for kind in kinds:
        if styles == {}:
            print(cpt_type, kind)
            cpt = cpt_make_from_type(cpt_type, kind=kind)
            cpt_sketch_make(cpt, dstyle)
        else:
            for style in styles:
                print(cpt_type, kind, style)
                cpt = cpt_make_from_type(
                    cpt_type, kind=kind, style=style)
                cpt_sketch_make(cpt, dstyle)


def make(cpt_type):

    for dstyle in ('american', 'british', 'european'):
        make1(cpt_type, dstyle)


def make_all():

    for k, v in UIModelBase.component_map.items():

        cpt_type = v[2]
        make(cpt_type)

    for k, v in UIModelBase.connection_map.items():

        cpt_type = v[2]
        make(cpt_type)
