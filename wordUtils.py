import os
parent = os.path.dirname(os.getcwd())

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

with open(parent + "/scrabble.txt") as file: 
   fileWords = file.readlines() 
   fileWords = set([x[:-1] for x in fileWords])

## Check if a group of letters is a word
## String --> Boolean
def isWord(letters):
    return letters.lower() in fileWords

## Removes a value from a list, if the value exists
## Any, [List-of Any] --> [List-of Any]
def safeRemove(val, l):
    try:
        l.remove(val)
    except:
        pass

## Gets the string fromed by a list of tiles
## [List-of Tiles] --> String
def getLetters(tiles):
    if tiles is None:
        return None
    letters = ""
    for tile in tiles:
        letters += tile.letter
    return letters

## Transposes a board
## [List-of Lists] --> [List-of Lists]
def transpose(board):
    return list(map(list, zip(*board)))

## Allows a player to edit the letters on the board
## [List-of Lists] --> [List-of Lists]
def editBoardLetters(board):
    needsEdit = "y"
    while needsEdit == "y":
        print("This is the current board:")
        for index,row in enumerate(board):
            print(index, row)
        print([str(x) for x in range(index+1)])
        needsEdit = input("\nIs there anything incorrect on the board? (y/n) ")
        if needsEdit == "y":
            edit = input("Enter the row, column, and the correct letter: (row,column,letter) ")
            r, c, l = edit.split(",")
            board[int(r)][int(c)] = l.upper()
    return board