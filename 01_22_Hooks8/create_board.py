import numpy as np
import matplotlib.pyplot as plt


def make_board(string):
    # An nxn board of hooks can be uniquely described by
    # an n-1 digit base 4 number (including leading zeros).
    # Each digit corresponds to which corner of
    # the remaining empty space
    # the next hook puts itself, starting from top left = 0
    # and going clockwise

    top_row, top_col = 0, 0
    bot_row, bot_col = len(string), len(string)
    size = len(string) + 1
    board = np.zeros((size, size), dtype=int)
    hook = len(string)  + 1
    for char in string:
        if char == "0":
            board[top_row:bot_row+1,top_col] = hook
            board[top_row,top_col:bot_col+1] = hook
            hook -= 1
            top_row += 1
            top_col += 1


        elif char == "1":
            board[top_row:bot_row+1,bot_col] = hook
            board[top_row,top_col:bot_col+1] = hook

            hook -= 1
            top_row += 1
            bot_col -= 1

        elif char == "2":
            board[top_row:bot_row+1,bot_col] = hook
            board[bot_row,top_col:bot_col+1] = hook

            hook -= 1
            bot_row -= 1
            bot_col -= 1

        elif char == "3":
            board[top_row:bot_row+1,top_col] = hook
            board[bot_row,top_col:bot_col+1] = hook

            hook -= 1
            bot_row -= 1
            top_col += 1
    board[top_row][top_col] = hook
    return board


#def make_board(string_arr):
#  return [make_board(x) for x in string_arr]


def valid_inputs(board_length):
    length = board_length - 1
    # For board of length n, you want all combinations of
    # length n-1 digits 0-3 including leading zeros.

    nums = np.arange(0, 4 ** length)
    base_converter = lambda x: str(np.base_repr(x, base=4)).zfill(length)
    vfunc = np.vectorize(base_converter)
    nums = vfunc(nums)
    return nums
