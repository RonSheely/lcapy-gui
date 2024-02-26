class HistoryEvent:

    def __init__(self, code, cpt, from_nodes=None, to_nodes=None,
                 join_nodes=None):

        self.code = code
        self.cpt = cpt
        self.from_nodes = from_nodes
        self.to_nodes = to_nodes
        self.join_nodes = join_nodes

    def __str__(self):

        return '%s %s %s -> %s' % (self.code, self.cpt, self.from_nodes, self.to_nodes)


class HistoryEventAdd(HistoryEvent):

    code = 'A'
    inverse_code = 'D'


class HistoryEventDelete(HistoryEvent):

    code = 'D'
    inverse_code = 'A'


class HistoryEventMove(HistoryEvent):

    code = 'M'
    inverse_code = 'M'


class HistoryEventJoin(HistoryEvent):

    code = 'J'
    inverse_code = 'S'


class HistoryEventSplit(HistoryEvent):

    code = 'S'
    inverse_code = 'J'
