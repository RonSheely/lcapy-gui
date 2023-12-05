class Picture:

    def __init__(self):

        self.elts = []

    def add(self, patch):

        if patch is None:
            raise ValueError('Adding invalid patch')

        self.elts.append(patch)

    def remove(self):

        def erase(elt):
            if isinstance(elt, list):
                for elt in elt:
                    erase(elt)
            else:
                elt.remove()

        erase(self.elts)
        self.elts = []
