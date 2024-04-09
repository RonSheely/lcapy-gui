class Action:

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


class ActionAdd(Action):

    code = 'A'
    inverse_code = 'D'


class ActionDelete(Action):

    code = 'D'
    inverse_code = 'A'


class ActionMove(Action):
    # Detach, move, attach

    code = 'M'
    inverse_code = 'M'


class ActionJoin(Action):

    code = 'J'
    inverse_code = 'S'


class ActionSplit(Action):

    code = 'S'
    inverse_code = 'J'
