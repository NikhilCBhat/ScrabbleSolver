import os
import sys
parent = os.path.dirname(os.getcwd())
sys.path.append(parent)

import argparse
parser = argparse.ArgumentParser(description='--gametype for scrabble/wwf')
parser.add_argument('--gametype', help="Choose the gametype")
args = parser.parse_args()

from board import Board, getBestMove
from wordClasses import Hand

board =         [['-', '-', '-', '-', '-', '-', '-', '-', 'J', 'O', '-', 'T', '-', '-', '-'], 
                ['-', '-', '-', '-', '-', '-', '-', '-', '-', 'D', 'R', 'O', 'N', 'E', '-'],
                ['-', '-', '-', '-', '-', '-', '-', '-', 'H', '-', '-', 'Y', '-', 'Y', 'O'],
                ['-', '-', '-', '-', '-', '-', '-', 'M', 'E', '-', '-', 'O', 'P', 'E', 'N'],
                ['-', '-', '-', '-', '-', '-', 'Q', 'I', 'S', '-', '-', '-', 'R', '-', '-'],
                ['-', '-', '-', '-', '-', '-', '-', 'K', '-', '-', '-', '-', 'O', 'H', '-'],
                ['-', '-', '-', '-', '-', '-', '-', 'E', '-', '-', '-', '-', 'B', 'A', 'D'],
                ['-', '-', '-', '-', '-', '-', '-', 'D', 'U', 'V', 'E', 'T', 'S', '-', 'A'], 
                ['-', '-', '-', '-', '-', '-', '-', '-', 'T', 'I', 'L', '-', '-', '-', 'R'], 
                ['-', '-', '-', '-', '-', 'F', '-', '-', '-', 'C', '-', '-', '-', '-', 'T'], 
                ['-', '-', '-', '-', '-', 'A', '-', '-', '-', 'E', '-', '-', '-', '-', '-'], 
                ['-', '-', '-', '-', '-', 'T', 'W', 'I', 'G', 'S', '-', '-', '-', '-', '-'], 
                ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
                ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'], 
                ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-']]

hand = ['N', 'C', 'E', 'S', 'R', 'O', 'Q']

if __name__ == "__main__":

    print("This is the current board: ")
    for row in board:
        print(row)
    print("You current letters are: ", hand)

    bestMove = getBestMove(board, hand, args.gametype)
    print("\nThe best word you can make is %s to earn %s points"%(bestMove, bestMove.score))

    print("Here's how the board should look after your move: ")
    bestMove.displayMove(board)