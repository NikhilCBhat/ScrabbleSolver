import time
from wordUtils import safeRemove, isWord, getPermutations, makeBlankBoard, isEndPoint, isAnchor, isValidPlacement
from wordClasses import move

## Gets all posibble moves on the board
def getAllMoves(board, hand):
    anchors = getAnchors(board)
    allowed = getValidLetters(board, hand)
    lefts = getLefts(board, anchors, allowed, hand)
    
    moves = makeBlankBoard(len(board))
    for i in range(len(board)):
        moves[i] = getRowMoves(board[i], lefts[i], allowed[i], anchors[i], hand)
    return moves

## Gets all of the anchors on the board
## List-of [List-of Strings] -> List-of Strings
def getAnchors(board):
    anchors = makeBlankBoard(len(board))
    for row_num in range(len(board)):
        for column_num in range(len(board[row_num])):
            if board[row_num][column_num] == '-':
                if isAnchor(board, row_num, column_num):
                    anchors[row_num][column_num] = "&"
    return anchors

## Gets all of the valid letter placements on a board, with a given hand
## List-of [List-of Strings], List-of Strings -> List-of [List-of Strings]
def getValidLetters(board, hand):
    allAllowed = makeBlankBoard(len(board))

    for row_num in range(len(board)):
        for column_num in range(len(board[row_num])):
            if board[row_num][column_num] == '-':
                allAllowed[row_num][column_num] = ""
                for letter in hand:
                    if isValidPlacement(letter, board, row_num, column_num):
                        allAllowed[row_num][column_num] += letter
    return allAllowed

## Returns all possible left parts for every anchor on the board
def getLefts(board, anchors, allowed, hand):
    lefts = ['']*len(board)
    for i in range(len(board)):
        lefts[i] = getLeftRow(board[i], anchors[i], allowed[i], hand)
    return lefts

## Get the possible moves for a row
def getRowMoves(row, rowLefts, rowAllowed, rowAnchors, hand):
    # Output Container
    moves = []
    for _ in range(len(row)):
        moves.append([])
    
    # Iterate over the row, looking for moves
    for i in range(len(row)):
        if rowAnchors[i] == '&':
            for leftPart in rowLefts[i]:
                moves[i].extend(extendRight(leftPart, i, rowAllowed.copy(), row, firstRun=True))

    return moves

## Generates moves by adding letters to the right of a tile
def extendRight(leftPart, currentIndex, rowAllowed, row, firstRun=False):
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
    if (not firstRun) and isEndPoint(currentIndex, row, rowAllowed) and isWord(left):
        allWords.append(left)
    
    # Stop when you've reached the end of the row
    if currentIndex >= len(row):
        return allWords if allWords is not [] else None
    
    # If there's a letter, add it and keep going
    elif row[currentIndex] != '-':
        leftPart.word = left+row[currentIndex]
        allWords.extend(extendRight(leftPart, currentIndex+1, rowAllowed, row))
    
    # If there are allowed letters, add each one
    elif len(trimmedAllowed[currentIndex]):
        for letter in trimmedAllowed[currentIndex]:
            leftPart.word = left+letter
            leftPart.fromHand = fromHand+letter if fromHand is not None else letter
            allWords.extend(extendRight(leftPart, currentIndex+1, rowAllowed, row))

    return allWords if allWords is not [] else None

## Gets all the left parts for every anchor in a row
def getLeftRow(row, rowAnchors, rowAllowed, hand):
    lefts = []
    for _ in row:
        lefts.append([])

    for i in range(1, len(row)):
        if rowAnchors[i] == '&':
            if (row[i-1] != '-') and (rowAnchors[i-1] != '&'):
                prev = row[i-1]
                for j in range(i-2, -1, -1):
                    if row[j] == '-':
                        break
                    prev = row[j] + prev

                lefts[i] = [move(prev)]
            else:
                leftsFromHand = getLeftFromHand(row, i, rowAnchors, rowAllowed, hand)
                lefts[i] = [move(x,x) for x in leftsFromHand]
                lefts[i].append(move(""))
    return lefts

## Gets all the left parts using the letters in your hand
def getLeftFromHand(row, anchorPoint, anchors, allowed, hand):
    allowedLetters = []
    combos = getPermutations(hand)
    wordLen = 1
    for i in range(anchorPoint-1, -1, -1):
        if (row[i] != '-') or (anchors[i] == '&'):
            break
        else:
            if wordLen in combos:
                if combos[wordLen] is not None:
                    combosToJoin = [''.join(x) for x in combos[wordLen]]
                    allowedLetters.extend(combosToJoin)
        wordLen += 1
    return allowedLetters
