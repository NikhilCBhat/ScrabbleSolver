from PIL import Image
import pytesseract
import cv2
import numpy as np
import time
from collections import Counter
import threading
from wordFunctions import makeBlankBoard

## Image --> Image
## Resizes an image
def resize(img):
    return cv2.resize(img, (0,0), None, 0.2, 0.2)

## Image --> List-of Letters
## Gets the letters the player has
def getPlayerLetters(screenshot, display=False):
    height, width, _ = screenshot.shape
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    screenshot = screenshot[int(3*height/4):height, 0:width]
    screenshot = cv2.threshold(screenshot, 50, 255, cv2.THRESH_BINARY_INV)[1]
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
def getSquare(img, x, y):
    oGsquare = img[hOffset+x*squareSize:hOffset+(x+1)*squareSize, squareSize*y:squareSize*(y+1)]
    square = cv2.cvtColor(oGsquare, cv2.COLOR_BGR2GRAY)
    square = cv2.threshold(square, 210, 255, cv2.THRESH_BINARY_INV)[1]
    square = cv2.GaussianBlur(square,(1,1),0)
    square = np.tile(square, 25)
    letters = pytesseract.image_to_string(square)
    data = Counter(letters)

    while True:
        cv2.imshow('hi', square)
        cv2.waitKey(1)

    return str(data.most_common(1)[0][0]) if len(letters) else "-"

def returnLetters(filePath):
    start = time.time()
    img = cv2.imread(filePath)
    # print(img)
    opposite = cv2.bitwise_not(img)
    print("~~~Gameboard~~~ \n")
    for i in range(15):
        line = ""
        for j in range(15):
            line += getSquare(opposite, i, j)
        print(line)
    print(time.time() - start)
    yourletters = getPlayerLetters(img)
    print("\nYour letters are %s."%''.join(yourletters))
    print(time.time() - start)

def getBoardLetters(filePath):
    img = cv2.imread(filePath)
    board = makeBlankBoard(15)
    opposite = cv2.bitwise_not(img)
    for i in range(15):
        for j in range(15):
            board[i][j] = getSquare(opposite, i, j)
    return board

if __name__ == '__main__':
    # img = cv2.imread('lateGame.PNG')
    # print(getPlayerLetters(img))
    img = cv2.imread('scrabbleGame.jpg')

    getSquare(img, 0,9)

    # returnLetters('lateGame.PNG')