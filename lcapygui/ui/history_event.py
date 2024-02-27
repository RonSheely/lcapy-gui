class HistoryEvent:

    def __init__(self, cpt, from_nodes=None, to_nodes=None, to_cpt=None):

        if to_cpt is None:
            to_cpt = cpt

        self.cpt = cpt
        self.to_cpt = to_cpt
        self.from_nodes = from_nodes
        self.to_nodes = to_nodes

    def __str__(self):

        return '%s (%s %s) -> (%s %s)' % (self.code, self.cpt,
                                          self.from_nodes, self.to_cpt,
                                          self.to_nodes)


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


class HistoryEventDetachMove(HistoryEvent):

    code = 'U'
    inverse_code = 'C'


class HistoryEventMoveAttach(HistoryEvent):

    code = 'C'
    inverse_code = 'U'


class HistoryEventJoin(HistoryEvent):

    code = 'J'
    inverse_code = 'S'


class HistoryEventSplit(HistoryEvent):

    code = 'S'
    inverse_code = 'J'
