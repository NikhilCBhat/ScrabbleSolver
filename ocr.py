from PIL import Image
import pytesseract
import cv2
import numpy as np
import time
from collections import Counter
import threading
from wordFunctions import makeBlankBoard

BOARD_LENGTH = 15

## Image --> Image
## Resizes an image
def resize(img, scale=0.2):
    return cv2.resize(img, (0,0), None, scale, scale)

## Image --> List-of Letters
## Gets the letters the player has
def getPlayerLetters(screenshot, display=False):
    height, width, _ = screenshot.shape
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    screenshot = cv2.threshold(screenshot[int(3*height/4):height, 0:width], 50, 255, cv2.THRESH_BINARY_INV)[1]
    screenshot = cv2.bitwise_not(screenshot)
    screenshot = cv2.GaussianBlur(screenshot,(3,3),0)
    screenshot = cv2.resize(screenshot, (0,0), None, 2.5, 2.5)

    while display:
        cv2.imshow('t', resize(screenshot))
        if(cv2.waitKey(1) & 0xFF == ord('q')):
            break

    return list(pytesseract.image_to_string(screenshot))

squareSize = 75
hOffset = 740
def getSquare(img, x, y, display=False):
    oGsquare = img[hOffset+x*squareSize:hOffset+(x+1)*squareSize, squareSize*y:squareSize*(y+1)]
    square = cv2.cvtColor(oGsquare, cv2.COLOR_BGR2GRAY)
    square = cv2.threshold(square, 190, 255, cv2.THRESH_BINARY_INV)[1]
    # square = cv2.GaussianBlur(square,(1,1),0)
    square = np.tile(square, 15)
    letters = pytesseract.image_to_string(square)
    data = Counter(letters)

    while display:
        cv2.imshow('hi', square)
        cv2.waitKey(1)

    return str(data.most_common(1)[0][0]) if len(letters) else "-"

def getBoardLetters(filePath, display=False):
    img = cv2.imread(filePath)
    board = makeBlankBoard(BOARD_LENGTH)
    opposite = cv2.bitwise_not(img)
    if display:
        print("~~~Gameboard~~~ \n")
    for i in range(BOARD_LENGTH):
        line = ""
        for j in range(BOARD_LENGTH):
            board[i][j] = getSquare(opposite, i, j)
            if display:
                line += getSquare(opposite, i, j)
        if display:
            print(line)
    if display:
        yourletters = getPlayerLetters(img)
        print("\nYour letters are %s."%''.join(yourletters))
    return board

if __name__ == '__main__':
    fp = '/home/nikhil/Documents/Projects/ScrabbleSolver/pics/scrabbleGame.jpg'
    fp2 = '/home/nikhil/Documents/Projects/ScrabbleSolver/pics/lateGame.PNG'
    img = cv2.imread(fp)
    getBoardLetters(fp, True)



    # print(getPlayerLetters(img))
    # getSquare(img, 0,9)
    # getBoardLetters('/home/nikhil/Documents/Projects/ScrabbleSolver/pics/lateGame.PNG')
    # returnLetters(fp)
    # print(getBoardLetters(fp))