import itertools

with open("scrabble.txt") as file: 
   file_words = file.readlines() 
   file_words = set([x[0:-1] for x in file_words])

## Get all permutations of the letters in your hand
## List-of Letters --> Dictionary
def getPermutations(hand):
    combosDict = dict.fromkeys(range(1,len(hand)+1))
    for i in range(1,len(hand)+1): 
        combosDict[i] = set(itertools.permutations(hand, i))
    return combosDict

## Check if a group of letters is a word
## String -> Boolean
def isWord(letters):
    return letters.lower() in file_words

## Outputs a list of list of letters nicely
def printBoard(board):
    for row in board:
        print('          '.join(row))

## Makes a list of n lists where each sublist is of length n 
## Int -> List-of [List-of Strings]
def makeBlankBoard(length):
    board = []
    for _ in range(length):
        row = ['-']*length
        board.append(row)
    return board

## Removes a value from a list, if the value exists
## Any, List-of Any -> List-of Any
def safeRemove(val, l):
    try:
        l.remove(val)
    except:
        pass

## Determines whether a given index is the end of a row
def isEndPoint(index, row, allowed):
    return (index >= len(row)) or row[index] == '-' or not(len(allowed[index]))

## Determines whether a given position is an anchor
## List-of [List-of Strings], Int, Int -> Boolean
def isAnchor(board, row, column):

    anchor = False
    
    if row != 0:
        anchor = anchor or (board[row-1][column] != '-')   
    if row != len(board) - 1:
        anchor = anchor or (board[row+1][column] != '-')
    if column != 0:
        anchor = anchor or (board[row][column-1] != '-')
    if column != len(board) - 1:
        anchor = anchor or (board[row][column+1] != '-')

    return anchor

## Determines if a letter is allowed to be placed in a location on the board
## String, List-of [List-of Strings], Int, Int -> Boolean
def isValidPlacement(letter, board, row_num, column_num):
    above = getAbove(board, row_num, column_num)
    below = getBelow(board, row_num, column_num)
    return (above == "" and below == "") or isWord((below+letter+above).lower())

## Gets the letters below a position
def getBelow(board, row_num, column_num):
    below = ""
    for row in range(row_num-1, -1, -1):
        if board[row][column_num] == '-':
            break
        below = board[row][column_num] + below
    return below

## Gets the letter above a position
def getAbove(board, row_num, column_num):
    above = ""
    for row in range(row_num+1, len(board)):
        if board[row][column_num] == '-':
            break
        above += board[row][column_num]
    return above