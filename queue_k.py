"""Queue class."""


class SimulationQueue_M_M_1_K():
    """Queue class."""

    def __init__(self,k):
        """Initialize queue."""
        self._items = []
        self._limit = k


    def is_empty(self):
        """Check if queue is empty."""
        return self._items == []
    def is_full(self):
        """Check if queue is full."""
        return len(self._items) == self._limit

    def enqueue(self, item):
        """Add item to queue."""
        self._items.append(item)

    def dequeue(self):
        """Remove item from queue."""
        return self._items.pop(0)

    def size(self):
        """Return size of queue."""
        return len(self._items)
