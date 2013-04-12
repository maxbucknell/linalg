from .vector import Vector
from collections import Iterable
from numbers import Number

class Matrix:
    
    """Matrix is initialised by giving a number of iterable objects.
    
    Example
    -------
    >>> str(Matrix([1, 0], [0, 1]))
    (<1, 0>, <0, 1>)
    """
    
    def __init__ (self, *args, columns=False):
        self._m = tuple(tuple(row) for row in args)
        # Check that all rows are the same length
        if len(set(len(row) for row in self._m)) > 1:
            raise ValueError("All {} must be the same length.".format(
                "columns" if columns else "rows"
            ))
        if columns:
            # We store the matrix internally as rows
            self._m = tuple(zip(*self._m))
        
        self._h = len(self._m)
        self._w = len(self._m[0]) if self._h else 0
        
        # An empty matrix is an empty matrix
        if 0 in (self.height, self.width):
            self._m = ((),)
            self._h = 0
            self._w = 0
    
    @property
    def width (self):
        """Return the width, which is to say the number of columns."""
        return self._w
    
    @property
    def height (self):
        """Return the height, which is to say the number of rows."""
        return self._h
    
    @property
    def dimensions (self):
        """Return a tuple of the width and height."""
        return (self.width, self.height)
    
    @property
    def is_square (self):
        """Return whether or not the matrix is square."""
        return self.width == self.height
    
    @property
    def determinant (self):
        """Return the determinant of a square matrix."""
        if self.is_square:
            det = 1
            for idx, row in enumerate(self.row_echelon_form().rows()):
                det *= row[idx]
            return det
        else:
            raise NotImplementedError(
                "Determinant only defined for square matrices.")
    
    def row (self, i):
        """Return the ith row."""
        return Vector(self._m[i])
    
    def rows (self):
        """Return an iterator for the rows."""
        for row in self._m:
            yield Vector(row)
    
    def column (self, i):
        """Return the ith column."""
        return Vector(tuple(zip(*self._m))[i])
    
    def columns (self):
        """Return an iterator for the columns.
        
        Example
        -------
        >>> A = Matrix((11, 12, 13), (21, 22, 23), (31, 32, 33))
        >>> for col in A.columns():
        ...     print(col)
        ...
        <11, 12, 13>
        <21, 22, 23>
        <31, 32, 33>
        """
        for col in zip(*self._m):
            yield Vector(*col)
    
    def augment (self, *args):
        """Augment the matrix with some vectors or matrices.
        
        Examples
        --------
        >>> A = Matrix((1, 2), (3, 4))
        >>> A + identity(2)
        Matrix((2, 2), (3, 5))
        >>> A.augment(_)
        Matrix((1, 2, 2, 2), (3, 4, 3, 5))
        >>> A.augment(A.column(0))
        Matrix((1, 2, 1), (3, 4, 3))
        >>> A.augment(A.row(0))
        Matrix((1, 2, 1), (3, 4, 2))
        """
        cols = list(self.columns())
        for aug in args:
            try:
                cols.extend(aug.columns())
            except AttributeError:
                cols.append(aug)
        return Matrix(*cols, columns=True)
    
    def __getitem__ (self, idx):
        """Return a specific element.
        
        A subscript of an instance of Matrix should be given two comma
        separated indices. The first index will be the row and the
        second index will be the column.
        
        Example
        -------
        >>> A = Matrix((1, 2), (3, 4))
        >>> A[1, 0]
        3
        """
        return self.row(idx[0])[idx[1]]
    
    def __len__ (self):
        """Return the number of rows"""
        return self.height
    
    def __add__ (self, other):
        """Return the sum of two matrices.
        
        Will add together two matrices if they have the same number of
        rows and columns, or throw a ValueError exception if they do
        not.
        
        Examples
        --------
        >>> A = Matrix((1, 0), (0, 1))
        >>> B = Matrix((0, 2), (3, 3))
        >>> A + B
        Matrix((1, 2), (3, 4))
        
        >>> A = Matrix((1, 0, 0), (0, 1, 0), (0, 0, 1))
        >>> B = Matrix((1, 0), (0, 1))
        >>> A + B
        ValueError: Matrices must have the same dimensions.
        """
        if self.dimensions == other.dimensions:
            result = []
            for row in zip(self._m, other._m):
                result.append(sum(cell) for cell in zip(*row))
            return Matrix(*result)
        else:
            raise ValueError("Matrices must have the same dimensions.")
    
    def __radd__ (self, other):
        return self + other
    
    def __sub__ (self, other):
        return self + other * -1
    
    def __rsub__ (self, other):
        return self - other
    
    def _scale (self, scalar):
        "Scale a matrix."
        result = []
        for row in self.rows():
            result.append(scalar * cell for cell in row)
        return Matrix(*result)
    
    def _mul (self, other):
        "Multiply two matrices."
        result = []
        for row in self.rows():
            new_row = []
            for col in other.columns():
                new_row.append(dot_product(row, col))
            result.append(new_row)
        return Matrix(*result)
    
    def _vecmul (self, other):
        "Multiply a matrix by a vector"
        return Vector(*(dot_product(row, other) for row in self.rows()))
    
    def __mul__ (self, other):
        """Multiply the matrix by a scalar, a vector or another matrix.
        
        Will return a matrix when multiplied by another matrix or a
        scalar, but will return a vector if other is a vector.
        
        Examples
        --------
        >>> A = linalg.Matrix((11, 12, 13), (21, 22, 23), (31, 32, 33))
        >>> A * 3
        Matrix((33, 36, 39), (63, 66, 69), (93, 96, 99))
        >>> A * linalg.Vector(2, 4, 6)
        Matrix((148,), (268,), (388,))
        >>> A * A
        Matrix((776, 812, 848), (1406, 1472, 1538), (2036, 2132, 2228))
        """ 
        if isinstance(other, Number):
            return self._scale(other)
        elif isinstance(other, Matrix):
            return self._mul(other)
        elif isinstance(other, Vector):
            return self._vecmul(other)
        else:
            return NotImplemented
    
    def __rmul__ (self, other):
        """Multiply the matrix by a scalar."""
        if isinstance(other, Number):
            return self._scale(other)
        else:
            return NotImplemented
    
    def __pow__ (self, idx):
        
        if not (self.is_square or isinstance(idx, int)):
            return NotImplemented
        elif idx >= 0:
            result = identity(self.width)
            for x in range(idx):
                result *= self
            return result
        elif idx < 0:
            return NotImplemented
    
    def __str__ (self):
        """Return a text representation of the matrix
        
        It represents a matrix textually as a list of vectors. Each
        vector is one of the rows of the matrix.
        
        Example
        -------
        >>> A = Matrix((1, 2), (3, 4))
        >>> str(A)
        '(<1, 2>, <3, 4>)'
        """
        return ", ".join(str(row) for row in self.rows()).join("()")
    
    def __repr__ (self):
        """Return the string necessary to make the matrix.
        
        It will give the argument to init as a tuple of tuples.
        
        Examples
        --------
        >>> A = Matrix((1, 1, 2), (3, 5, 8), (13, 21, 34))
        >>> repr(A)
        'Matrix((1, 1, 2), (3, 5, 8), (13, 21, 34))'
        
        >>> B = Matrix([x + 1, x + 5, x + 7] for x in range(3))
        >>> repr(B)
        'Matrix((1, 5, 7), (2, 6, 8), (3, 7, 9))
        """
        return "Matrix{}".format(repr(self._m))
    
    def __eq__ (self, other):
        """Return whether two matrices are equal."""
        if type(self) == type(other):
            return self._m == other._m
        else:
            return False
    
    def __ne__ (self, other):
        """Return whether two matrices are not equal"""
        return not self == other

from .utils import leading_entry, dot_product, identity