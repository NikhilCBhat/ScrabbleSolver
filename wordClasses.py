import itertools
from wordUtils import wordMultiplier, letterMultiplier, pointsList

class Move(object):
    def __init__(self, word=[]):
        self.word = word
        self.score = 0

    def getScore(self, board):

        scorableLetters = [x for x in self.word if not(x.onBoard)]
        finalMultiplier = 1

        for tile in scorableLetters:
            for direction in [-1,1]:
                for dTile in board.getVertical(tile, direction):
                    self.score += dTile.points
            if tile.posn is not None:
                board.board[tile.posn.x][tile.posn.y] = tile
                finalMultiplier *= wordMultiplier.get(board.modifiers[tile.posn.x][tile.posn.y], 1)
                self.score += tile.points * (letterMultiplier.get(board.modifiers[tile.posn.x][tile.posn.y], 1)-1)

        self.score += tile.points*finalMultiplier
        for lTile in board.getLeft(tile):
            self.score += lTile.points*finalMultiplier
        for lTile in board.getRight(tile):
            self.score += lTile.points*finalMultiplier

    def __gt__(self, move2):
        return self.score > move2.score

    def __lt__(self, move2):
        return self.score < move2.score

    def __repr__(self):
        return ''.join([tile.letter for tile in self.word])

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