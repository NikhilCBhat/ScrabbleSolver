from PIL import Image
import pytesseract
import cv2
import numpy as np
import time
from collections import Counter
import threading

## Image --> Image
## Resizes an image
def resize(img):
    return cv2.resize(img, (0,0), None, 0.2, 0.2)

## Image --> List-of Letters
## Gets the letters the player has
def getPlayerLetters(screenshot, display=False):
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

squareSize = 75
hOffset = 740
def getSquare(img, x, y):
    oGsquare = img[hOffset+x*squareSize:hOffset+(x+1)*squareSize, squareSize*y:squareSize*(y+1)]
    square = cv2.cvtColor(oGsquare, cv2.COLOR_BGR2GRAY)
    square = cv2.threshold(square, 210, 255, cv2.THRESH_BINARY_INV)[1]
    square = cv2.GaussianBlur(square,(1,1),0)
    square = np.tile(square, 20)
    letters = pytesseract.image_to_string(square)
    data = Counter(letters)
    return str(data.most_common(1)[0][0]) if len(letters) else "-"

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
    yourletters = getPlayerLetters(img)
    print("\nYour letters are %s."%''.join(yourletters))
    print(time.time() - start)

returnLetters('lateGame.PNG')