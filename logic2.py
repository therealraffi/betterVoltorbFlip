from read import get_cols_rows
from typing import List, Dict
from utils2 import *

class HeaderCell:
    def __init__(self, points, voltorbs):
        self.voltorbs = voltorbs
        self.free_cells = 5 - voltorbs
        self.points = points
        self.combos = None

    def calc_combos(self):
        self.combos = find_combos(self.points, self.voltorbs, self.free_cells)

    def update(self, val):
        self.combos = updated_combos(val, self.combos)
        self.points -= val
        self.free_cells -= 1

    def __repr__(self):
        return f"{self.points}/{self.voltorbs}"

    def __str__(self) -> str:
        return self.__repr__()

class GameCell:
    def __init__(self, ri, ci, gb, best=False):
        self.row_idx = ri
        self.col_idx  = ci
        self.gameboard: Gameboard = gb
        self.probs: Dict[float] = None
        self.solved = False
        self.best = best

        self.calc_probs()

    def calc_probs(self):
        combos, pvals = combine_combos(self.gameboard.row_headers[self.row_idx].combos, self.gameboard.col_headers[self.col_idx].combos)
        if len(combos[1]) == 0:
            print("EMPTY! on COL in cell")
            print(self.row_idx, self.col_idx)
        row_combos, col_combos = combos[0], combos[1]
        self.probs = get_probs(pvals, row_combos, col_combos)
    
    def is_useful(self):
        return (self.probs[2] > 0 or self.probs[3] > 0)
        
    def set_value(self, val):
        self.solved = True
        self.best = False
        self.probs = {i:0 for i in range(4)}
        self.probs[val] = 1

        self.gameboard.row_headers[self.row_idx].update(val)
        self.gameboard.col_headers[self.col_idx].update(val)

        self.gameboard.recalc_probs(self.row_idx, self.col_idx)
        return len(self.probs) == 1

    def get_corners(self):
        corners = ['' for i in range(4)]
        for v in self.probs:
            if self.probs[v] != 0:
                corners[v] = str(v)
        return corners
    
    def expected_val(self):
        # return round(sum([i * self.probs[i] for i in self.probs]), 3)
        # return round(((1 - self.probs[0])*sum([i * self.probs[i] for i in self.probs])), 3)

        pvals = [k for k in self.probs if self.probs[k] > 0]
        print(pvals,  (1 - self.probs[0]))
        return sum(pvals) / len(pvals) * (1 - self.probs[0])


    def __repr__(self) -> str:
        return str(self.expected_val())

    def __str__(self) -> str:
        return self.__repr__()
    
class Gameboard:
    def __init__(self):
        self.row_headers: List[HeaderCell] = []
        self.col_headers: List[HeaderCell] = []
        self.board: List[GameCell][GameCell] = [[None for j in range(5)] for i in range(5)]

    def create_board(self, img_path):
        row_vals, col_vals = get_cols_rows(img_path)
        for i in range(0, len(row_vals), 3):
            t, d, v = row_vals[i:i+3]
            row_cell = HeaderCell(t * 10 + d, v)  
            row_cell.calc_combos()         
            self.row_headers.append(row_cell) 
            
            t, d, v = col_vals[i:i+3]
            col_cell = HeaderCell(t * 10 + d, v)  
            print(col_cell.points, col_cell.voltorbs)
            col_cell.calc_combos()         
            self.col_headers.append(col_cell) 

        best_val = 0
        best_coord = (0, 0)
        for ri in range(5):
            for ci in range(5):
                self.board[ri][ci] = GameCell(ri, ci, self)
                if self.board[ri][ci].expected_val() > best_val and not self.board[ri][ci].solved and self.board[ri][ci].is_useful():
                    best_val = self.board[ri][ci].expected_val()
                    best_coord = (ri, ci)
        
        self.board[best_coord[0]][best_coord[1]].best = True
    
    def recalc_probs(self, ri, ci):
        row_header: HeaderCell = self.row_headers[ri]
        col_header: HeaderCell = self.col_headers[ci]

        for i in range(5):
            if not self.board[i][ci].solved:
                # print("INTEREST", self.col_headers[4].combos)

                combos, _ = combine_combos(self.row_headers[i].combos, col_header.combos)
                if len(combos[1]) == 0:
                    print("EMPTY! on ROW")
                    print(self.row_headers[i].combos, col_header.combos)
                    print(i, ci)

                self.row_headers[i].combos = combos[0]
                self.board[i][ci].calc_probs()
            
            if not self.board[ri][i].solved:
                combos, _ = combine_combos(row_header.combos, self.col_headers[i].combos)
                if len(combos[1]) == 0:
                    print("EMPTY! on COL")
                    print(ri, i)

                self.col_headers[i].combos = combos[1]
                self.board[ri][i].calc_probs()  
                

        best_val = 0
        best_coord = (0, 0)
        for i in range(5):
            for j in range(5):
                self.board[i][j].best = False
                if self.board[i][j].expected_val() > best_val and not self.board[i][j].solved and self.board[i][j].is_useful():
                    best_val = self.board[i][j].expected_val()
                    best_coord = (i, j)

        self.board[best_coord[0]][best_coord[1]].best = True

    def print_board(self):
        # Print each row with the numbers aligned in each column
    
        for i, row in enumerate(self.board):
            formatted_row = " ".join(f"{gc.expected_val():.2f}" for ci, gc in enumerate(row)) + " " + self.row_headers[i].__str__()
            print(formatted_row)

        formatted_row = " ".join(str(rc.__str__()) + ((4-len(rc.__str__())) * " ") for ri, rc in enumerate(self.col_headers))
        print(formatted_row)

# board = Gameboard()
# directory_path = '/Users/raffukhondaker/Desktop'  # Replace with your directory path
# board.create_board(get_most_recently_added_file(directory_path))


# board.print_board()
# # print(board.board[2][0].probs)
# # print(board.board[2][1].probs)
# # print(board.board[2][2].probs)
# # print(board.board[2][3].probs)
# # print(board.board[2][4].probs)

# print("ROWS:")
# for i, row in enumerate(board.row_headers):
#     # print(i, row.probs)
#     print(i, row.combos)

# print("COLS:")
# for i, col in enumerate(board.col_headers):
#     # print(i, col.probs)
#     print(i, col.combos)


# print()
# r=0
# c=2
# board.board[r][c].set_value(2)
# board.print_board()

# print()
# r=0
# c=0
# board.board[r][c].set_value(3)
# board.print_board()

# print()
# r=2
# c=4
# board.board[r][c].set_value(1)
# board.print_board()

# print()
# r=1
# c=4
# board.board[r][c].set_value(1)
# board.print_board()

# r=3
# c=1
# print(board.board[r][c].probs)