from .transistor import Transistor


class BJT(Transistor):

    type = "Q"
    angle_offset = 90
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
             'pnp-Lpigbt':  'L-shaped PNP IGBT'}

    # TODO: add base offset for Lnigbt, Lpigbt
