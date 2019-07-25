import itertools
from wordUtils import isWord, safeRemove

pointsList = {'-': -1, 'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4, 'I': 1, 'J': 8,
 'K': 5, 'L': 1, 'M': 3, 'N': 1, 'O': 1, 'P': 3, 'Q': 10, 'R': 1, 'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 4, 'X': 8, 'Y': 4, 'Z': 10}

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

letterMultiplier = {"DL": 2, "TL":3}
wordMultiplier = {"TW":3, "DW":2}

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
        return "MO: %s/%s"%(w, fh)

    def __eq__(self, value):
        return self.word == value.word and self.fromHand == value.fromHand

    def printMistakes(self):
        if self.fromHand is not None:
            for letter in set(self.fromHand):
                if letter not in set(self.word):
                    print(letter)

class Move(object):
    def __init__(self, letters=None, board=None):
        self.letters = letters
        self.board = board
        self.score = self.getScore()
   
    def getScore(self, score=0):

        finalMultiplier = 1
         
        for tile in self.letters:
            for direction in [-1,1]:
                for dTile in self.board.getVertical(tile, direction):
                    score += dTile.points
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

class Board(object):
    def __init__(self, board=None, size=None, hand=None):
        self.modifiers = MODIFIERS.copy()
        self.board = board
        self.allowed = []
        self.lefts = []
        self.moves = []
        self.size = size

        if self.board is None:
            self.board = []
            for i in range(self.size):
                board_row = []
                for j in range(self.size):
                    p = Posn(i,j)
                    board_row.append(Tile(posn=p))
                self.board.append(board_row)
        else:
            self.size = len(board)
        self.updateAnchors()

        for _ in range(self.size):
            self.allowed.append(['-']*self.size)
            self.lefts.append(['']*self.size)
            self.moves.append(['-']*self.size)

        if hand is not None:
            self.updateAllowed(hand)
            self.updateLefts()
            self.updateMoves()

    ## Prints the letters in the board
    def printBoard(self):
        for row in self.board:
            print(row)
    
    ## Updates "isAnchor" field of each Tile in the Board.board
    def updateAnchors(self):
        for row_num, row in enumerate(self.board):
            for column_num, _ in enumerate(row):
                if self.board[row_num][column_num].isEmpty():
                    self.board[row_num][column_num].isAnchor = self.isAnchor(row_num, column_num)
    
    ## Fills the Board.allowed table with strings, representing allowed letters from the hand
    def updateAllowed(self, hand):
        self.hand = hand
        for row_num, row in enumerate(self.board):
            for column_num, _ in enumerate(row):
                if self.board[row_num][column_num].isEmpty():
                    self.allowed[row_num][column_num] = ""
                    for tile in hand.tiles:
                        tile.posn = Posn(row_num, column_num)
                        if self.isValidPlacement(tile):
                            self.allowed[row_num][column_num] += tile.letter

    def updateLefts(self):
        for i in range(self.size):
            self.lefts[i] = self.getLeftRow(i)

    ## Gets all the left parts for every anchor in a row
    def getLeftRow(self, rowIndex):
        lefts = []
        row = self.board[rowIndex]

        for _ in range(self.size):
            lefts.append([])

        for i in range(1, self.size):
            if row[i].isAnchor:
                if not(row[i-1].isEmpty()) and not(row[i-1].isAnchor):
                    prev = row[i-1].letter
                    for j in range(i-2, -1, -1):
                        if row[j].isEmpty():
                            break
                        prev = row[j].letter + prev

                    lefts[i] = [move(prev)]
                else:
                    leftsFromHand = self.getLeftFromHand(row, i)
                    lefts[i] = [move(x,x) for x in leftsFromHand]
                    lefts[i].append(move(""))
        return lefts

    ## Gets all the left parts using the letters in your hand
    def getLeftFromHand(self, row, anchorPoint):
        allowedLetters = []
        combos = self.hand.getPermutations()
        wordLen = 1
        for i in range(anchorPoint-1, -1, -1):
            if not(row[i].isEmpty()) or row[i].isAnchor:
                break
            elif (wordLen in combos) and combos[wordLen] is not None:
                # combosToJoin = [''.join(x) for x in combos[wordLen]]
                allowedLetters.extend([''.join(x) for x in combos[wordLen]])
            wordLen += 1
        return allowedLetters

    ## Determines whether a location on the board is an anchor
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
   
    ## Gets adjacent tiles in the vertical direction 
    # Direction 1 --> Down, -1 Up 
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

    ## Gets adjacent tiles to the lef.`t of the current one
    def getLeft(self, tile):
        left = []
        row_num, column_num = tile.posn.x, tile.posn.y
        for col in range(column_num-1, -1, -1):
            tile = self.board[row_num][col]
            if tile.isEmpty():
                break
            left.append(tile)
        return left[::-1]

    ## Gets adjacent tiles to the right of the current one
    def getRight(self, tile):
        right = []
        row_num, column_num = tile.posn.x, tile.posn.y
        for col in range(column_num+1, self.size):
            tile = self.board[row_num][col]
            if tile.isEmpty():
                break
            right.append(tile)
        return right

    ## Determines if a tile forms a word in the vertical direction
    def isValidPlacement(self, tile):
        above = getLetters(self.getVertical(tile, -1))
        below = getLetters(self.getVertical(tile, 1))
        return (above == "" and below == "") or isWord((below+tile.letter+above).lower())

    ## Updates the board moves with the possible moves
    def updateMoves(self):
        for i in range(self.size):
            self.moves[i] = self.getRowMoves(i)

    ## Get the possible moves for a row
    def getRowMoves(self, rowIndex):
        # Output Container
        moves = []
        for _ in range(self.size):
            moves.append([])
        
        # Iterate over the row, looking for moves
        for colIndex in range(self.size):
            if self.board[rowIndex][colIndex].isAnchor:
                for leftPart in self.lefts[rowIndex][colIndex]:
                    moves[colIndex].extend(self.extendRight(leftPart, rowIndex, colIndex, self.allowed[rowIndex].copy(), firstRun=True))

        return moves

    ## Generates moves by adding letters to the right of a tile
    def extendRight(self, leftPart, rowIndex, currentIndex, rowAllowed, firstRun=False):
        row = self.board[rowIndex]
        allWords = []
        trimmedAllowed = [list(x) for x in rowAllowed]

        left = leftPart.word
        fromHand = leftPart.fromHand

        # Removes letters that have already been used from the allowed letters
        if fromHand is not None:
            for sublist in trimmedAllowed:
                for letter in list(fromHand):
                    safeRemove(letter, sublist)
        
        # If you're at an endpoint, check your previous, unless this 
        if (not firstRun) and self.isEndPoint(currentIndex, rowIndex, rowAllowed) and isWord(left):
            allWords.append(left)
        
        # Stop when you've reached the end of the row
        if currentIndex >= self.size:
            return allWords if allWords is not [] else None
        
        # If there's a letter, add it and keep going
        elif not(row[currentIndex].isEmpty()):
            leftPart.word = left+row[currentIndex].letter
            allWords.extend(self.extendRight(leftPart, rowIndex, currentIndex+1, rowAllowed))
        
        # If there are allowed letters, add each one
        elif len(trimmedAllowed[currentIndex]):
            for letter in trimmedAllowed[currentIndex]:
                leftPart.word = left+letter
                leftPart.fromHand = fromHand+letter if fromHand is not None else letter
                allWords.extend(self.extendRight(leftPart, rowIndex, currentIndex+1, rowAllowed))

        return allWords if allWords is not [] else None
    
    ## Determines whether a given index is the end of a row
    def isEndPoint(self, index, rowInd, allowed):
        return (index >= self.size) or self.board[rowInd][index].isEmpty() or not(len(allowed[index]))
    
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

class Hand(object):
    def __init__(self, tiles=None, letters=None):
        if letters is not None:
            self.letters = letters
            self.tiles = []
            for l in letters:
                self.tiles.append(Tile(letter=l))
            self.size = len(letters)
        else:
            self.tiles = tiles
            self.size = len(tiles)
    
    def getPermutations(self):
        combosDict = dict.fromkeys(range(1,self.size+1))
        for i in range(1,self.size+1): 
            combosDict[i] = set(itertools.permutations(self.letters, i))
        return combosDict

class Posn(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return "%d,%d"%(self.x,self.y)

def getLetters(tiles):
    letters = ""
    for tile in tiles:
        letters += tile.letter
    return letters