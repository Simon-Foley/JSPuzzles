import numpy as np

dim = 4
board = np.zeros((dim, dim), dtype=float)

if __name__ == '__main__':
    board[0, 0] = 1.0


    def new_board(board, shots_so_far):
        horizontal_board = np.zeros((dim, dim), dtype=float)
        vertical_board = np.zeros((dim, dim), dtype=float)
        results_board = np.zeros((dim, dim), dtype=float)

        shot = shots_so_far + 1
        results_board = np.fliplr(np.tril(np.fliplr(board), k=-1))
        results_board[dim - 1, 0] = board[dim - 1, 0]

        for i in range(0, dim - 1):
            for j in range(0, dim - i):
                horizontal_board[i, (j + 1) % (dim - i)] = board[i, j] / shot

        for i in range(0, dim - 1):
            for j in range(0, dim - i, 1):
                vertical_board[i + 1, j] = board[i, j] * (shot - 1) / shot

        return horizontal_board + vertical_board + results_board


    def iterate(iterations=1):
        start_board = np.zeros((dim, dim), dtype=float)
        # You can set this to [0,n] for different  bots
        start_board[0, 0] = 1.0

        for i in range(0, iterations):
            start_board = new_board(start_board, i)

        return start_board

    answer = iterate(iterations=25)

    with np.printoptions(precision=19, suppress=True, formatter={'float': '{:0.14f}'.format}, linewidth=100):
        print(answer[-1][0])
