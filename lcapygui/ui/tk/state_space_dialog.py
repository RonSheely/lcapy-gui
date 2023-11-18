from .menu import MenuDropdown, MenuItem
from .labelentries import LabelEntry, LabelEntries
from .window import Window


class StateSpaceDialog(Window):

    def __init__(self, ui, ss):

        super().__init__(ui, None, 'State space')

        self.ss = ss
        self.kindmap = {'State equations': 'state_equations',
                        'Output equations': 'output_equations',
                        'State matrix, A': 'A',
                        'Input matrix, B': 'B',
                        'Output matrix, C': 'C',
                        'Feed through matrix, D': 'D',
                        'Transfer function vector, G': 'G',
                        'System transfer functions matrix, H': 'H',
                        'Eigenvalue matrix, Lambda': 'Lambda',
                        'Modal matrix, M': 'M',
                        'Characteristic polynomial': 'P',
                        'State transition matrix (Laplace), Phi': 'Phi',
                        'Input vector (Laplace), U': 'U',
                        'State vector (Laplace), X': 'X',
                        'Output vector (Laplace), Y': 'Y',
                        'Input vector, u': 'u',
                        'State vector, x': 'x',
                        'State initial value vector, x0': 'x0',
                        'Output vector, y': 'y',
                        'System impulse responses matrix, h': 'h',
                        'Controllability matrix': 'controllability_matrix',
                        'Observability matrix': 'observability_matrix'}

        items = []
        for v in self.kindmap:
            items.append(MenuItem(v, self.on_view))

        mdd = MenuDropdown('View', 0, items)

        menudropdowns = [
            mdd,
            MenuDropdown('Manipulate', 0,
                         [MenuItem('Discretize', self.on_discretize)
                          ])]

        self.add_menu(menudropdowns)

        self.minsize(200, 20)

    def on_view(self, arg):

        attr = getattr(self.ss, self.kindmap[arg])
        try:
            expr = attr()
        except (AttributeError, TypeError):
            expr = attr

        self.ui.show_expr_dialog(expr)

    def on_discretize(self, arg):

        from lcapy.dtstatespace import DTStateSpace

        if isinstance(arg, DTStateSpace):
            return

        ssd = self.ss.discretize()
        self.ui.show_state_space_dialog(ssd)
