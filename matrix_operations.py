import numpy as np


class MatrixOperations:

    # ================= SAFE ADD =================
    def add(self, A, B):
        if A.shape != B.shape:
            raise ValueError("Addition requires same dimensions")
        return np.add(A, B)

    # ================= SAFE MULTIPLY =================
    def multiply(self, A, B):
        if A.shape[1] != B.shape[0]:
            raise ValueError("Invalid multiplication dimensions")
        return np.matmul(A, B)

    # ================= TRANSPOSE =================
    def transpose(self, A):
        return np.transpose(A)

    # ================= DETERMINANT =================
    def determinant(self, A):
        if A.shape[0] != A.shape[1]:
            raise ValueError("Determinant requires square matrix")
        return np.linalg.det(A)

    # ================= INVERSE =================
    def inverse(self, A):
        if A.shape[0] != A.shape[1]:
            raise ValueError("Inverse requires square matrix")
        return np.linalg.inv(A)

    # ================= ADJOINT =================
    def adjoint(self, A):
        if A.shape[0] != A.shape[1]:
            raise ValueError("Adjoint requires square matrix")

        det = np.linalg.det(A)

        if np.isclose(det, 0):
            raise ValueError("Matrix is singular (no adjoint via inverse method)")

        inv = np.linalg.inv(A)
        return det * inv

    # ================= POWER =================
    def power(self, A, n):
        if A.shape[0] != A.shape[1]:
            raise ValueError("Power requires square matrix")
        return np.linalg.matrix_power(A, n)

    # ================= SOLVE AX = B =================
    def solve_equations(self, A, B):
        if A.shape[0] != A.shape[1]:
            raise ValueError("A must be square for solving equations")

        if A.shape[0] != B.shape[0]:
            raise ValueError("Row mismatch between A and B")

        return np.linalg.solve(A, B)