import ctypes


# Implements the Array ADT using array capabilities of the ctypes module.

class Array:
    # Creates an array with size elements.
    def __init__(self, size):
        assert size > 0, "Array size must be > 0"
        self._size = size
        # Create the array structure using the ctypes module.
        PyArrayType = ctypes.py_object * size
        self._elements = PyArrayType()
        # Initialize each element.
        self.clear(None)

    # Returns the size of the array.
    def __len__(self):
        return self._size

    # Gets the contents of the index element.
    def __getitem__(self, index):
        assert index >= 0 and index < len(self), "Array subscript out of range"
        return self._elements[index]

    # Puts the value in the array element at index position.
    def __setitem__(self, index, value):
        assert index >= 0 and index < len(self), "Array subscript out of range"
        self._elements[index] = value

    # Clears the array by setting each element to the given value.
    def clear(self, value):
        for i in range(len(self)):
            self._elements[i] = value

    # Returns the array's iterator for traversing the elements.
    def __iter__(self):
        return _ArrayIterator(self._elements)


# An iterator for the Array ADT.
class _ArrayIterator:
    def __init__(self, the_array):
        self._array_ref = the_array
        self._cur_index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._cur_index < len(self._array_ref):
            entry = self._array_ref[self._cur_index]
            self._cur_index += 1
            return entry
        else:
            raise StopIteration


# Implementation of the Array2D ADT using an array of arrays.

class Array2D:
    # Creates a 2 -D array of size numRows x numCols.
    def __init__(self, num_rows, num_cols):
        # Create a 1 -D array to store an array reference for each row.
        self.rows = Array(num_rows)

        # Create the 1 -D arrays for each row of the 2 -D array.
        for i in range(num_rows):
            self.rows[i] = Array(num_cols)

    # Returns the number of rows in the 2 -D array.
    def num_rows(self):
        return len(self.rows)

    # Returns the number of columns in the 2 -D array.
    def num_cols(self):
        return len(self.rows[0])

    # Clears the array by setting every element to the given value.
    def clear(self, value):
        for row in self.rows:
            row.clear(value)

    # Gets the contents of the element at position [i, j]
    def __getitem__(self, index_tuple):
        assert len(index_tuple) == 2, "Invalid number of array subscripts."
        row = index_tuple[0]
        col = index_tuple[1]
        assert row >= 0 and row < self.num_rows() \
               and col >= 0 and col < self.num_cols(), \
            "Array subscript out of range."
        array_1d = self.rows[row]
        return array_1d[col]

    # Sets the contents of the element at position [i,j] to value.
    def __setitem__(self, index_tuple, value):
        assert len(index_tuple) == 2, "Invalid number of array subscripts."
        row = index_tuple[0]
        col = index_tuple[1]
        assert row >= 0 and row < self.num_rows() \
               and col >= 0 and col < self.num_cols(), \
            "Array subscript out of range."
        array_1d = self.rows[row]
        array_1d[col] = value


class DynamicArray:
    """A dynamic array class akin to a simplified Python list."""

    def __init__(self):
        """Create an empty array."""
        self._n = 0  # count actual elements
        self._capacity = 1  # default array capacity
        self._A = self._make_array(self._capacity)  # low-level array

    def __len__(self):
        """Return number of elements stored in the array."""
        return self._n

    def __getitem__(self, k):
        """Return element at index k."""
        if not 0 <= k < self._n:
            raise IndexError('invalid index')
        return self._A[k]  # retrieve from array

    def append(self, obj):
        """Add object to end of the array."""
        if self._n == self._capacity:  # not enough room
            self._resize(2 * self._capacity)  # so double capacity
        self._A[self._n] = obj
        self._n += 1

    def _resize(self, c):  # nonpublic utitity
        """Resize internal array to capacity c."""
        B = self._make_array(c)  # new (bigger) array
        for k in range(self._n):  # for each existing value
            B[k] = self._A[k]
        self._A = B  # use the bigger array
        self._capacity = c

    def _make_array(self, c):  # nonpublic utitity
        """Return new array with capacity c."""
        return (c * ctypes.py_object)()  # see ctypes documentation

    def insert(self, k, value):
        """Insert value at index k, shifting subsequent values rightward."""
        # (for simplicity, we assume 0 <= k <= n in this verion)
        if self._n == self._capacity:  # not enough room
            self._resize(2 * self._capacity)  # so double capacity
        for j in range(self._n, k, -1):  # shift rightmost first
            self._A[j] = self._A[j - 1]
        self._A[k] = value  # store newest element
        self._n += 1

    def remove(self, value):
        """Remove first occurrence of value( or  raise ValueError)."""
        # note: we do not consider shrinking the dynamic array in this version
        for k in range(self._n):
            if self._A[k] == value:  # found a match!
                for j in range(k, self._n - 1):  # shift others to fill gap
                    self._A[j] = self._A[j + 1]
                self._A[self._n - 1] = None  # help garbage collection
                self._n -= 1  # we have one less item

                return  # exit immediately
        raise ValueError("value not found")  # only reached if no match


