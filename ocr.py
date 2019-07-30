from PIL import Image
import pytesseract
import cv2
import numpy as np
import time
from collections import Counter
import threading

## Makes a list of n lists where each sublist is of length n 
## Int -> List-of [List-of Strings]
def makeBlankBoard(length):
    board = []
    for _ in range(length):
        row = ['-']*length
        board.append(row)
    return board

## Image --> Image
## Resizes an image
def resize(img, scale=0.2):
    return cv2.resize(img, (0,0), None, scale, scale)

## Image --> List-of Letters
## Gets the letters the player has
def getPlayerLetters(filePath, display=False):
    screenshot = cv2.imread(filePath)
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

## Image, X/Y Coordinates --> String
## Gets the letter in a tile
def getSquare(img, x, y, display=False, squareSize = 75, hOffset = 740):
    oGsquare = img[hOffset+x*squareSize:hOffset+(x+1)*squareSize, squareSize*y:squareSize*(y+1)]
    square = cv2.cvtColor(oGsquare, cv2.COLOR_BGR2GRAY)
    square = cv2.threshold(square, 190, 255, cv2.THRESH_BINARY_INV)[1]
    square = np.tile(square, 15)
    letters = pytesseract.image_to_string(square)
    data = Counter(letters)

    while display:
        cv2.imshow('hi', square)
        cv2.waitKey(1)

    return str(data.most_common(1)[0][0]) if len(letters) else "-"

## String -> [List-of [List-of Strings]]
## Converts an image to a list of letters
def getBoardLetters(filePath, boardLength=15):
    img = cv2.imread(filePath)
    board = makeBlankBoard(boardLength)
    opposite = cv2.bitwise_not(img)

    for i in range(boardLength):
        for j in range(boardLength):
            board[i][j] = getSquare(opposite, i, j).upper()

    return board