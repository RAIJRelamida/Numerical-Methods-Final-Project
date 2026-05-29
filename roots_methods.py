import numpy as np
import sympy as sp


class RootsMethods:

    def parse_function(self, expr):

        x = sp.symbols('x')

        f = sp.lambdify(
            x,
            sp.sympify(expr),
            "numpy"
        )

        return f

    # =====================================================
    # INCREMENTAL METHOD
    # =====================================================

    def incremental(self, expr, x0, step, iterations):

        f = self.parse_function(expr)

        table = []

        prev_x = None

        for i in range(iterations):

            x1 = x0 + step

            if prev_x is None:
                error = 0
            else:
                error = abs((x1 - prev_x) / x1) * 100

            table.append([
                i + 1,
                x0,
                x1,
                f(x0),
                f(x1),
                error
            ])

            if f(x0) * f(x1) < 0:
                break

            prev_x = x1
            x0 = x1

        return table

    # =====================================================
    # BISECTION METHOD
    # =====================================================

    def bisection(self, expr, a, b,
                  tol=1e-6,
                  max_iter=100):

        f = self.parse_function(expr)

        table = []

        prev_c = None

        for i in range(max_iter):

            c = (a + b) / 2

            if prev_c is None:
                error = 0
            else:
                error = abs((c - prev_c) / c) * 100

            table.append([
                i + 1,
                a,
                b,
                c,
                f(c),
                error
            ])

            if abs(f(c)) < tol:
                break

            if f(a) * f(c) < 0:
                b = c
            else:
                a = c

            prev_c = c

        return table

    # =====================================================
    # REGULA FALSI
    # =====================================================

    def regula_falsi(self, expr, a, b,
                     tol=1e-6,
                     max_iter=100):

        f = self.parse_function(expr)

        table = []

        prev_c = None

        for i in range(max_iter):

            c = (
                a * f(b) - b * f(a)
            ) / (
                f(b) - f(a)
            )

            if prev_c is None:
                error = 0
            else:
                error = abs((c - prev_c) / c) * 100

            table.append([
                i + 1,
                a,
                b,
                c,
                f(c),
                error
            ])

            if abs(f(c)) < tol:
                break

            if f(a) * f(c) < 0:
                b = c
            else:
                a = c

            prev_c = c

        return table

    # =====================================================
    # NEWTON RAPHSON
    # =====================================================

    def newton_raphson(self, expr,
                       x0,
                       tol=1e-6,
                       max_iter=100):

        x = sp.symbols('x')

        f_expr = sp.sympify(expr)

        df_expr = sp.diff(f_expr, x)

        f = sp.lambdify(x, f_expr, "numpy")

        df = sp.lambdify(x, df_expr, "numpy")

        table = []

        for i in range(max_iter):

            x1 = x0 - f(x0) / df(x0)

            error = abs((x1 - x0) / x1) * 100

            table.append([
                i + 1,
                x0,
                x1,
                f(x1),
                error
            ])

            if abs(f(x1)) < tol:
                break

            x0 = x1

        return table

    # =====================================================
    # SECANT METHOD
    # =====================================================

    def secant(self, expr,
               x0,
               x1,
               tol=1e-6,
               max_iter=100):

        f = self.parse_function(expr)

        table = []

        for i in range(max_iter):

            x2 = x1 - (
                f(x1) * (x1 - x0)
            ) / (
                f(x1) - f(x0)
            )

            error = abs((x2 - x1) / x2) * 100

            table.append([
                i + 1,
                x0,
                x1,
                x2,
                f(x2),
                error
            ])

            if abs(f(x2)) < tol:
                break

            x0 = x1
            x1 = x2

        return table