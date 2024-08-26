class Pins(dict):

    def add(self, pin):

        self[pin.name] = pin

    def __iter__(self):
        # Iterate over the values and not the keys
        return iter(self.values())

    def by_position(self, position):

        x, y = position

        for pin in self:
            if abs(pin.x - x) < 1e-5 and abs(pin.y - y) < 1e-5:
                return pin
        return None
