import tkinter as tk
from logic import *
import time

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*map(int, rgb))

default_rgb = [150, 150, 150]
done_rgb = [100, 50, 255]
best_rgb = [150, 230, 150]

class CellDisplay:
    def __init__(self, master, displayboard, gameboard, x, y, entry_width=15, cell_size=80, font=('Arial', 18), small_font=('Arial', 12), editable=True, rgb_color=default_rgb):
        # Create a frame for the cell with a thicker border
        self.game_cell: GameCell = gameboard.board[x][y]

        if self.game_cell.best:
            bg_color = rgb_to_hex(best_rgb)

        else:
            self.rgb = rgb_color
            self.rgb[0] = int(100 * self.game_cell.pvals[0]) + 150
            bg_color = rgb_to_hex(self.rgb)

        self.frame = tk.Frame(master, width=cell_size, height=cell_size, borderwidth=2, relief="solid", bg=bg_color)
        self.frame.grid(row=x, column=y, padx=2, pady=2)  # padx and pady for the border effect
        self.frame.grid_propagate(False)  # Prevents the frame from resizing
        self.editable = editable
        self.displayboard = displayboard
        self.x = x
        self.y = y

        # Create the Entry or Label in the center
        if editable:
            self.entry = tk.Entry(self.frame, width= int(entry_width * 0.2), font=font, justify='center', borderwidth=0, bg=bg_color)
            self.entry.delete(0, tk.END)
            self.entry.insert(0, self.game_cell.__str__())
            self.entry.place(relx=0.5, rely=0.5, anchor='center')  # Center the Entry
            self.entry.bind('<Return>', self.on_enter)
        else:
            self.label = tk.Label(self.frame, font=font, justify='center', bg=bg_color, text=' ')
            self.label.place(relx=0.5, rely=0.5, anchor='center')  # Center the Label

        # Add corner numbers
        corner_numbers = self.game_cell.get_corners()
        self.tl_label = tk.Label(self.frame, text=str(corner_numbers[0]), font=small_font, bg=bg_color)
        self.tl_label.place(anchor='nw')

        self.tr_label = tk.Label(self.frame, text=str(corner_numbers[1]), font=small_font, bg=bg_color)
        self.tr_label.place(anchor='ne', relx=1.0)

        self.bl_label = tk.Label(self.frame, text=str(corner_numbers[2]), font=small_font, bg=bg_color)
        self.bl_label.place(anchor='sw', rely=1.0)

        self.br_label = tk.Label(self.frame, text=str(corner_numbers[3]), font=small_font, bg=bg_color)
        self.br_label.place(anchor='se', relx=1.0, rely=1.0)

        self.corners=[self.tl_label, self.tr_label, self.bl_label, self.br_label]
        self.components = [self.frame, self.entry]
        self.components.extend(self.corners)

    def on_enter(self, event):
        done_color = rgb_to_hex(done_rgb)

        self.game_cell.set_value(int(self.entry.get()))
        self.editable = False

        self.entry.configure(state='readonly')
        self.entry.configure(readonlybackground=done_color)
        self.frame.configure(background=done_color)

        for corner in self.corners:
            corner.configure(background=done_color)
            corner.config(text="")

        self.displayboard.update(self.x, self.y)

        # Add additional functionality here for when a cell is edited
    
    def update(self):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, self.game_cell.__str__())

        if self.game_cell.best:
            self.rgb = best_rgb
        else:
            self.rgb[0] = int(100 * self.game_cell.pvals[0]) + 150

        for comp in self.components:
            comp.configure(background=(rgb_to_hex(self.rgb)))

        corners = self.game_cell.get_corners()
        for i in range(len(self.corners)):
            self.corners[i].configure(text=corners[i])

class GameboardDisplay:
    def __init__(self, master, image_path, size=5):
        self.master = master
        self.size = size
        self.gameboard = Gameboard()
        self.gameboard.create_board(image_path)
        self.gameboard.print_board()
        self.cells = [[CellDisplay(master, self, self.gameboard, i, j) for j in range(size)] for i in range(size)]

        # Create a frame for the button and use grid to place it
        self.button_frame = tk.Frame(master)
        self.button_frame.grid(row=7, column=0, columnspan=4)  # Adjust row and columnspan as needed

        # Add the 'Update Board' button inside the frame
        self.reset_btn = tk.Button(self.button_frame, text="Update Board", command=self.reset)
        self.reset_btn.grid(row=0, column=0)



        # # Add an extra non-editable row at the bottom
        # for j in range(size):
        #     CellDisplay(master, self.gameboard, size, j, editable=False)

        # # Add an extra non-editable column on the right
        # for i in range(size + 1):
        #     CellDisplay(master, self.gameboard, i, size, editable=False)

    def update(self, ri, ci):
        for i in range(5):
            for j in range(5):
                if self.cells[i][j].editable:
                    self.cells[i][j].update()

    def reset(self):
        directory_path = '/Users/raffukhondaker/Desktop'  # Replace with your directory path
        self.gameboard = Gameboard()
        self.gameboard.create_board(get_most_recently_added_file(directory_path))
        self.gameboard.print_board()
        self.cells = [[CellDisplay(self.master, self, self.gameboard, i, j) for j in range(self.size)] for i in range(self.size)]


def main():
    root = tk.Tk()
    root.title("Gameboard")
    # gameboard = GameboardDisplay(root, "imgs/Screen Shot 2023-12-17 at 12.59.32 PM.png")
    directory_path = '/Users/raffukhondaker/Desktop'  # Replace with your directory path
    gameboard = GameboardDisplay(root, get_most_recently_added_file(directory_path))
    root.mainloop()

if __name__ == "__main__":
    main()
