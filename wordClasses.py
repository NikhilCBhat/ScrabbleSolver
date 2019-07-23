pointsList = {'-': -1,
 'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4, 'I': 1, 'J': 8, 'K': 5, 'L': 1, 'M': 3, 'N': 1, 'O': 1, 'P': 3,
 'Q': 10, 'R': 1, 'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 4, 'X': 8, 'Y': 4, 'Z': 10}

MODIFIERS =    [['~', '~', '~', 'TW', '~', '~', 'TL', '~', 'TL', '~', '~', 'TW', '~', '~', '~'],
                ['~', '~', 'DL', '~', '~', 'DW', '~', '~', '~', 'DW', '~', '~', 'DL', '~', '~'],
                ['~', 'DL', '~', '~', 'DL', '~', '~', '~', '~', '~', 'DL', '~', '~', 'DL', '~'],
                ['TW', '~', '~', 'TL', '~', '~', '~', 'DW', '~', '~', '~', 'TL', '~', '~', 'TW'],
                ['~', '~', 'DL', '~', '~', '~', 'DL', '~', 'DL', '~', '~', '~', 'DL', '~', '~'],
                ['~', 'DW', '~', '~', '~', 'TL', '~', '~', '~', 'TL', '~', '~', '~', 'DW', '~'],
                ['TL', '~', '~', '~', 'DL', '~', '~', '~', '~', '~', 'DL', '~', '~', '~', 'TL'],
                ['~', '~', '~', 'DW', '~', '~', '~', 'DW', '~', '~', '~', 'DW', '~', '~', '~'],
                ['TL', '~', '~', '~', 'DL', '~', '~', '~', '~', '~', 'DL', '~', '~', '~', 'TL'],
                ['~', 'DW', '~', '~', '~', 'TL', '~', '~', '~', 'TL', '~', '~', '~', 'DW', '~'],
                ['~', '~', 'DL', '~', '~', '~', 'DL', '~', 'DL', '~', '~', '~', 'DL', '~', '~'],
                ['TW', '~', '~', 'TL', '~', '~', '~', 'DW', '~', '~', '~', 'TL', '~', '~', 'TW'],
                ['~', 'DL', '~', '~', 'DL', '~', '~', '~', '~', '~', 'DL', '~', '~', 'DL', '~'],
                ['~', '~', 'DL', '~', '~', 'DW', '~', '~', '~', 'DW', '~', '~', 'DL', '~', '~'],
                ['~', '~', '~', 'TW', '~', '~', 'TL', '~', 'TL', '~', '~', 'TW', '~', '~', '~']]

class Move(object):
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

class Board(object):
    def __init__(self, board=None, size=None):
        self.modifiers = MODIFIERS.copy()
        self.board = board
        self.size = size
        if self.board is None:
            self.board = []
            for i in range(self.size):
                row = []
                for j in range(self.size):
                    p = Posn(i,j)
                    row.append(Tile(posn=p))
                self.board.append(row)

    def printBoard(self):
        for row in self.board:
            print(row)
    
    def updateAnchors(self):
        for row_num, row in enumerate(self.board):
            for column_num, _ in enumerate(row):
                if self.board[row_num][column_num].isEmpty():
                    self.board[row_num][column_num].isAnchor == self.isAnchor(row_num, column_num)
    
    def isAnchor(self, row, column):
        anchor = False

        if row != 0:
            anchor = anchor or (self.board[row-1][column] != '-')   
        if row != self.size - 1:
            anchor = anchor or (self.board[row+1][column] != '-')
        if column != 0:
            anchor = anchor or (self.board[row][column-1] != '-')
        if column != self.size - 1:
            anchor = anchor or (self.board[row][column+1] != '-')
        return anchor


def makeBoard(letters):
    b = []
    for i,row in enumerate(letters):
        boardRow = []
        for j,char in enumerate(row):
            p = Posn(i, j)
            boardRow.append(Tile(p, char))
        b.append(boardRow)
    return Board(b)          

class Tile(object):
    def __init__(self, posn=None, letter="-", isAnchor=False):
        self.letter = letter
        self.points = pointsList[self.letter]
        self.posn = posn
        self.isAnchor = isAnchor
    
    def isEmpty(self):
        return self.letter == "-"

    def __repr__(self):
        return self.letter

class Posn(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return "%d,%d"%(self.x,self.y)