from .transistor import Transistor


class BJT(Transistor):

    type = "Q"
    default_kind = 'npn-'

    kinds = {'npn-': 'NPN',
             'pnp-': 'PNP',
             'npn-nigbt': 'NPN IGBT',
             'pnp-pigbt': 'PNP IGBT gate',
             'npn-bodydiode': 'NPN with body diode',
             'pnp-bodydiode': 'PNP with body diode',
             'npn-nigbt-bodydiode': 'NPN IGBT with body diode',
             'pnp-pigbt-bodydiode': 'PNP IGBT with body diode',
             'npn-Lnigbt': 'L-shaped NPN IGBT',
             'pnp-Lpigbt': 'L-shaped PNP IGBT'}

    # TODO: add base offset for Lnigbt, Lpigbt

    pinname1 = 'c'
    pinname2 = 'e'

    node_pinnames = ('e', 'b', 'c')

    hh = 0.5
    hw = 0.55 / 2
    ppins = {'e': ('lx', -hw, -hh),
             'b': ('lx', -hw, -hh),
             'c': ('lx', -hw, hh)}
    npins = {'e': ('lx', -hw, hh),
             'b': ('lx', -hw, -hh),
             'c': ('lx', -hw, -hh)}
    ippins = {'e': ('lx', -hw, -hh),
              'b': ('lx', -hw, -hh),
              'c': ('lx', -hw, hh)}
    inpins = {'e': ('lx', -hw, hh),
              'b': ('lx', -hw, -hh),
              'c': ('lx', -hw, -hh)}
