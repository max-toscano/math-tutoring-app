"""
tools/math/linear_algebra.py
Linear algebra computation using NumPy.

Handles: matrix operations, determinants, eigenvalues, row reduction,
matrix inverse, matrix multiplication, solving linear systems.

This is a real tool — NumPy does exact matrix computation
that LLMs frequently get wrong (especially with larger matrices).
"""

import numpy as np
from langchain_core.tools import tool
import json


def compute_linear_algebra(matrix_a: list, operation: str, matrix_b: list = None, vector_b: list = None) -> dict:
    """
    Perform a linear algebra computation.

    Args:
        matrix_a: 2D list representing the primary matrix.
        operation: determinant | inverse | eigenvalues | transpose |
                   multiply | solve | rref | rank | trace
        matrix_b: Optional second matrix for multiplication.
        vector_b: Optional vector for solving Ax = b.

    Returns:
        Dict with input, operation, result, error.
    """
    try:
        A = np.array(matrix_a, dtype=float)

        if operation == "determinant":
            if A.shape[0] != A.shape[1]:
                return {"error": "Matrix must be square for determinant"}
            det = float(np.linalg.det(A))
            return {"operation": operation, "matrix": matrix_a, "result": round(det, 8), "error": None}

        elif operation == "inverse":
            if A.shape[0] != A.shape[1]:
                return {"error": "Matrix must be square for inverse"}
            det = np.linalg.det(A)
            if abs(det) < 1e-10:
                return {"error": "Matrix is singular (determinant ≈ 0), no inverse exists"}
            inv = np.linalg.inv(A)
            return {"operation": operation, "matrix": matrix_a, "result": inv.round(6).tolist(), "error": None}

        elif operation == "eigenvalues":
            if A.shape[0] != A.shape[1]:
                return {"error": "Matrix must be square for eigenvalues"}
            eigenvalues, eigenvectors = np.linalg.eig(A)
            return {
                "operation": operation,
                "matrix": matrix_a,
                "eigenvalues": [round(float(v.real), 6) for v in eigenvalues],
                "eigenvectors": eigenvectors.round(6).tolist(),
                "error": None,
            }

        elif operation == "transpose":
            result = A.T
            return {"operation": operation, "matrix": matrix_a, "result": result.tolist(), "error": None}

        elif operation == "multiply":
            if matrix_b is None:
                return {"error": "matrix_b required for multiplication"}
            B = np.array(matrix_b, dtype=float)
            if A.shape[1] != B.shape[0]:
                return {"error": f"Incompatible dimensions: {A.shape} × {B.shape}"}
            result = A @ B
            return {"operation": operation, "matrix_a": matrix_a, "matrix_b": matrix_b, "result": result.round(6).tolist(), "error": None}

        elif operation == "solve":
            # Solve Ax = b
            if vector_b is None:
                return {"error": "vector_b required for solving Ax = b"}
            b = np.array(vector_b, dtype=float)
            if A.shape[0] != A.shape[1]:
                return {"error": "Matrix must be square for direct solving"}
            solution = np.linalg.solve(A, b)
            return {"operation": operation, "matrix": matrix_a, "vector_b": vector_b, "solution": solution.round(6).tolist(), "error": None}

        elif operation == "rank":
            rank = int(np.linalg.matrix_rank(A))
            return {"operation": operation, "matrix": matrix_a, "result": rank, "error": None}

        elif operation == "trace":
            if A.shape[0] != A.shape[1]:
                return {"error": "Matrix must be square for trace"}
            result = float(np.trace(A))
            return {"operation": operation, "matrix": matrix_a, "result": round(result, 6), "error": None}

        elif operation == "rref":
            # Row echelon form using Gaussian elimination
            from sympy import Matrix as SympyMatrix
            M = SympyMatrix(matrix_a)
            rref_matrix, pivot_cols = M.rref()
            return {
                "operation": operation,
                "matrix": matrix_a,
                "result": [[float(x) for x in row] for row in rref_matrix.tolist()],
                "pivot_columns": list(pivot_cols),
                "error": None,
            }

        else:
            return {"operation": operation, "error": f"Unknown operation: {operation}"}

    except Exception as e:
        return {"operation": operation, "error": str(e)}


@tool
def linear_algebra(matrix_a: str, operation: str, matrix_b: str = "null", vector_b: str = "null") -> str:
    """Compute linear algebra using NumPy. Operations: determinant, inverse, eigenvalues, transpose, multiply, solve, rref, rank, trace.

    Args:
        matrix_a: JSON 2D array representing the matrix (e.g. '[[1,2],[3,4]]')
        operation: What to compute
        matrix_b: Optional second matrix as JSON (for multiply)
        vector_b: Optional vector as JSON (for solve)
    """
    a = json.loads(matrix_a) if isinstance(matrix_a, str) else matrix_a
    b = json.loads(matrix_b) if matrix_b and matrix_b != "null" else None
    vb = json.loads(vector_b) if vector_b and vector_b != "null" else None
    return json.dumps(compute_linear_algebra(a, operation, b, vb))
