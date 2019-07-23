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
    def __init__(self, letters=None, board=None):
        self.letters = letters
        self.board = board
        self.score = self.getScore()
   
    def getScore(self, score=0):
         
        for tile in self.letters:
            for bTile in self.board.getVertical(tile, 1):
                score += bTile.points
            
            for aTile in self.board.getVertical(tile, -1):
                score += aTile.points

            self.board.board[tile.posn.x][tile.posn.y] = tile
        
        score += tile.points
        for lTile in self.board.getLeft(tile):
            print(lTile.letter, lTile.points)
            score += lTile.points
 
        return score

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
        else:
            self.size = len(board)
        self.updateAnchors()

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
            anchor = anchor or not(self.board[row-1][column].isEmpty()) 
        if row != self.size - 1:
            anchor = anchor or not(self.board[row+1][column].isEmpty())
        if column != 0:
            anchor = anchor or not(self.board[row][column-1].isEmpty())
        if column != self.size - 1:
            anchor = anchor or not(self.board[row][column+1].isEmpty())
        return anchor
   
    def getVertical(self, tile, direction):
        adjacent = []
        row_num, column_num = tile.posn.x, tile.posn.y

        r = range(row_num-1, -1, -1)
        if direction == 1:
            r = range(row_num+1, self.size)
        
        for row in r:
            tile = self.board[row][column_num]
            if tile.isEmpty():
                break
            adjacent.append(tile)
        
        return adjacent[::direction]

    def getLeft(self, tile):
        left = []
        row_num, column_num = tile.posn.x, tile.posn.y
        for col in range(column_num-1, -1, -1):
            tile = self.board[row_num][col]
            if tile.isEmpty():
                break
            left.append(tile)
        return left[::-1]

    def getRight(self, tile):
        right = []
        row_num, column_num = tile.posn.x, tile.posn.y
        for col in range(column_num+1, self.size):
            tile = self.board[row_num][col]
            if tile.isEmpty():
                break
            right.append(tile)
        return right

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