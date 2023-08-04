from .bipole import BipoleComponent


class OpenCircuit(BipoleComponent):

    type = 'O'
    args = ()
    has_value = False

    def draw(self, model, **kwargs):
        pass
