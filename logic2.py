from read import get_cols_rows
from typing import List, Dict
from utils import *

class HeaderCell:
    def __init__(self, points, voltorbs):
        self.voltorbs = voltorbs
        self.free_cells = 5 - voltorbs
        self.points = points
        self.pvals = {i:0 for i in range(5)}
        self.combos = None

    def calc_pvals(self):
        self.pvals, self.combos = find_pvals(self.points, self.voltorbs, self.free_cells)

    def __repr__(self):
        return f"{self.points}/{self.voltorbs}"

    def __str__(self) -> str:
        return self.__repr__()

class GameCell:
    def __init__(self, ri, ci, gb, pvals=None, best=False):
        self.row_idx = ri
        self.col_idx  = ci
        self.gameboard: Gameboard = gb
        self.pvals: Dict[float] = pvals
        self.solved = False
        self.best = best

        self._calc_pvals()

    def _calc_pvals(self):
        vals = [0,1,2,3]
        self.pvals = {i:0 for i in vals}
        s = 0

        for v in vals:
            self.pvals[v] = self.gameboard.row_headers[self.row_idx].pvals[v] * self.gameboard.col_headers[self.col_idx].pvals[v]
            s += self.pvals[v]
            # self.pvals[v] = (self.gameboard.row_headers[self.row_idx].pvals[v] + self.gameboard.row_headers[self.col_idx].pvals[v]) / 2
            # self.pvals[v] = (self.gameboard.row_headers[self.row_idx].pvals[v])

        if s == 0:
            return

        for v in vals:
            self.pvals[v] = round(self.pvals[v] / s, 3)
    
    def is_useful(self):
        return (self.pvals[2] > 0 or self.pvals[3] > 0)
        
    def set_value(self, val):
        self.solved = True
        self.best = False
        self.pvals = {i:0 for i in range(5)}
        self.pvals[val] = 1

        self.gameboard.row_headers[self.row_idx].points -= val
        self.gameboard.row_headers[self.row_idx].free_cells -= 1

        self.gameboard.col_headers[self.col_idx].points -= val
        self.gameboard.col_headers[self.col_idx].free_cells -= 1

        self.gameboard.recalc_pvals(self.row_idx, self.col_idx)

        return len(self.pvals) == 1

    def get_corners(self):
        corners = ['' for i in range(4)]
        for v in self.pvals:
            if self.pvals[v] != 0:
                corners[v] = str(v)
        return corners
    
    def expected_val(self):
        # return round(sum([i * self.pvals[i] for i in self.pvals]), 3)
        return 1 - round(self.pvals[0], 3)


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
            row_cell.calc_pvals()         
            self.row_headers.append(row_cell) 
            
            t, d, v = col_vals[i:i+3]
            col_cell = HeaderCell(t * 10 + d, v)  
            col_cell.calc_pvals()         
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
    
    def recalc_pvals(self, ri, ci):
        self.col_headers[ci].calc_pvals()
        self.row_headers[ri].calc_pvals()

        for i in range(5):
            if not self.board[i][ci].solved:
                self.board[i][ci]._calc_pvals()
            
            if not self.board[ri][i].solved:
                self.board[ri][i]._calc_pvals()
        
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

board = Gameboard()
board.create_board("imgs/Screen Shot 2023-12-17 at 12.59.32 PM.png")

board.print_board()
# print(board.board[2][0].pvals)
# print(board.board[2][1].pvals)
# print(board.board[2][2].pvals)
# print(board.board[2][3].pvals)
# print(board.board[2][4].pvals)

print("ROWS:")
for i, row in enumerate(board.row_headers):
    # print(i, row.pvals)
    print(i, row.combos)

print("COLS:")
for i, col in enumerate(board.col_headers):
    # print(i, col.pvals)
    print(i, col.combos)


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
# print(board.board[r][c].pvals)