from copy import deepcopy
from wordUtils import isWord, safeRemove, getLetters, MODIFIERS, transpose
from wordClasses import Tile, Posn, Hand, Move

class Board(object):
    def __init__(self, letters, hand=None):
        self.modifiers = MODIFIERS

        self.board = []
        for i,row in enumerate(letters):
            boardRow = []
            for j,char in enumerate(row):
                boardRow.append(Tile(Posn(i, j), char, onBoard=True))
            self.board.append(boardRow)

        self.allowed = []
        self.lefts = []
        self.moves = []
        self.size = len(letters)
        self.updateAnchors()

        for _ in range(self.size):
            self.allowed.append([['-']]*self.size)
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
                    self.allowed[row_num][column_num] = []
                    for tile in hand.tiles:
                        nt = Tile(letter=tile.letter, posn=Posn(row_num, column_num))
                        if self.isValidPlacement(nt):
                            self.allowed[row_num][column_num].append(nt)

    ## Calls the getLeftRow function to update self.lefts
    def updateLefts(self):
        for i in range(self.size):
            self.lefts[i] = self.getLeftRow(i)

    ## Gets all the left parts for every anchor in a row
    def getLeftRow(self, rowIndex):
        lefts = []
        row = self.board[rowIndex]

        for _ in range(self.size):
            lefts.append([])

        for columnIndex in range(1, self.size):
            if row[columnIndex].isAnchor:
                if not(row[columnIndex-1].isEmpty()) and not(row[columnIndex-1].isAnchor):
                    prev = [row[columnIndex-1]]
                    for j in range(columnIndex-2, -1, -1):
                        if row[j].isEmpty():
                            break
                        prev.insert(0, row[j])

                    lefts[columnIndex] = [Move(prev)]
                else:
                    leftsFromHand = self.getLeftFromHand(row, columnIndex)
                    lefts[columnIndex] = [Move(t) for t in leftsFromHand]
                    lefts[columnIndex].append(Move())
        return lefts

    ## Gets all the left parts using the letters in your hand
    def getLeftFromHand(self, row, anchorPoint):
        allowedLetters = []
        combos = self.hand.getPermutations()
        wordLen = 1
        for i in range(anchorPoint-1, -1, -1):
            if not(row[i].isEmpty()) or row[i].isAnchor:
                break
            lefts = combos.get(wordLen, None)
            if lefts is not None:
                allowedLetters.extend(lefts)
            wordLen += 1
        return allowedLetters

    ## Determines whether a location on the board is an anchor
    def isAnchor(self, rowIndex, columnIndex):
        anchor = False

        if rowIndex != 0:
            anchor = anchor or not(self.board[rowIndex-1][columnIndex].isEmpty()) 
        if rowIndex != self.size - 1:
            anchor = anchor or not(self.board[rowIndex+1][columnIndex].isEmpty())
        if columnIndex != 0:
            anchor = anchor or not(self.board[rowIndex][columnIndex-1].isEmpty())
        if columnIndex != self.size - 1:
            anchor = anchor or not(self.board[rowIndex][columnIndex+1].isEmpty())
        return anchor
   
    def printAnchors(self, save=False):
        b = []
        for i in range(self.size):
            row = ""
            for j in range(self.size):
                if self.board[i][j].isAnchor:
                    row += "&"
                else:
                    row += "-"
            print(row)
            if save:
                b.append(row)
        if save:
            return b

    ## Gets adjacent tiles in the vertical direction 
    # Direction 1 --> Down, -1 Up 
    def getVertical(self, tile, direction):
        if tile.posn is None:
            return []
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

    ## Gets adjacent tiles to the left of the current one
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
        return (above == "" and below == "") or isWord((above+tile.letter+below).lower())

    ## Updates the board moves with the possible moves
    def updateMoves(self):
        for rowNumber in range(self.size):
            self.moves[rowNumber] = self.getRowMoves(rowNumber)

            for listOfMoves in self.moves[rowNumber]:
                for move in listOfMoves:
                    for position, tile in enumerate(move):
                        if tile.posn is not None:
                            rn, cn = tile.posn.x, tile.posn.y
                            for index, tile in enumerate(move):
                                tile.posn = Posn(rn, index + cn - position)
                            break

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
                    moves[colIndex].extend(self.extendRight(leftPart, rowIndex, colIndex, firstRun=True))

        return moves

    ## Generates moves by adding letters to the right of a tile
    def extendRight(self, leftPart, rowIndex, currentIndex, firstRun=False):
        rowAllowed = [[elem for elem in sublist] for sublist in self.allowed[rowIndex]]
        row = self.board[rowIndex]
        allWords = []
        left = getLetters(leftPart.word)

        # Removes letters that have already been used from the allowed letters
        for tile in leftPart:
            if not(tile.onBoard):
                for sublist in rowAllowed:
                    safeRemove(tile, sublist)

        # If you're at an endpoint, check your previous, unless this 
        if (not firstRun) and self.isEndPoint(currentIndex, rowIndex) and isWord(left):
            allWords.append(leftPart)

        # Stop when you've reached the end of the row
        if currentIndex >= self.size:
            return allWords if allWords is not [] else None

        # If there's a letter, add it and keep going
        elif not(row[currentIndex].isEmpty()):
            leftPart.word.append(row[currentIndex])
            allWords.extend(self.extendRight(leftPart, rowIndex, currentIndex+1))

        # If there are allowed letters, add each one
        elif len(rowAllowed[currentIndex]):
            for tile in rowAllowed[currentIndex]:
                lp = deepcopy(leftPart)
                lp.word.append(tile)
                allWords.extend(self.extendRight(lp, rowIndex, currentIndex+1))

        return allWords if allWords is not [] else None

    ## Determines whether a given index is the end of a row
    def isEndPoint(self, index, rowInd):
        return (index >= self.size) or self.board[rowInd][index].isEmpty() or not(len(self.allowed[rowInd][index]))

def getBestMoveBoard(b):
    bestMove = None

    for row in b.moves:
        for listOfMoves in row:
            for move in listOfMoves:
                move.getScore(b)
                if bestMove is None or move > bestMove:
                    bestMove = move
    return bestMove

def getBestMove(letters, hand):

    h = Hand(hand)
    b1 = Board(letters, h)
    bm = getBestMoveBoard(b1)
    b2 = Board(transpose(letters), h)
    bm2 = getBestMoveBoard(b2)

    for tile in bm2:
        tile.posn.x, tile.posn.y = tile.posn.y, tile.posn.x

    return max(bm, bm2)