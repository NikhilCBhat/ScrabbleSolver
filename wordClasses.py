import itertools
from wordUtils import wordMultiplier, letterMultiplier, pointsList

class Move(object):
    def __init__(self, word=[]):
        self.word = word
        self.score = 0
        self.index = 0

    def getScore(self, board):

        finalMultiplier = 1
        wordPoints = 0

        for tile in self.word:

            tileMultiplier = 1

            if not(tile.onBoard):
                tileMultiplier = letterMultiplier.get(board.modifiers[tile.posn.x][tile.posn.y], 1)
                finalMultiplier *= wordMultiplier.get(board.modifiers[tile.posn.x][tile.posn.y], 1)
                for direction in [-1,1]:
                    for dTile in board.getVertical(tile, direction):
                        self.score += dTile.points
            
            wordPoints += tile.points * tileMultiplier

        self.score += wordPoints * finalMultiplier
        return self.score

    def displayMove(self, board):
        for tile in self.word:
            board.board[tile.posn.x][tile.posn.y] = tile

        board.printBoard()

    def __gt__(self, move2):
        return self.score > move2.score

    def __lt__(self, move2):
        return self.score < move2.score

    def __repr__(self):
        return ''.join([tile.letter for tile in self.word])

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index >= len(self.word):
            raise StopIteration
        else:
            self.index += 1
            return self.word[self.index-1]

class Tile(object):
    def __init__(self, posn=None, letter="-", isAnchor=False, onBoard=False):
        self.letter = letter
        self.points = pointsList[self.letter]
        self.posn = posn
        self.isAnchor = isAnchor
        self.onBoard = onBoard

    def isEmpty(self):
        return self.letter == "-"

    def __repr__(self):
        return self.letter

class Hand(object):
    def __init__(self, letters, tiles=[]):
        self.tiles = tiles
        for l in letters:
            self.tiles.append(Tile(letter=l))
        self.size = len(letters)
    
    def getPermutations(self):
        combosDict = dict.fromkeys(range(1,self.size+1))
        for i in range(1,self.size+1):
            combosDict[i] = [list(x) for x in itertools.permutations(self.tiles, i)]
        return combosDict

class Posn(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return "%d,%d"%(self.x,self.y)