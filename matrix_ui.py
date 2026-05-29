import tkinter as tk
from tkinter import messagebox, simpledialog
import numpy as np

from styles import get_style, get_fonts, style_entry, style_button, style_label


class MatrixUI:

    def __init__(self, root, matrix_ops):

        self.root = root
        self.root.withdraw()

        self.window = tk.Toplevel(root)
        self.window.title("Matrix Calculator Pro")
        self.window.geometry("1300x820")

        self.matrix_ops = matrix_ops

        self.A_cells = []
        self.B_cells = []

        self.STYLE = get_style()
        self.FONTS = get_fonts()

        self.build_ui()

        self.window.protocol("WM_DELETE_WINDOW", self.go_back)

    # ================= BACK =================
    def go_back(self):
        self.window.destroy()
        self.root.deiconify()

    # ================= MATRIX =================
    def get_matrix(self, cells):
        try:
            return np.array([
                [float(c.get()) for c in row]
                for row in cells
            ])
        except:
            messagebox.showerror("Error", "Invalid matrix values")
            return None

    # ================= GRID =================
    def make_grid(self, parent, rows, cols, store):

        # 🔥 FULL REPLACE MODE
        for widget in parent.winfo_children():
            widget.destroy()

        store.clear()

        for i in range(rows):
            row = []
            for j in range(cols):
                e = tk.Entry(
                    parent,
                    width=6,
                    font=self.FONTS["grid"],
                    justify="center"
                )

                style_entry(e)

                e.grid(row=i, column=j, padx=2, pady=2)
                e.insert(0, "0")
                row.append(e)

            store.append(row)

    # ================= UI =================
    def build_ui(self):

        # BACK BUTTON
        back_btn = tk.Button(
            self.window,
            text="← Back",
            command=self.go_back
        )
        style_button(back_btn)
        back_btn.pack(anchor="nw", padx=10, pady=10)

        # TITLE
        title = tk.Label(
            self.window,
            text="Matrix Calculator Pro",
            font=self.FONTS["title"]
        )
        style_label(title)
        title.pack(pady=5)

        # ================= SIZE CONTROLS =================
        size = tk.Frame(self.window, bg=self.STYLE["bg"])
        size.pack(pady=8)

        self.ar = tk.Entry(size, width=5)
        self.ac = tk.Entry(size, width=5)
        self.br = tk.Entry(size, width=5)
        self.bc = tk.Entry(size, width=5)

        for e in [self.ar, self.ac, self.br, self.bc]:
            style_entry(e)

        tk.Label(size, text="A r", bg=self.STYLE["bg"], fg=self.STYLE["fg"]).grid(row=0, column=0)
        self.ar.grid(row=1, column=0)

        tk.Label(size, text="A c", bg=self.STYLE["bg"], fg=self.STYLE["fg"]).grid(row=0, column=1)
        self.ac.grid(row=1, column=1)

        tk.Label(size, text="B r", bg=self.STYLE["bg"], fg=self.STYLE["fg"]).grid(row=0, column=2)
        self.br.grid(row=1, column=2)

        tk.Label(size, text="B c", bg=self.STYLE["bg"], fg=self.STYLE["fg"]).grid(row=0, column=3)
        self.bc.grid(row=1, column=3)

        gen_btn = tk.Button(size, text="Generate", command=self.generate)
        style_button(gen_btn)
        gen_btn.grid(row=1, column=4, padx=10)

        # ================= MATRICES =================
        mat = tk.Frame(self.window, bg=self.STYLE["bg"])
        mat.pack()

        tk.Label(mat, text="Matrix A", bg=self.STYLE["bg"], fg=self.STYLE["fg"]).grid(row=0, column=0)
        tk.Label(mat, text="Matrix B", bg=self.STYLE["bg"], fg=self.STYLE["fg"]).grid(row=0, column=1)

        self.frame_a = tk.Frame(mat, bg=self.STYLE["bg"])
        self.frame_b = tk.Frame(mat, bg=self.STYLE["bg"])

        self.frame_a.grid(row=1, column=0, padx=15)
        self.frame_b.grid(row=1, column=1, padx=15)

        # default grids
        self.make_grid(self.frame_a, 2, 2, self.A_cells)
        self.make_grid(self.frame_b, 2, 2, self.B_cells)

        # ================= OPERATIONS =================
        btn = tk.Frame(self.window, bg=self.STYLE["bg"])
        btn.pack(pady=10)

        buttons = [
            ("A + B", self.add),
            ("A × B", self.multiply),
            ("Solve Ax=B", self.solve_eq),

            ("Transpose A", lambda: self.unary(self.matrix_ops.transpose, self.A_cells)),
            ("Inverse A", lambda: self.unary(self.matrix_ops.inverse, self.A_cells)),
            ("Det A", lambda: self.unary(self.matrix_ops.determinant, self.A_cells)),
            ("Adj A", lambda: self.unary(self.matrix_ops.adjoint, self.A_cells)),

            ("Transpose B", lambda: self.unary(self.matrix_ops.transpose, self.B_cells)),
            ("Inverse B", lambda: self.unary(self.matrix_ops.inverse, self.B_cells)),
            ("Det B", lambda: self.unary(self.matrix_ops.determinant, self.B_cells)),
            ("Adj B", lambda: self.unary(self.matrix_ops.adjoint, self.B_cells)),

            ("Power A", lambda: self.power("A")),
            ("Power B", lambda: self.power("B")),
        ]

        for i, (t, c) in enumerate(buttons):
            b = tk.Button(
                btn,
                text=t,
                width=14,
                height=2,
                command=c
            )
            style_button(b)
            b.grid(row=i // 4, column=i % 4, padx=5, pady=5)

        # ================= OUTPUT =================
        self.out = tk.Text(
            self.window,
            height=10,
            bg="#111111",
            fg="white",
            font=("Consolas", 13),
            wrap="none"
        )
        self.out.pack(fill="both", expand=True, padx=20, pady=10)

    # ================= GENERATE =================
    def generate(self):
        try:
            ar = int(self.ar.get())
            ac = int(self.ac.get())
            br = int(self.br.get())
            bc = int(self.bc.get())

            self.make_grid(self.frame_a, ar, ac, self.A_cells)
            self.make_grid(self.frame_b, br, bc, self.B_cells)

        except:
            messagebox.showerror("Error", "Invalid size input")

    # ================= OUTPUT =================
    def show(self, r):

        self.out.delete("1.0", tk.END)

        text = str(r)

        # Convert numpy array nicely
        if isinstance(r, np.ndarray):
            text = np.array2string(
                r,
                precision=4,
                suppress_small=True
            )

        # Center formatting
        lines = text.split("\n")
        width = 60  # visual center width

        centered = "\n".join(
            line.center(width) for line in lines
        )

        self.out.insert(tk.END, centered)

    # ================= HELPERS =================
    def unary(self, func, cells):
        mat = self.get_matrix(cells)
        if mat is None:
            return
        self.show(func(mat))

    # ================= OPERATIONS =================
    def add(self):
        A = self.get_matrix(self.A_cells)
        B = self.get_matrix(self.B_cells)
        if A is None or B is None:
            return
        self.show(self.matrix_ops.add(A, B))

    def multiply(self):
        A = self.get_matrix(self.A_cells)
        B = self.get_matrix(self.B_cells)
        if A is None or B is None:
            return
        self.show(self.matrix_ops.multiply(A, B))

    def solve_eq(self):
        A = self.get_matrix(self.A_cells)
        B = self.get_matrix(self.B_cells)

        if A is None or B is None:
            return

        if A.shape[0] != A.shape[1]:
            messagebox.showerror("Error", "A must be square")
            return

        if A.shape[0] != B.shape[0]:
            messagebox.showerror("Error", "Dimension mismatch")
            return

        try:
            x = self.matrix_ops.solve_equations(A, B)
            self.show(x)
        except np.linalg.LinAlgError:
            messagebox.showerror("Error", "Singular matrix")

    # ================= POWER =================
    def power(self, target):

        mat = self.get_matrix(self.A_cells if target == "A" else self.B_cells)

        if mat is None:
            return

        n = simpledialog.askinteger(
            "Matrix Power",
            "Enter power n:",
            minvalue=0
        )

        if n is None:
            return

        self.show(self.matrix_ops.power(mat, n))