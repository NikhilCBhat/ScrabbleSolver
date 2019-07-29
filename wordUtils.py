with open("scrabble.txt") as file: 
   fileWords = file.readlines() 
   fileWords = set([x[0:-1] for x in fileWords])

## Check if a group of letters is a word
## String -> Boolean
def isWord(letters):
    return letters.lower() in fileWords

## Removes a value from a list, if the value exists
## Any, List-of Any -> List-of Any
def safeRemove(val, l):
    try:
        l.remove(val)
    except:
        pass