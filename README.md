# Scrabble Solver
_Currently a work in progress._

### About:
A scrabble solver, which reads the current game board and produces the highest scoring move.

### How it Works:

#### Reading the Board
1) OpenCV is used to apply several filters to the input image in to make it as clean as possible.
2) Then each tile from the game board is split, and duplicated in a row 10x.
3) Pytesseract is then used to read the letters, and the most common letter in the 10 is selected.
4) The output from the OCR is stored as a Board object. 
