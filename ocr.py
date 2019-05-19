from PIL import Image
import pytesseract
import cv2
import numpy as np
import time

## Image --> Image
## Resizes an image
def resize(img):
    return cv2.resize(img, (0,0), None, 0.2, 0.2)

## Image --> List-of Letters
## Gets the letters the player has
def getCurrentLetters(screenshot, display=False):
    height, width, _ = screenshot.shape
    # print(height, width)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    screenshot = screenshot[int(3*height/4):height, 0:width]

    screenshot = cv2.threshold(screenshot, 50, 255, cv2.THRESH_BINARY_INV)[1]
    screenshot = cv2.bitwise_not(screenshot)
    screenshot = cv2.GaussianBlur(screenshot,(3,3),0)
    screenshot = cv2.resize(screenshot, (0,0), None, 2.5, 2.5)
    # print(list(pytesseract.image_to_string(screenshot)))
    while display:
        cv2.imshow('t', resize(screenshot))
        if(cv2.waitKey(1) & 0xFF == ord('q')):
            break
    return list(pytesseract.image_to_string(screenshot))


## Image --> List-of Letters
## Gets the letters on the board
def getBoardLetters(filePath):
    screenshot = cv2.imread(filePath)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    screenshot = cv2.bitwise_not(screenshot)
    _, width = screenshot.shape
    screenshot = screenshot[700:1900, 0:width]

    screenshot = cv2.threshold(screenshot, 50, 255, cv2.THRESH_BINARY_INV)[1]
    screenshot = cv2.bitwise_not(screenshot)
    screenshot = cv2.GaussianBlur(screenshot,(3,3),0)

    # print(list(pytesseract.image_to_string(screenshot)), "Print")
    while True:
        cv2.imshow('t', resize(screenshot))
        if(cv2.waitKey(1) & 0xFF == ord('q')):
            break
        
    # return list(pytesseract.image_to_string(screenshot))

def printTxt(img):
    print(list(pytesseract.image_to_string(img)))
    print('-'*60)

from collections import Counter

squareSize = 75
hOffset = 740
def getSquare(img, x, y):
    # img = cv2.bitwise_not(img)
    oGsquare = img[hOffset+x*squareSize:hOffset+(x+1)*squareSize, squareSize*y:squareSize*(y+1)]
    square = cv2.cvtColor(oGsquare, cv2.COLOR_BGR2GRAY)
    square = cv2.threshold(square, 210, 255, cv2.THRESH_BINARY_INV)[1]
    # square = cv2.bitwise_not(square)
    square = cv2.GaussianBlur(square,(1,1),0)
    # cv2.imwrite('D.jpg', square)
    square = np.tile(square, 20) #, axis=1)
    # print(square.shape, type(square))
    letters = (list(pytesseract.image_to_string(square)))
    # print(letters)

    data = Counter(letters)
    return str(data.most_common(1)[0][0]) if len(letters) else "-"

    # height, width, _ = img.shape
    # board = img[hOffset:hOffset+1125, 0:1125]
    # cv2.imshow('o', oGsquare)
    # cv2.imshow('board', resize(board))
    # cv2.imshow('square', square)
    # cv2.waitKey(0)

def returnLetters(filePath):
    start = time.time()
    img = cv2.imread(filePath)
    opposite = cv2.bitwise_not(img)
    print("~~~Gameboard~~~ \n")
    for i in range(15):
        line = ""
        for j in range(15):
            line += getSquare(opposite, i, j)
        print(line)
    print(time.time() - start)
    yourletters = getCurrentLetters(img)
    print("\nYour letters are %s."%''.join(yourletters))
    print(time.time() - start)


returnLetters('lateGame.PNG')