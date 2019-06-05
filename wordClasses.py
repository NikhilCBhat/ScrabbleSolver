class move(object):
    def __init__(self, word=None, fromHand=None):
        self.word = word
        self.fromHand = fromHand

    def __str__(self):
        w = "None" if self.word is None else self.word
        fh = "None" if self.fromHand is None else self.fromHand
        return "%s / %s"%(w, fh)

    def __repr__(self):
        w = "None" if self.word is None else self.word
        fh = "None" if self.fromHand is None else self.fromHand
        return "MoveObject: %s/%s"%(w, fh)

    def printMistakes(self):
        if self.fromHand is not None:
            for letter in set(self.fromHand):
                if letter not in set(self.word):
                    print(letter)
