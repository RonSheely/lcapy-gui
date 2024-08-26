class Pins(dict):

    def add(self, pin):

        self[pin.name] = pin

    def __iter__(self):
        # Iterate over the values and not the keys
        return iter(self.values())
