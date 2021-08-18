import numpy as np


class Grid:
    template = None

    def __init__(self, n, m, list_of_indexes):
        self.array = np.array([['-'] * m] * n) if Grid.template is None else np.array(Grid.template)  # empty grid or grid of past piece
        self.fill(list_of_indexes, m)

    def __str__(self):
        return "\n".join(" ".join(elem for elem in row) for row in self.array)

    def fill(self, list_of_indexes, m):
        for index in list_of_indexes:
            self.array[index // m][index % m] = "0"

    @staticmethod
    def check_empty(array, list_of_indexes, m):
        return all(array[index // m][index % m] != "0" for index in list_of_indexes)

    def check_endgame(self, m):
        return any(all(self.array[i][j] == "0" for i in range(len(self.array))) for j in range(m))

    def remove_full_lines(self, n, m):
        new_array = [row for row in self.array[::-1] if any(cell != "0" for cell in row)]
        self.array = np.array([['-'] * m] * (n - len(new_array)) + new_array[::-1])


class Tetris:
    pieces_storage = {"I": np.array([[4, 14, 24, 34], [3, 4, 5, 6]] * 2),
                      "S": np.array([[5, 4, 14, 13], [4, 14, 15, 25]] * 2),
                      "Z": np.array([[4, 5, 15, 16], [5, 15, 14, 24]] * 2),
                      "L": np.array([[4, 14, 24, 25], [5, 15, 14, 13], [4, 5, 15, 25], [6, 5, 4, 14]]),
                      "J": np.array([[5, 15, 25, 24], [15, 5, 4, 3], [5, 4, 14, 24], [4, 14, 15, 16]]),
                      "O": np.array([[4, 14, 15, 5]] * 4),
                      "T": np.array([[4, 14, 24, 15], [4, 13, 14, 15], [5, 15, 25, 14], [4, 5, 6, 15]])}

    def __init__(self, n, m):
        self.n = n  # number of rows
        self.m = m  # number of columns
        if m != 10:  # adjust the indexes for the board
            self.adjust_board()
        self.grid = Grid(n, m, [])  # the grid of the game
        self.current_piece = None  # the piece we're playing with right now
        self.current_index = None  # the position of the piece in the rotation positions (from 0 to 3)
        self.positions = None  # the array containing the rotation positions of the piece adjusted to the current dimension of the board
        self.bottom = False  # to indicate if this piece is at the bottom of the grid or not

    def __str__(self):
        return str(self.grid)

    def adjust_board(self):
        for piece in Tetris.pieces_storage:  # for each piece == matrix, in the dictionary
            for i, pos in enumerate(Tetris.pieces_storage[piece]):  # for each position == array
                for j, index in enumerate(pos):  # for each index == int_element
                    Tetris.pieces_storage[piece][i][j] = (index % 10) - (10 - self.m) // 2 + index // 10 * self.m

    def load_piece(self, piece):
        Grid.template = self.grid.array
        self.current_piece = piece
        self.current_index = 0
        self.positions = np.array(Tetris.pieces_storage[piece])
        self.bottom = False
        assert Grid.check_empty(Grid.template, self.positions[self.current_index], self.m) or self.grid.check_endgame(self.m)
        self.grid = Grid(self.n, self.m, self.positions[0])

    def go_down(self):
        if all(index + self.m < self.m * self.n for index in self.positions[self.current_index]):
            self.positions = [[index + self.m for index in pos] for pos in self.positions]  # go down theoretically
            if Grid.check_empty(Grid.template, self.positions[self.current_index], self.m):
                self.grid = Grid(self.n, self.m, self.positions[self.current_index])  # go down in the grid if only it's possible
            else:
                self.bottom = True
                assert not self.grid.check_endgame(self.m)
        if any(index + self.m >= self.m * self.n for index in self.positions[self.current_index]):  # check for next down
            self.bottom = True
            assert not self.grid.check_endgame(self.m)

    def rotate_piece(self):
        if not self.bottom:
            self.current_index += 1 if self.current_index != 3 else - self.current_index
        self.go_down()

    def move_piece_left(self):
        if not self.bottom and all(index % self.m != 0 for index in self.positions[self.current_index]):
            for i, pos in enumerate(self.positions):
                for j, index in enumerate(pos):
                    self.positions[i][j] = index - 1
        self.go_down()

    def move_piece_right(self):
        if not self.bottom and all((index + 1) % self.m != 0 for index in self.positions[self.current_index]):
            for i, pos in enumerate(self.positions):
                for j, index in enumerate(pos):
                    self.positions[i][j] = index + 1
        self.go_down()

    def remove_full_lines(self):
        self.grid.remove_full_lines(self.n, self.m)
        Grid.template = self.grid.array


# Write your code here
dim = input().split()
game = Tetris(int(dim[1]), int(dim[0]))
print(str(game), end="\n\n")
try:
    while True:
        in_put = input()
        if in_put == "piece":
            game.load_piece(input().strip().upper())
            print(str(game), end="\n\n")
        if in_put == "rotate":
            game.rotate_piece()
            print(str(game), end="\n\n")
        elif in_put == "right":
            game.move_piece_right()
            print(str(game), end="\n\n")
        elif in_put == "left":
            game.move_piece_left()
            print(str(game), end="\n\n")
        elif in_put == "down":
            game.go_down()
            print(str(game), end="\n\n")
        elif in_put == "break":
            game.remove_full_lines()
            print(str(game), end="\n\n")
        elif in_put == "exit":
            break
except AssertionError:
    print(str(game), "Game Over!", sep="\n\n")
