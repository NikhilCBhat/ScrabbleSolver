import itertools
from wordUtils import wordMultiplier, letterMultiplier, pointsList

class Move(object):
    def __init__(self, word=[], board=None, scoreMove=False):
        self.word = word
        self.board = board
        self.score = self.getScore() if scoreMove else 0

    def getScore(self, score=0):

        scorableLetters = [x for x in self.word if not(x.onBoard)]
        # print(scorableLetters)

        finalMultiplier = 1

        for tile in scorableLetters:
            for direction in [-1,1]:
                for dTile in self.board.getVertical(tile, direction):
                    score += dTile.points
            if tile.posn is not None:
                self.board.board[tile.posn.x][tile.posn.y] = tile
                finalMultiplier *= wordMultiplier.get(self.board.modifiers[tile.posn.x][tile.posn.y], 1)
                score += tile.points * (letterMultiplier.get(self.board.modifiers[tile.posn.x][tile.posn.y], 1)-1)

        score += tile.points*finalMultiplier
        for lTile in self.board.getLeft(tile):
            score += lTile.points*finalMultiplier
        for lTile in self.board.getRight(tile):
            score += lTile.points*finalMultiplier
        return score

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