class Stack:
    # Creates an empty stack.
    def __init__(self):
        self._top = None
        self._size = 0

    # Returns True if the stack is empty or False otherwise.
    def is_empty(self):
        return self._top is None

    # Returns the number of items in the stack.
    def __len__(self):
        return self._size

    # Returns the top item on the stack without removing it.
    def peek(self):
        assert not self.is_empty(), "Cannot peek at an empty stack"
        return self._top.item

    # Removes and returns the top item on the stack.
    def pop(self):
        assert not self.is_empty(), "Cannot pop from an empty stack"
        node = self._top
        self._top = self._top.next
        self._size -= 1
        return node.item

    # Pushes an item onto the top of the stack.
    def push(self, item):
        self._top = _StackNode(item, self._top)
        self._size += 1


# The private storage class for creating stack nodes.
class _StackNode:
    def __init__(self, item, link):
        self.item = item
        self.next = link


class AbstractCollection:
    """An abstract collection implementation."""

    # Constructor
    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._size = 0
        if sourceCollection:
            for item in sourceCollection:
                self.add(item)

    def add(self, item):
        raise NotImplementedError

    def push(self, item):
        raise NotImplementedError

    def __iter__(self):
        raise NotImplementedError

    # Accessor methods
    def isEmpty(self):
        """Returns True if len(self) == 0, or False otherwise."""
        return len(self) == 0

    def __len__(self):
        """Returns the number of items in self."""
        return self._size

    def __str__(self):
        """Returns the string representation of self."""
        return "[" + ", ".join(map(str, self)) + "]"

    def __add__(self, other):
        """Returns a new bag containing the contents
        of self and other."""
        result = type(self)(self)
        for item in other:
            result.add(item)
        return result

    def __eq__(self, other):
        """Returns True if self equals other,
        or False otherwise."""
        if self is other: return True
        if type(self) != type(other) or \
                len(self) != len(other):
            return False
        otherIter = iter(other)
        for item in self:
            if item != next(otherIter):
                return False
        return True


class AbstractStack(AbstractCollection):
    """An abstract stack implementation."""

    # Constructor
    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        AbstractCollection.__init__(self, sourceCollection)

    # Mutator methods
    def add(self, item):
        """Adds item to self."""
        self.push(item)


class Node:
    """Represents a singly linked node."""

    def __init__(self, data, next=None):
        self.data = data
        self.next = next


class LinkedStack(AbstractStack):
    """A link-based stack implementation."""

    # Constructor
    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._items = None
        AbstractStack.__init__(self, sourceCollection)

    # Accessor methods
    def __iter__(self):
        """Supports iteration over a view of self.
        Visits items from bottom to top of stack."""

        def visitNodes(node):
            """Adds items to tempList from tail to head."""
            if not node is None:
                visitNodes(node.next)
                tempList.append(node.data)

        tempList = list()
        visitNodes(self._items)
        return iter(tempList)

    def peek(self):
        """
        Returns the item at the top of the stack.
        Precondition: the stack is not empty.
        Raises: KeyError if the stack is empty."""
        if self.isEmpty():
            raise KeyError("The stack is empty.")
        return self._items.data

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._size = 0
        self._items = None

    def push(self, item):
        """Adds item to the top of the stack."""
        self._items = Node(item, self._items)
        self._size += 1

    def pop(self):
        """
        Removes and returns the item at the top of the stack.
        Precondition: the stack is not empty.
        Raises: KeyError if the stack is empty.
        Post condition: the top item is removed from the stack."""
        if self.isEmpty():
            raise KeyError("The stack is empty.")
        oldItem = self._items.data
        self._items = self._items.next
        self._size -= 1
        return oldItem


class LinkedQueue(AbstractCollection):
    """A link-based queue implementation."""

    # Constructor
    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._front = self._rear = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __iter__(self):
        """Supports iteration over a view of self."""
        cursor = self._front
        while not cursor is None:
            yield cursor.data
            cursor = cursor.next

    def peek(self):
        """
        Returns the item at the front of the queue.
        Precondition: the queue is not empty.
        Raises: KeyError if the stack is empty."""
        if self.isEmpty():
            raise KeyError("The queue is empty.")
        return self._front.data

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._size = 0
        self._front = self._rear = None

    def add(self, item):
        """Adds item to the rear of the queue."""
        newNode = Node(item, None)
        if self.isEmpty():
            self._front = newNode
        else:
            self._rear.next = newNode
        self._rear = newNode
        self._size += 1

    def pop(self):
        """
        Removes and returns the item at the front of the queue.
        Precondition: the queue is not empty.
        Raises: KeyError if the queue is empty.
        Post condition: the front item is removed from the queue."""
        if self.isEmpty():
            raise KeyError("The queue is empty.")
        oldItem = self._front.data
        self._front = self._front.next
        if self._front is None:
            self._rear = None
        self._size -= 1
        return oldItem

    def remove(self, index):
        """Removes and returns the item at index,
        where index ranges from 0 (the front) to size - 1 (the rear).
        Precondition: 0 <= index < size of queue"""
        if index < 0 or index >= len(self):
            raise AttributeError("i must be >= 0 and < size of queue")
        if index == 0:
            oldItem = self._front.data
            self._front = self._front.next
        else:
            probe = self._front
            while index > 1:
                probe = probe.next
                index -= 1
            oldItem = probe.next.data
            probe.next = probe.next.next
        self._size -= 1
        if self.isEmpty():
            self._rear = None
        return oldItem

class BSTNode:
    """Represents a node for a linked binary search tree."""

    def __init__(self, data, left = None, right = None):
        self.data = data
        self.left = left
        self.right = right