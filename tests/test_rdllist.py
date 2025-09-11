import pytest

from physdes.rdllist import RDllist, RDllIterator


def test_rdllist_init():
    """
    Test initialization of RDllist.
    """
    dll = RDllist(5)
    assert len(dll.cycle) == 5
    for i in range(5):
        assert dll[i].data == i
        assert dll[i].next.data == (i + 1) % 5
        assert dll[i].prev.data == (i - 1 + 5) % 5


def test_rdllist_init_reverse():
    """
    Test initialization of RDllist with reverse=True.
    """
    dll = RDllist(5, reverse=True)
    assert len(dll.cycle) == 5
    for i in range(5):
        assert dll[i].data == i
        assert dll[i].next.data == (i - 1 + 5) % 5
        assert dll[i].prev.data == (i + 1) % 5


def test_rdllist_getitem():
    """
    Test __getitem__ of RDllist.
    """
    dll = RDllist(5)
    assert dll[0].data == 0
    assert dll[4].data == 4
    with pytest.raises(IndexError):
        _ = dll[5]


def test_rdllist_iter():
    """
    Test __iter__ of RDllist.
    """
    dll = RDllist(5)
    it = iter(dll)
    assert isinstance(it, RDllIterator)
    data = [node.data for node in it]
    assert data == [1, 2, 3, 4]


def test_rdllist_from_node():
    """
    Test from_node of RDllist.
    """
    dll = RDllist(5)
    it = dll.from_node(2)
    assert isinstance(it, RDllIterator)
    data = [node.data for node in it]
    assert data == [3, 4, 0, 1]
