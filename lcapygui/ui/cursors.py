class Cursors(list):

    def debug(self):

        s = ''
        for cursor in self:
            s += '%s, %s' % (cursor.x, cursor.y) + '\n'
        return s

    def remove(self):

        while self != []:
            self.pop().remove()

    def draw(self):

        if len(self) > 0:
            self[0].draw(polarity='positive')
        if len(self) > 1:
            self[1].draw(polarity='negative')
