# coding: utf-8

"""Various functions used on vectors and matrices that are useful on their
own and within linalg itself.
"""

from .vector import Vector
from .matrix import Matrix

def kronecker_delta (i, j):
    """Return 1 if i == j and 0 otherwise."""
    return 1 if i == j else 0

def levi_civita (i, j, k):
    """The 3D Levi-Civita symbol.
    
    The Levi-Civita symbol is defined as follows:
    * +1 if (i, j, k) is an even permutation of (1, 2, 3),
    * -1 if (i, j, k) is an odd permutation of (1, 2, 3),
    * 0 otherwise (i.e. two elements are repeated).
    
    Examples
    --------
    >>> levi_civita(1, 2, 3)
    1
    >>> levi_civita(1, 3, 3)
    0
    >>> levi_civita(2, 1, 3)
    -1
    """
    if (i, j, k) in ((1, 2, 3), (3, 1, 2), (2, 3, 1)):
        return 1
    elif (i, j, k) in ((1, 3, 2), (2, 1, 3), (3, 2, 1)):
        return -1
    else:
        return 0

def leading_entry (v):
    """Return the index of the first non-zero element.
    
    If v is a zero vector, the function returns len(v).
    """
    idx = 0
    while idx < len(v) and v[idx] == 0:
        idx += 1
    return idx

def inner_product (a, b):
    """Return the {inner, dot, scalar} product of a and b.
    
    Example
    -------
    >>> inner_product(Vector(1, 2, 3), Vector(2, 7, 9))
    43
    """
    return sum(x * y for x, y in zip(a, b))

dot_product = inner_product
scalar_product = inner_product

def vector_product (a, b):
    """Return the vector or cross product of a and b.
    
    That is the mutually orthogonal vector with magnitude |a||b|sin(x)
    where x is the angle made by a and b. In a right handed system, the
    resultant vector will have positive direction in the direction that
    a conventional screw would move (up or down) were it rotated from a
    to b in the plane they generate.
    
    Examples
    --------
    >>> vector_product(i, j)
    Vector(0, 0, 1)
    >>> vector_product(j, i)
    Vector(0, 0, -1)
    >>> a = Vector(1, 2, 5)
    >>> b = Vector(-2, 4, 6)
    >>> cross_product(a, b)
    Vector(-8, -16, 8)
    """
    return Vector(a[i] * b[i + 1] - a[i + 1] * b[i] for i in range(-2, 1))

cross_product = vector_product

def scalar_triple_product (a, b, c):
    u"""Return the scalar triple product (a·(b ⨉ c))."""
    return inner_product(a, vector_product(b, c))

def vector_triple_product (a, b, c):
    u"""Return the vector triple product of three vectors.
    
    The vector triple product of three vectors a, b and c is defined
    to be a ⨉ (b ⨉ c), which is in fact equal to (a·c) b - (a·b) c.
    """
    return Vector(inner_product(a, c) * Vector(b) -
                  inner_product(a, b) * Vector(c))

def e (direction, dimensions):
    """Return a unit vector in a base direction.
    
    Examples
    --------
    >>> e(0, 3) # i
    Vector((1, 0, 0))
    >>> e(7, 9)
    Vector((0, 0, 0, 0, 0, 0, 0, 1, 0))
    >>> e(0, 1)
    Vector((1))
    """
    return Vector(kronecker_delta(i, direction) for i in range(dimensions))

def zero_vector (dimensions):
    """Return a vector filled with zeroes.
    
    Example
    -------
    >>> zero_vector(5)
    Vector((0, 0, 0, 0, 0))
    """
    return Vector([0] * dimensions)

i = e(0, 3)
j = e(1, 3)
k = e(2, 3)

def echelon_form (M):
    """Return the matrix in row echelon form.
    
    Examples
    --------
    >>> A = Matrix((1, 2, 3), (4, 5, 6), (7, 8, 9))
    >>> echelon_form(A)
    Matrix((1, 2, 3), (0.0, -3.0, -6.0), (0.0, 0.0, 0.0))
    """
    rows = list(M.rows())
    for idx, row in enumerate(rows):
        lead = leading_entry(row)
        if lead == M.width:
            continue
        for i in range(idx + 1, M.height):
            if leading_entry(rows[i]) == lead:
                rows[i] -= row * (rows[i][lead] / row[lead])
            else:
                continue
    rows.sort(key=leading_entry)
    return Matrix(*rows)

def identity (n):
    """Return the n by n identity matrix.
    
    Example
    -------
    >>> identity(2)
    Matrix((1, 0), (0, 1))
    """
    return Matrix(
        *([kronecker_delta(i, j) for i in range(n)] for j in range(n)))
