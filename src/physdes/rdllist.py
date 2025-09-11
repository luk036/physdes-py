from typing import List, TypeVar

from mywheel.dllist import Dllink

T = TypeVar("T")


class RDllIterator:
    """The `RobinIterator` class is an iterator that iterates over a singly linked list starting from a
    given node.
    """

    __slots__ = ("cur", "stop")
    cur: Dllink[int]
    stop: Dllink[int]

    def __init__(self, node: Dllink[int]) -> None:
        """
        The function initializes the current and stop pointers to the given node.

        :param node: The `node` parameter is an instance of the `SlNode` class. It represents a node in a singly linked list
        :type node: Dllink[int]
        """
        self.cur = self.stop = node

    def __iter__(self) -> "RDllIterator":
        """
        The function returns an instance of the RobinIterator class.

        :return: The `__iter__` method is returning an instance of the `RobinIterator` class.
        """
        return self

    def next(self) -> Dllink[int]:
        """
        The `next` function returns the next element in a linked list and raises a `StopIteration` exception
        if there are no more elements.

        :return: The method is returning an integer value.
        """
        self.cur = self.cur.next
        if self.cur != self.stop:
            return self.cur
        else:
            raise StopIteration()

    def __next__(self):
        """
        The __next__ function returns the next item in the iterator.

        :return: The `next()` method is being called and its return value is being returned.
        """
        return self.next()


class RDllist:
    """Round-Robin Doubly Linked List implementation"""

    __slots__ = "cycle"
    cycle: List[Dllink[int]]

    def __init__(self, num_nodes: int, reverse: bool = False) -> None:
        """
        Initialize a Round-Robin doubly linked list.
        The head node contains no data and serves as a sentinel.

        :param num_nodes: The `num_nodes` parameter is an integer that represents the number of parts in the cycle
        :type num_nodes: int
        """
        self.cycle = list(Dllink(k) for k in range(num_nodes))
        dl2 = self.cycle[-1]
        if not reverse:
            for dl1 in self.cycle:
                dl2.next = dl1
                dl1.prev = dl2
                dl2 = dl1
        else:
            for dl1 in self.cycle:
                dl2.prev = dl1
                dl1.next = dl2
                dl2 = dl1

    def __getitem__(self, k: int) -> Dllink[int]:
        return self.cycle[k]

    def from_node(self, k: int) -> RDllIterator:
        return RDllIterator(self.cycle[k])

    def __iter__(self) -> RDllIterator:
        """
        The `__iter__` function returns an iterator object for a doubly linked list.
        """
        return self.from_node(0)


# Example usage and tests
if __name__ == "__main__":
    # Create a new Round-Robin doubly linked list
    cdll = RDllist(10)

    for vlink in cdll.from_node(3):
        print(vlink.data)

    print("---------")

    print(cdll[4].data)
