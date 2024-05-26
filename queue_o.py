"""Queue class."""


class SimulationQueue():
    """Queue class."""

    def __init__(self):
        """Initialize queue."""
        self._items = []

    def is_empty(self):
        """Check if queue is empty."""
        return self._items == []

    def enqueue(self, item):
        """Add item to queue."""
        self._items.append(item)

    def dequeue(self):
        """Remove item from queue."""
        return self._items.pop(0)

    def size(self):
        """Return size of queue."""
        return len(self._items)