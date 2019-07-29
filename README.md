# Scrabble Solver
_Currently a work in progress._

### About
A scrabble solver, which reads the current game board and produces the highest scoring move.

### Try it Yourself!

#### Without an image:
1. Open the `/examples/` folder.
2. Edit the gameboard, and hand if you'd like. 
3. Run the `withoutOCR_example` script using your IDE of choice, or from terminal with `python3 withoutOCR_example.py`. 

Here's how it should look:
![Without OCR](https://raw.githubusercontent.com/NikhilCBhat/ScrabbleSolver/master/examples/Without_OCR_Example.png)

### How it Works

#### Reading the Board
1) OpenCV is used to apply several filters to the input image in to make it as clean as possible.
2) Then each tile from the game board is split, and duplicated in a row 10x.
3) Pytesseract is then used to read the letters, and the most common letter in the 10 is selected.
4) The output from the OCR is stored as a Board object. x`
