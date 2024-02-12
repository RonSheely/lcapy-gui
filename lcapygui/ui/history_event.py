class HistoryEvent:

    def __init__(self, code, cpt=None, from_nodes=None, to_nodes=None):

        self.code = code
        self.cpt = cpt
        self.from_nodes = from_nodes
        self.to_nodes = to_nodes

    def __str__(self):

        return '%s %s %s -> %s' % (self.code, self.cpt, self.from_nodes, self.to_nodes)
