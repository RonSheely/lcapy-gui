from lcapygui.ui.uimodelbase import UIModelBase
from lcapygui.core.sketch import Sketch
from lcapygui.core.cpt_maker import gcpt_make_from_type


def cpt_sketch_make(cpt, dstyle):

    Sketch.create(cpt.sketch_key, cpt.sketch_net, dstyle)


def make1(thing, dstyle):

    gcpt = gcpt_make_from_type(thing.cpt_type, kind=thing.kind)
    print(gcpt.sketch_key, '\t', gcpt.sketch_net)
    cpt_sketch_make(gcpt, dstyle)

    if thing.kind:
        # Don't make other connections; make_connections
        # chooses which to make.
        return

    kinds = gcpt.kinds
    styles = gcpt.styles
    for kind in kinds:
        if styles == {}:
            gcpt = gcpt_make_from_type(thing.cpt_type, kind=kind)
            print(gcpt.sketch_key, '\t', gcpt.sketch_net)
            cpt_sketch_make(gcpt, dstyle)
        else:
            for style in styles:
                gcpt = gcpt_make_from_type(
                    thing.cpt_type, kind=kind, style=style)
                print(gcpt.sketch_key, '\t', gcpt.sketch_net)
                cpt_sketch_make(gcpt, dstyle)


def make(thing):

    if thing.cpt_type == 'DW':
        return

    for dstyle in ('american', 'british', 'european'):
        make1(thing, dstyle)


def make_connections():

    for thing in UIModelBase.connection_map.values():

        make(thing)


def make_components():

    for thing in UIModelBase.component_map.values():

        make(thing)


def make_cpt(cpt_type):

    make(UIModelBase.component_map[cpt_type])


def make_all():

    make_connections()
    make_components()

# make_all()

print('Do not forget to install for these changes to take affect.')
