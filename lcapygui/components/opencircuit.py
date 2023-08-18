from .bipole import Bipole


class OpenCircuit(Bipole):

    type = 'O'
    args = ()
    has_value = False

    def draw(self, model, **kwargs):
        pass
