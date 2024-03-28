class HistoryEvent:

    def __init__(self, cpt, from_nodes=None, to_nodes=None):

        self.cpt = cpt
        self.from_nodes = from_nodes
        self.to_nodes = to_nodes

    def __str__(self):

        if self.from_nodes is None or self.to_nodes is None:
            return '%s %s' % (self.code, self.cpt)

        return '%s %s %s -> %s' % (self.code, self.cpt,
                                   list(self.from_nodes),
                                   list(self.to_nodes))


class HistoryEventAdd(HistoryEvent):

    code = 'A'
    inverse_code = 'D'


class HistoryEventDelete(HistoryEvent):

    code = 'D'
    inverse_code = 'A'


class HistoryEventMove(HistoryEvent):
    # Detach, move, attach

    code = 'M'
    inverse_code = 'M'


class HistoryEventJoin(HistoryEvent):

    code = 'J'
    inverse_code = 'S'


class HistoryEventSplit(HistoryEvent):

    code = 'S'
    inverse_code = 'J'
