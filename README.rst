Linalg: Vector and Matrix Computations Made Easy
================================================

Linalg is an Apache2 licenced library for doing various matrix based
computations. It started out as a project for me to learn both Python and
linear algebra. The linear algebra because I have exams soon, the Python
because I wanted to learn Python.

.. code-block:: pycon

    >>> a = Vector((x + 1) ** 2 for x in range(3))
    >>> print(a)
    <1, 4, 9>
    >>> a.magnitude
    9.899494936611665
    >>> dot_product(a, Vector(1, 4, 3))
    44
    >>> M = (
    ... (1, 2, 3),
    ... (4, 7, 6),
    ... (7, 8, 9))
    >>> A = Matrix(*M)
    >>> print(A.determinant)
    -24
    >>> A * a
    Vector(36, 86, 120)
    >>> A * Vector(1, 2)
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    ValueError: Height of second operand must match width of first operand.
    >>> print(A)
    (<1, 2, 3>, <4, 7, 6>, <7, 8, 9>)
    
