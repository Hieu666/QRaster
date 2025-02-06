import tkinter as tk
from tkinter import ttk

class QRaster:
    def __init__(self, master):
        self.master = master
        self.master.title("QRaster")
        self.master.iconbitmap("app.ico")

        self.grid_size = 21  # Default grid size
        self.cell_size = 20  # Cell size
        self.grid = []
        self.current_row = 0  # Current row
        self.current_col = 0  # Current column
        self.is_toggling = False  # Flag for checking if key is being held
        self.is_space_pressed = False  # Space key flag
        self.is_enter_pressed = False  # Enter key flag

        # Create QR code size selector and grid button
        self.create_size_selector()
        self.create_generate_button()

        # Bind keyboard controls for movement and cell toggling
        self.master.bind("<Up>", self.move_up)
        self.master.bind("<Down>", self.move_down)
        self.master.bind("<Left>", self.move_left)
        self.master.bind("<Right>", self.move_right)
        self.master.bind("<space>", self.toggle_cell)
        self.master.bind("<Return>", self.toggle_cell)
        self.master.bind("<KeyRelease-space>", self.stop_toggling)
        self.master.bind("<KeyRelease-Return>", self.stop_toggling)

    def create_size_selector(self):
        self.size_label = tk.Label(self.master, text="Select QR Code Size:")
        self.size_label.grid(row=0, column=0, padx=10, pady=10)

        sizes = [f"{i}x{i}" for i in range(21, 162, 4)]
        self.size_combobox = ttk.Combobox(self.master, values=sizes, state="readonly")
        self.size_combobox.set("21x21")  # Default selection
        self.size_combobox.grid(row=0, column=1, padx=10, pady=10)

    def create_generate_button(self):
        self.generate_button = tk.Button(self.master, text="Generate QR Grid", command=self.generate_grid)
        self.generate_button.grid(row=1, column=0, columnspan=2, pady=10)

    def generate_grid(self):
        # Get grid size from dropdown
        selected_size = self.size_combobox.get()
        self.grid_size = int(selected_size.split('x')[0])

        # Clear previous grid before generating a new one
        for widget in self.master.grid_slaves():
            widget.grid_forget()

        self.create_grid()

    def create_grid(self):
        self.grid = []
        
        # Add horizontal labels
        for col in range(self.grid_size):
            label = tk.Label(self.master, text=str(col + 1), width=3, anchor='n', relief="flat")
            label.grid(row=1, column=col + 1, sticky="nsew")

        # Add vertical labels
        for row in range(self.grid_size):
            label = tk.Label(self.master, text=str(row + 1), width=3, anchor='e', relief="flat")
            label.grid(row=row + 2, column=0, sticky="nsew")

        # Create cells
        for row in range(self.grid_size):
            row_cells = []
            for col in range(self.grid_size):
                cell = tk.Button(self.master, width=2, height=1, bg='white', relief="flat", 
                                 command=lambda r=row, c=col: self.toggle_cell_from_button(r, c))
                cell.grid(row=row + 2, column=col + 1, sticky="nsew")
                row_cells.append(cell)
            self.grid.append(row_cells)

        # Update QR size label
        self.size_label.config(text=f"QR Code Size: {self.grid_size}x{self.grid_size}")

    def toggle_cell(self, event=None):
        if event:
            if event.keysym == 'space':
                self.is_space_pressed = True
            elif event.keysym == 'Return':
                self.is_enter_pressed = True
        
        # Toggle current cell color between black and white
        current_color = self.grid[self.current_row][self.current_col].cget('bg')
        new_color = 'black' if current_color == 'white' else 'white'
        self.grid[self.current_row][self.current_col].config(bg=new_color)

    def toggle_cell_from_button(self, row, col):
        current_color = self.grid[row][col].cget('bg')
        new_color = 'black' if current_color == 'white' else 'white'
        self.grid[row][col].config(bg=new_color)

    def move_up(self, event):
        if self.current_row > 0:
            self.current_row -= 1
            self.highlight_current_cell()
            if self.is_space_pressed or self.is_enter_pressed:
                self.toggle_cell()

    def move_down(self, event):
        if self.current_row < self.grid_size - 1:
            self.current_row += 1
            self.highlight_current_cell()
            if self.is_space_pressed or self.is_enter_pressed:
                self.toggle_cell()

    def move_left(self, event):
        if self.current_col > 0:
            self.current_col -= 1
            self.highlight_current_cell()
            if self.is_space_pressed or self.is_enter_pressed:
                self.toggle_cell()

    def move_right(self, event):
        if self.current_col < self.grid_size - 1:
            self.current_col += 1
            self.highlight_current_cell()
            if self.is_space_pressed or self.is_enter_pressed:
                self.toggle_cell()

    def highlight_current_cell(self):
        # Remove border from all cells
        for row in self.grid:
            for cell in row:
                cell.config(relief="flat")

        # Add border to the currently selected cell
        self.grid[self.current_row][self.current_col].config(relief="solid", borderwidth=2)

    def stop_toggling(self, event):
        self.is_space_pressed = False
        self.is_enter_pressed = False

if __name__ == "__main__":
    root = tk.Tk()
    app = QRaster(root)
    root.mainloop()
