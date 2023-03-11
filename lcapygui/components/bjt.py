from .transistor import Transistor


class BJT(Transistor):

    type = "Q"
    can_stretch = True
    angle_offset = 90
    default_kind = 'npn-'

    kinds = {'npn-': 'NPN',
             'pnp-': 'PNP',
             'npn-nigbt': 'nigbt',
             'pnp-pigbt': 'pigbt',
             'npn-Lnigbt': 'Lnigbt',
             'pnp-Lpigbt': 'Lpigbt'}

    # TODO: add base offset for Lnigbt, Lpigbt
    # TODO: add bodydiode
