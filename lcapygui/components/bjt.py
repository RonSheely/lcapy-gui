from .transistor import Transistor


class BJT(Transistor):

    type = "Q"
    default_kind = 'npn'

    kinds = {'npn': 'NPN',
             'pnp': 'PNP',
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

    node_pinnames = ('c', 'b', 'e')

    extra_fields = {'mirror': 'Mirror', 'invert': 'Invert'}

    ppins = {'e': ('lx', 0.225, -0.5),
             'b': ('lx', -0.3224, 0),
             'c': ('lx', 0.225, 0.5)}

    @property
    def pins(self):

        newpins = {}
        for pinname, data in self.ppins.items():
            loc, x, y = data
            if self.mirror:
                y = -y
            if self.invert:
                x = -x
            newpins[pinname] = loc, x, y
        return newpins
