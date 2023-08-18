from .labelentries import LabelEntry, LabelEntries
from .window import Window


class ExprAttributesDialog(Window):

    def __init__(self, expr, ui, title='Expression attributes'):

        super(ExprAttributesDialog, self).__init__(ui, None, title)

        self.expr = expr

        entries = [LabelEntry('units', 'Units', expr.units),
                   LabelEntry('domain', 'Domain', expr.domain),
                   LabelEntry('quantity', 'Quantity', expr.quantity),
                   LabelEntry('causal', 'Causal', expr.is_causal, command=self.causal)]

        self.labelentries = LabelEntries(self, ui, entries)

    def causal(self):

        self.expr.is_causal = self.labelentries.get('causal')
