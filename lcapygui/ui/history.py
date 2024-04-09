class History(list):

    def __str__(self):

        return '\n'.join([str(e) for e in self])


    def add(self, *args):

        self.append(', '.join([str(arg) for arg in args]))
