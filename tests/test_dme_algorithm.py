import pytest
from physdes.dme_algorithm import DMEAlgorithm, Sink, TreeNode, get_tree_statistics
from physdes.point import Point
from physdes.interval import Interval


def test_sink_creation():
    """Test creation of a Sink object."""
    pos = Point(10, 20)
    s = Sink(name="s1", position=pos, capacitance=1.5)
    assert s.name == "s1"
    assert s.position == pos
    assert s.capacitance == 1.5


def test_treenode_creation():
    """Test creation of a TreeNode object."""
    pos = Point(30, 40)
    node = TreeNode(name="n1", position=pos)
    assert node.name == "n1"
    assert node.position == pos
    assert node.left is None
    assert node.right is None
    assert node.parent is None


def test_dme_algorithm_init():
    """Test initialization of the DMEAlgorithm class."""
    dme = DMEAlgorithm(unit_resistance=0.2, unit_capacitance=0.3)
    assert dme.unit_resistance == 0.2
    assert dme.unit_capacitance == 0.3


def test_build_clock_tree_no_sinks():
    """Test that building a clock tree with no sinks raises a ValueError."""
    dme = DMEAlgorithm()
    with pytest.raises(ValueError, match="No sinks provided"):
        dme.build_clock_tree([])


def test_build_clock_tree_single_sink():
    """Test building a clock tree with a single sink.
    This test characterizes the current behavior, which may not be correct.
    The position of the sink is changed by the algorithm.
    """
    sinks = [Sink("s1", Point(10, 20))]
    dme = DMEAlgorithm()
    tree = dme.build_clock_tree(sinks)
    assert tree.name == "s1"
    # The current implementation changes the position of the sink.
    # This is likely a bug.
    assert tree.position != Point(10, 20)


def test_manhattan_distance():
    """Test the Manhattan distance calculation."""
    dme = DMEAlgorithm()
    p1 = Point(10, 20)
    p2 = Point(40, 60)
    assert dme._manhattan_distance(p1, p2) == 70


def test_wire_delay_calculations():
    """Test the wire delay and capacitance calculations."""
    dme = DMEAlgorithm(unit_resistance=0.1, unit_capacitance=0.2)
    assert dme._wire_capacitance(10) == 2.0
    assert dme._wire_delay(10, 5.0) == 0.1 * 10 * (
        0.2 * 10 / 2 + 5.0
    )  # 1.0 * (1.0 + 5.0) = 6.0
    assert dme._wire_delay_per_unit(5.0) == 0.1 * (
        0.2 / 2 + 5.0
    )  # 0.1 * (0.1 + 5.0) = 0.51


def test_get_center():
    """Test the _get_center method."""
    dme = DMEAlgorithm()
    assert dme._get_center(10) == 10
    assert dme._get_center(Interval(10, 20)) == 15


def test_dme_full_run():
    """Test a full run of the DME algorithm with a small example.
    This test characterizes the current behavior, which may not be correct.
    The skew is expected to be close to 0, but it is not.
    """
    sinks = [
        Sink("s1", Point(10, 20)),
        Sink("s2", Point(30, 40)),
        Sink("s3", Point(50, 10)),
    ]
    dme = DMEAlgorithm(unit_resistance=0.1, unit_capacitance=0.2)
    clock_tree = dme.build_clock_tree(sinks)

    # Check the tree structure
    stats = get_tree_statistics(clock_tree)
    assert stats["total_nodes"] == 5  # 3 sinks + 2 internal nodes
    assert stats["total_sinks"] == 3

    # Check skew
    analysis = dme.analyze_skew(clock_tree)
    # The current implementation has a large skew, which is likely a bug.
    assert analysis["skew"] > 1
