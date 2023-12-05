class History(list):

    def __str__(self):

        return '\n'.join([str(e) for e in self])
