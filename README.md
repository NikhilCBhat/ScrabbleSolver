# Scrabble Solver
_Currently a work in progress._

### About
A scrabble solver, which reads the current game board and produces the highest scoring move.

### Try it Yourself!

#### Without an image:
1. Open the `/examples/` folder.
2. Edit the gameboard, and hand if you'd like. 
3. Run the `withoutOCR_example` script using your IDE of choice, or from terminal with `python3 withoutOCR_example.py --gametype <choose either scrabble or wwf>`. 

Here's how it should look:
![Without OCR](https://raw.githubusercontent.com/NikhilCBhat/ScrabbleSolver/master/examples/exampleOutput.png)

### How it Works

#### Reading the Board
1) OpenCV is used to apply several filters to the input image in to make it as clean as possible.
2) Then each tile from the game board is split, and duplicated in a row 10x.
3) Pytesseract is then used to read the letters, and the most common letter in the 10 is selected.
4) The output from the OCR is stored as a Board object.

#### Calculating the Best Move
Generating all of the move is a 4 step process. Initial inspiration, along with the idea of reducing the move generation to a 1-Dimensional problem is taken from a publication by Appel & Jacobson, which is cited below.

1. A new word in scrabble can only be placed connecting to an existing word. As a result, the program initially goes through the board recording all of these locations in the Tile object, by updating the property `isAnchor`.
2. The program next goes through the board, and checks each empty location on the board, to see if any of the tiles can be placed there. All allowable tiles are placed into the "allowed" list of that location. 
3. With the allowed letters, the program then steps through each anchor tile, and compiles a list of each possible left part of a word, prior to the anchor point. Each left part can be made from either existing tiles on the board, or tiles from the hand. 
4. Finally possible moves are generated by going through each left part, and then extended to the right, using the allowed letters and any letters it runs into. If any moves do not form valid words, they are rejected.

As this process is solely 1-D (it only searchs for moves made horizontally) this process is repeated for the transposed board. Each move generated is then scored, and the highest scoring move is returned.

Appel, Andrew W., and Guy J. Jacobson. “The World's Fastest Scrabble Program.” Communications of the ACM, vol. 31, no. 5, 1988, pp. 572–578., doi:10.1145/42411.42420.

