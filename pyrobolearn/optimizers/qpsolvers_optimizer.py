#!/usr/bin/env python
"""Provide a wrapper around quadratic programming solvers.

References:
    [1] https://github.com/stephane-caron/qpsolvers
"""

import numpy as np

# CVXOPT
# import cvxopt
# CVXPY: nice wrapper around cvxopt
# import cvxpy
# Quadprog
# import quadprog

# QPsolvers optimizers: unified Python interface for multiple QP solvers (cvxopt, cvxpy, quadprog,...)
try:
    import qpsolvers
except ImportError as e:
    raise ImportError(e.__str__() + "\n HINT: you can install qpsolvers directly via 'pip install qpsolvers'.")

from optimizer import Optimizer

__author__ = "Brian Delhaisse"
__copyright__ = "Copyright 2018, PyRoboLearn"
__credits__ = ["Brian Delhaisse"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Brian Delhaisse"
__email__ = "briandelhaisse@gmail.com"
__status__ = "Development"


# class CVXOPT(Optimizer):
#     r"""Convex Optimizer
#
#     Note: cvxpy module is a nice wrapper around cvxopt that follows paradigm of a disciplined convex programming.
#
#     References:
#         [1] Python Software for Convex Optimization: https://cvxopt.org/
#         [2] Github repo: https://github.com/cvxopt/cvxopt
#     """
#     pass
#
#
# class CVXPY(Optimizer):
#     r"""Convex Optimizer
#
#     References:
#         [1] CVXPY: http://www.cvxpy.org/
#         [2] Github repo: https://github.com/cvxgrp/cvxpy
#     """
#     pass
#
#
# class QuadProg(object):
#     r"""Quadprog
#
#     References:
#         [1] Github repo: https://github.com/rmcgibbo/quadprog
#     """
#     pass

class QP(object):
    r"""Quadratic Programming solvers

    This class uses the `qpsolvers` which is a unified Python interface for multiple QP solvers [1,2].

    .. math::

        \min_{x \in R^n} \frac{1}{2} x^T P x + q^T x

    subject to

    .. math::

        Gx \leq h
        Ax = b

    where :math:`x` is the vector of optimization variables, the matrix :math:`P` and vector :math:`q` are used to
    define any quadratic objective function on these variables, while the matrix-vector couples :math:`(G,h)` and
    :math:`(A,b)` respectively define inequality and equality constraints. Vector inequalities apply coordinate by
    coordinate [1].

    - Dense solvers:
        - CVXOPT
        - CVXPY
        - qpOASES
        - quadprog
    - Sparse solvers:
        - ECOS as wrapped by CVXPY
        - Gurobi
        - MOSEK
        - OSQP

    Check the available solvers by calling `print(qpsolvers.available_solvers)`.

    Notes: Many solvers (including CVXOPT, OSQP and quadprog) assume that `P` is a symmetric matrix, and may return
    erroneous results when that is not the case. You can set ``sym_proj=True`` to project `P` on its symmetric part,
    at the cost of some computation time.

    References:
        [1] QP in Python: https://scaron.info/blog/quadratic-programming-in-python.html
        [2] Github repo: https://github.com/stephane-caron/qpsolvers
    """

    def __init__(self, method='quadprog'):
        """
        Initialize the QP solver.

        Args:
            method (str): ['cvxopt', 'cvxpy', 'ecos', 'gurobi', 'mosek', 'osqp', 'qpoases', 'quadprog']
        """
        solvers = set(qpsolvers.available_solvers)
        if len(solvers) == 0:
            raise ValueError("No QP solvers have been found on this computer. Please install one of the QP modules")
        if method not in solvers:
            method = 'quadprog'
        self.method = method

        # check methods that require a symmetric matrix for P
        methods = ['cvxopt', 'osqp', 'quadprog']
        self.sym_proj = True if self.method in set(methods) else False

    def is_symmetric(self, X, tol=1e-8):
        return np.allclose(X, X.T, atol=tol)

    def optimize(self, P, q, x0=None, G=None, h=None, A=None, b=None):
        return qpsolvers.solve_qp(P, q, G, h, A, b, solver=self.method, initvals=x0, sym_proj=self.sym_proj)