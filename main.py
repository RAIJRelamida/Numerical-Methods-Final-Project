import tkinter as tk
from roots_methods import RootsMethods
from matrix_operations import MatrixOperations
from roots_ui import RootsUI
from matrix_ui import MatrixUI


class RootsMatricesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Roots and Matrices Solver")
        self.root.geometry("1000x700")  
        self.root.configure(bg='#1a1a1a')

        self.roots_methods = RootsMethods()
        self.matrix_ops = MatrixOperations()

        self.create_main_menu()
 
    def create_main_menu(self):
        self.clear_window()

        tk.Label(
            self.root,
            text="Roots and Matrices Solver",
            font=("Arial", 28, "bold"),
            fg="white",
            bg="#1a1a1a"
        ).pack(pady=50)

        tk.Label(
            self.root,
            text="Numerical Methods and Linear Algebra",
            fg="#cccccc",
            bg="#1a1a1a"
        ).pack()

        btn_frame = tk.Frame(self.root, bg="#1a1a1a")
        btn_frame.pack(pady=50)

        tk.Button(
            btn_frame,
            text="Find Roots",
            width=30,
            height=3,
            bg="#2a2a2a",
            fg="white",
            command=self.show_roots_menu
        ).pack(pady=20)

        # ✅ DIRECT MATRIX CALCULATOR
        tk.Button(
            btn_frame,
            text="Matrix Calculator",
            width=30,
            height=3,
            bg="#2a2a2a",
            fg="white",
            command=self.open_matrix
        ).pack(pady=20)

        tk.Button(
            btn_frame,
            text="Exit",
            width=20,
            bg="#444444",
            fg="white",
            command=self.root.quit
        ).pack(pady=20)

    def show_roots_menu(self):
        self.clear_window()

        tk.Button(
            self.root,
            text="← Back",
            command=self.create_main_menu,
            bg="#444"
        ).pack(anchor="nw", padx=10, pady=10)

        tk.Label(
            self.root,
            text="Root Finding Methods",
            font=("Arial", 20, "bold"),
            fg="white",
            bg="#1a1a1a"
        ).pack(pady=20)

        methods = [
            "Incremental Method",
            "Bisection",
            "Regula Falsi",
            "Newton-Raphson",
            "Secant"
        ]

        for m in methods:
            tk.Button(
                self.root,
                text=m,
                width=40,
                height=2,
                bg="#2a2a2a",
                fg="white",
                command=lambda mm=m: self.open_roots(mm)
            ).pack(pady=10)

    def open_roots(self, method):
        RootsUI(self.root, method, self.roots_methods)

    # ✅ MATRIX OPENS DIRECTLY
    def open_matrix(self):
        MatrixUI(self.root, self.matrix_ops)

    def clear_window(self):
        for w in self.root.winfo_children():
            w.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = RootsMatricesApp(root)
    root.mainloop()