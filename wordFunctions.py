import time
from wordUtils import safeRemove, isWord, getPermutations, makeBlankBoard, isEndPoint, isAnchor, isValidPlacement

## Gets all posibble moves on the board
def getAllMoves(board, hand):
    start = time.time()
    anchors = getAnchors(board)
    print("Anchors",time.time()-start)
    allowed = getValidLetters(board, hand)
    print("Allowed", time.time()-start)
    lefts = getLefts(board, anchors, allowed, hand)
    # print(lefts)
    for l in lefts:
        print(l)
    
    
    print("Lefts", time.time()-start)
    moves = makeBlankBoard(len(board))
    print("Blank board", time.time()-start)
    for i in range(len(board)):
        moves[i] = getRowMoves(board[i], lefts[i], allowed[i], anchors[i], hand)
        print("Row", i, time.time()-start)
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
            moves[i].extend(extendRight(["", False], i, rowAllowed.copy(), row))
            for leftPart in rowLefts[i]:
                moves[i].extend(extendRight(leftPart, i, rowAllowed.copy(), row, firstRun=True))

    return moves

def extendRight(leftPart, currentIndex, rowAllowed, row, firstRun=False):
    allWords = []
    trimmedAllowed = [list(x) for x in rowAllowed]
    # print(leftPart)

    if not(isinstance(leftPart, list)) or len(leftPart) < 2:
        return allWords

    left = leftPart[0]

    if leftPart[1]:
        for sublist in trimmedAllowed:
            for letter in list(left):
                safeRemove(letter, sublist)
        # print(trimmedAllowed)
    
    # If you're at an endpoint, check your previous, unless this 
    if (not firstRun) and isEndPoint(currentIndex, row, rowAllowed) and isWord(left):
        allWords.append(left)
    
    # Stop when you've reached the end of the row
    if currentIndex >= len(row):
        return allWords if allWords is not [] else None
    
    # If there's a letter, add it and keep going
    elif row[currentIndex] != '-':
        leftPart[0] = left+row[currentIndex]
        allWords.extend(extendRight(leftPart, currentIndex+1, rowAllowed, row))
    
    # If there are allowed letters, add each one
    elif len(trimmedAllowed[currentIndex]):
        for letter in trimmedAllowed[currentIndex]:
            leftPart[0] = left+letter
            leftPart[1] = True
            allWords.extend(extendRight(leftPart, currentIndex+1, rowAllowed, row))

    return allWords if allWords is not [] else None

## Gets all the left parts for every anchor in a row
def getLeftRow(row, rowAnchors, rowAllowed, hand):
    lefts = [['-', False]]*len(row)
    for i in range(1, len(row)):
        if rowAnchors[i] == '&':
            if (row[i-1] != '-') and (rowAnchors[i-1] != '&'):
                prev = row[i-1]
                for j in range(i-2, -1, -1):
                    if row[j] == '-':
                        break
                    prev = row[j] + prev

                lefts[i] = [[prev,False]]
            else:
                leftsFromHand = getLeftFromHand(row, i, rowAnchors, rowAllowed, hand)
                leftsFromHand = [[x, True] for x in leftsFromHand]
                lefts[i] = leftsFromHand
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
    return allowedLetters if allowedLetters != [] else ['-']
