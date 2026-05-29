import tkinter as tk
from tkinter import ttk, messagebox

import matplotlib.pyplot as plt
import numpy as np
import sympy as sp


class RootsUI:

    def __init__(self,
                 root,
                 method,
                 roots_methods):

        self.root = root

        # Hide main window
        self.root.withdraw()

        self.window = tk.Toplevel(root)

        self.window.title(method)

        self.window.geometry("1100x700")

        self.window.configure(bg="#1a1a1a")

        self.window.resizable(False, False)

        self.method = method

        self.roots_methods = roots_methods

        # Handle close button
        self.window.protocol(
            "WM_DELETE_WINDOW",
            self.go_back
        )

        self.build_ui()

    # =====================================================
    # BACK FUNCTION
    # =====================================================

    def go_back(self):

        self.window.destroy()

        self.root.deiconify()

    # =====================================================
    # UI
    # =====================================================

    def build_ui(self):

        # ==========================================
        # BACK BUTTON
        # ==========================================

        back_btn = tk.Button(
            self.window,
            text="← Back",
            command=self.go_back,
            font=("Arial", 10, "bold"),
            bg="#333333",
            fg="white",
            relief=tk.FLAT,
            cursor="hand2"
        )

        back_btn.pack(
            anchor="nw",
            padx=10,
            pady=10
        )

        # ==========================================
        # TITLE
        # ==========================================

        title = tk.Label(
            self.window,
            text=self.method,
            font=("Arial", 20, "bold"),
            fg="white",
            bg="#1a1a1a"
        )

        title.pack(pady=10)

        # ==========================================
        # EQUATION INPUT
        # ==========================================

        equation_frame = tk.Frame(
            self.window,
            bg="#1a1a1a"
        )

        equation_frame.pack(pady=10)

        tk.Label(
            equation_frame,
            text="Equation f(x):",
            fg="white",
            bg="#1a1a1a",
            font=("Arial", 12)
        ).grid(row=0, column=0, padx=10)

        self.function_entry = tk.Entry(
            equation_frame,
            width=40,
            font=("Consolas", 12),
            bg="#2a2a2a",
            fg="white",
            insertbackground="white"
        )

        self.function_entry.grid(
            row=0,
            column=1,
            padx=10
        )

        # ==========================================
        # XL INPUT
        # ==========================================

        tk.Label(
            equation_frame,
            text="xl:",
            fg="white",
            bg="#1a1a1a",
            font=("Arial", 12)
        ).grid(row=1, column=0, padx=10, pady=10)

        self.xl_entry = tk.Entry(
            equation_frame,
            width=20,
            font=("Consolas", 12),
            bg="#2a2a2a",
            fg="white",
            insertbackground="white"
        )

        self.xl_entry.grid(
            row=1,
            column=1,
            sticky="w",
            padx=10,
            pady=10
        )

        # ==========================================
        # XU INPUT
        # ==========================================

        tk.Label(
            equation_frame,
            text="xu:",
            fg="white",
            bg="#1a1a1a",
            font=("Arial", 12)
        ).grid(row=2, column=0, padx=10, pady=10)

        self.xu_entry = tk.Entry(
            equation_frame,
            width=20,
            font=("Consolas", 12),
            bg="#2a2a2a",
            fg="white",
            insertbackground="white"
        )

        self.xu_entry.grid(
            row=2,
            column=1,
            sticky="w",
            padx=10,
            pady=10
        )

        # ==========================================
        # SOLVE BUTTON
        # ==========================================

        solve_btn = tk.Button(
            self.window,
            text="Solve",
            command=self.solve,
            font=("Arial", 12, "bold"),
            bg="#2a2a2a",
            fg="white",
            width=20,
            cursor="hand2"
        )

        solve_btn.pack(pady=10)

        # ==========================================
        # TABLE STYLE
        # ==========================================

        style = ttk.Style()

        style.theme_use("clam")

        style.configure(
            "Treeview",
            background="#2a2a2a",
            foreground="white",
            fieldbackground="#2a2a2a",
            rowheight=30,
            font=("Consolas", 10)
        )

        style.configure(
            "Treeview.Heading",
            background="#111111",
            foreground="white",
            font=("Arial", 10, "bold")
        )

        # ==========================================
        # TABLE FRAME
        # ==========================================

        table_frame = tk.Frame(
            self.window,
            bg="#1a1a1a"
        )

        table_frame.pack(
            pady=10,
            padx=10,
            fill="both",
            expand=True
        )

        scrollbar_y = ttk.Scrollbar(
            table_frame,
            orient="vertical"
        )

        scrollbar_y.pack(
            side="right",
            fill="y"
        )

        scrollbar_x = ttk.Scrollbar(
            table_frame,
            orient="horizontal"
        )

        scrollbar_x.pack(
            side="bottom",
            fill="x"
        )

        self.table = ttk.Treeview(
            table_frame,
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set,
            show="headings"
        )

        scrollbar_y.config(
            command=self.table.yview
        )

        scrollbar_x.config(
            command=self.table.xview
        )

        self.table.pack(
            fill="both",
            expand=True
        )

    # =====================================================
    # SOLVE
    # =====================================================

    def solve(self):

        expr = self.function_entry.get()

        try:

            xl = float(self.xl_entry.get())
            xu = float(self.xu_entry.get())

            # ======================================
            # METHOD SELECTION
            # ======================================

            if self.method == "Bisection":

                table = self.roots_methods.bisection(
                    expr,
                    xl,
                    xu
                )

                columns = (
                    "Iter",
                    "xl",
                    "xu",
                    "xr",
                    "f(xr)",
                    "Error %"
                )

            elif self.method == "Regula Falsi":

                table = self.roots_methods.regula_falsi(
                    expr,
                    xl,
                    xu
                )

                columns = (
                    "Iter",
                    "xl",
                    "xu",
                    "xr",
                    "f(xr)",
                    "Error %"
                )

            elif self.method == "Newton-Raphson":

                table = self.roots_methods.newton_raphson(
                    expr,
                    xl
                )

                columns = (
                    "Iter",
                    "x0",
                    "x1",
                    "f(x1)",
                    "Error %"
                )

            elif self.method == "Secant":

                table = self.roots_methods.secant(
                    expr,
                    xl,
                    xu
                )

                columns = (
                    "Iter",
                    "xl",
                    "xu",
                    "xr",
                    "f(xr)",
                    "Error %"
                )

            else:

                table = self.roots_methods.incremental(
                    expr,
                    xl,
                    xu,
                    20
                )

                columns = (
                    "Iter",
                    "xl",
                    "xu",
                    "f(xl)",
                    "f(xu)",
                    "Error %"
                )

            # ======================================
            # CLEAR TABLE
            # ======================================

            for item in self.table.get_children():
                self.table.delete(item)

            # ======================================
            # SET COLUMNS
            # ======================================

            self.table["columns"] = columns

            for col in columns:

                self.table.heading(
                    col,
                    text=col
                )

                self.table.column(
                    col,
                    width=150,
                    anchor="center"
                )

            # ======================================
            # INSERT DATA
            # ======================================

            for row in table:

                formatted_row = []

                for value in row:

                    if isinstance(value, float):

                        formatted_row.append(
                            f"{value:.6f}"
                        )

                    else:

                        formatted_row.append(value)

                self.table.insert(
                    "",
                    tk.END,
                    values=formatted_row
                )

            # ======================================
            # SHOW GRAPH
            # ======================================

            self.plot_graph(expr)

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    # =====================================================
    # GRAPH
    # =====================================================

    def plot_graph(self, expr):

        x = sp.symbols('x')

        f = sp.lambdify(
            x,
            sp.sympify(expr),
            "numpy"
        )

        xs = np.linspace(-10, 10, 500)

        ys = f(xs)

        plt.figure(
            figsize=(8, 5)
        )

        plt.plot(
            xs,
            ys,
            color="cyan",
            linewidth=2
        )

        plt.axhline(
            0,
            color="red"
        )

        plt.axvline(
            0,
            color="white"
        )

        plt.grid(True)

        plt.title(
            f"Graph of {expr}"
        )

        plt.xlabel("x")

        plt.ylabel("f(x)")

        plt.show()
