class HistoryEvent:

    def __init__(self, code, cpt, nodes=None):

        self.code = code
        self.cpt = cpt
        self.nodes = nodes

    def __str__(self):

        return '%s %s %s' % (self.code, self.cpt, self.nodes)
