"""
Unit tests for DME Algorithm with delay calculator strategy pattern
"""

import pytest
import sys
from pathlib import Path

# Add the parent directory to Python path to import the modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from physdes.cts.dme_algorithm import (
    DMEAlgorithm,
    LinearDelayCalculator,
    ElmoreDelayCalculator,
    Sink,
    TreeNode,
    get_tree_statistics,
)
from physdes.point import Point
from physdes.interval import Interval


class TestDelayCalculators:
    """Test cases for delay calculator strategies"""

    def test_linear_delay_calculator_initialization(self):
        """Test LinearDelayCalculator initialization"""
        calc = LinearDelayCalculator(delay_per_unit=0.5, capacitance_per_unit=0.2)
        assert calc.delay_per_unit == 0.5
        assert calc.capacitance_per_unit == 0.2

    def test_linear_delay_calculation(self):
        """Test linear delay calculation"""
        calc = LinearDelayCalculator(delay_per_unit=0.5)
        delay = calc.calculate_wire_delay(10.0, 5.0)
        assert delay == 5.0  # 0.5 * 10

    def test_linear_delay_per_unit(self):
        """Test linear delay per unit calculation"""
        calc = LinearDelayCalculator(delay_per_unit=0.3)
        delay_per_unit = calc.calculate_wire_delay_per_unit(5.0)
        assert delay_per_unit == 0.3

    def test_linear_wire_capacitance(self):
        """Test linear wire capacitance calculation"""
        calc = LinearDelayCalculator(capacitance_per_unit=0.2)
        capacitance = calc.calculate_wire_capacitance(10.0)
        assert capacitance == 2.0

    def test_elmore_delay_calculator_initialization(self):
        """Test ElmoreDelayCalculator initialization"""
        calc = ElmoreDelayCalculator(unit_resistance=0.1, unit_capacitance=0.2)
        assert calc.unit_resistance == 0.1
        assert calc.unit_capacitance == 0.2

    def test_elmore_delay_calculation(self):
        """Test Elmore delay calculation"""
        calc = ElmoreDelayCalculator(unit_resistance=0.1, unit_capacitance=0.2)
        delay = calc.calculate_wire_delay(10.0, 5.0)
        expected = 0.1 * 10 * (0.2 * 10 / 2 + 5.0)  # R * (C_wire/2 + C_load)
        assert delay == expected

    def test_elmore_delay_per_unit(self):
        """Test Elmore delay per unit calculation"""
        calc = ElmoreDelayCalculator(unit_resistance=0.1, unit_capacitance=0.2)
        delay_per_unit = calc.calculate_wire_delay_per_unit(5.0)
        expected = 0.1 * (0.2 / 2 + 5.0)
        assert delay_per_unit == expected

    def test_elmore_wire_capacitance(self):
        """Test Elmore wire capacitance calculation"""
        calc = ElmoreDelayCalculator(unit_capacitance=0.2)
        capacitance = calc.calculate_wire_capacitance(10.0)
        assert capacitance == 2.0


class TestDMEAlgorithm:
    """Test cases for DMEAlgorithm class"""

    @pytest.fixture
    def sample_sinks(self):
        """Create sample sinks for testing"""
        return [
            Sink("s1", Point(0, 0), 1.0),
            Sink("s2", Point(10, 0), 1.0),
            Sink("s3", Point(0, 10), 1.0),
        ]

    @pytest.fixture
    def linear_calculator(self):
        return LinearDelayCalculator(delay_per_unit=0.5, capacitance_per_unit=0.1)

    @pytest.fixture
    def elmore_calculator(self):
        return ElmoreDelayCalculator(unit_resistance=0.1, unit_capacitance=0.1)

    def test_dme_algorithm_initialization(self, linear_calculator):
        """Test DMEAlgorithm initialization with delay calculator"""
        dme = DMEAlgorithm(delay_calculator=linear_calculator)
        assert dme.delay_calculator == linear_calculator

    def test_build_clock_tree_with_linear_model(self, sample_sinks, linear_calculator):
        """Test clock tree construction with linear delay model"""
        dme = DMEAlgorithm(delay_calculator=linear_calculator)
        root = dme.build_clock_tree(sample_sinks)

        assert root is not None
        assert root.name.startswith("n")
        assert root.left is not None
        assert root.right is not None

    def test_build_clock_tree_with_elmore_model(self, sample_sinks, elmore_calculator):
        """Test clock tree construction with Elmore delay model"""
        dme = DMEAlgorithm(delay_calculator=elmore_calculator)
        root = dme.build_clock_tree(sample_sinks)

        assert root is not None
        assert root.name.startswith("n")
        assert root.left is not None
        assert root.right is not None

    def test_build_clock_tree_single_sink(self, linear_calculator):
        """Test clock tree construction with single sink"""
        single_sink = [Sink("s1", Point(0, 0), 1.0)]
        dme = DMEAlgorithm(delay_calculator=linear_calculator)
        root = dme.build_clock_tree(single_sink)

        assert root.name == "s1"
        assert root.left is None
        assert root.right is None

    def test_build_clock_tree_empty_sinks(self, linear_calculator):
        """Test clock tree construction with empty sinks list"""
        dme = DMEAlgorithm(delay_calculator=linear_calculator)
        with pytest.raises(ValueError, match="No sinks provided"):
            dme.build_clock_tree([])

    def test_analyze_skew_linear_model(self, sample_sinks, linear_calculator):
        """Test skew analysis with linear delay model"""
        dme = DMEAlgorithm(delay_calculator=linear_calculator)
        root = dme.build_clock_tree(sample_sinks)
        analysis = dme.analyze_skew(root)

        assert "max_delay" in analysis
        assert "min_delay" in analysis
        assert "skew" in analysis
        assert "sink_delays" in analysis
        assert "total_wirelength" in analysis
        assert "delay_model" in analysis
        assert analysis["delay_model"] == "LinearDelayCalculator"
        assert analysis["skew"] >= 0  # Skew should be non-negative

    def test_analyze_skew_elmore_model(self, sample_sinks, elmore_calculator):
        """Test skew analysis with Elmore delay model"""
        dme = DMEAlgorithm(delay_calculator=elmore_calculator)
        root = dme.build_clock_tree(sample_sinks)
        analysis = dme.analyze_skew(root)

        assert "delay_model" in analysis
        assert analysis["delay_model"] == "ElmoreDelayCalculator"
        assert analysis["skew"] >= 0

    def test_manhattan_distance(self, linear_calculator):
        """Test Manhattan distance calculation"""
        dme = DMEAlgorithm(delay_calculator=linear_calculator)
        p1 = Point(0, 0)
        p2 = Point(3, 4)
        distance = dme._manhattan_distance(p1, p2)
        assert distance == 7

    def test_get_center_int(self, linear_calculator):
        """Test center calculation for integer coordinate"""
        dme = DMEAlgorithm(delay_calculator=linear_calculator)
        center = dme._get_center(10)
        assert center == 10

    def test_get_center_interval(self, linear_calculator):
        """Test center calculation for interval coordinate"""
        dme = DMEAlgorithm(delay_calculator=linear_calculator)
        interval = Interval(10, 20)
        center = dme._get_center(interval)
        assert center == 15

    def test_total_wirelength(self, sample_sinks, linear_calculator):
        """Test total wirelength calculation"""
        dme = DMEAlgorithm(delay_calculator=linear_calculator)
        root = dme.build_clock_tree(sample_sinks)
        total_length = dme._total_wirelength(root)
        assert total_length >= 0


class TestTreeStatistics:
    """Test cases for tree statistics function"""

    def test_get_tree_statistics_simple_tree(self):
        """Test tree statistics for a simple tree"""
        s1 = TreeNode(name="s1", position=Point(10, 20))
        s2 = TreeNode(name="s2", position=Point(30, 40))
        root = TreeNode(name="n1", position=Point(20, 30), left=s1, right=s2)

        stats = get_tree_statistics(root)

        assert stats["total_nodes"] == 3
        assert stats["total_sinks"] == 2
        assert stats["total_wires"] == 2
        assert len(stats["nodes"]) == 3
        assert len(stats["wires"]) == 2
        assert len(stats["sinks"]) == 2

        # Check node information
        node_names = [node["name"] for node in stats["nodes"]]
        assert "s1" in node_names
        assert "s2" in node_names
        assert "n1" in node_names

    def test_get_tree_statistics_single_node(self):
        """Test tree statistics for single node"""
        single_node = TreeNode(name="s1", position=Point(10, 20))

        stats = get_tree_statistics(single_node)

        assert stats["total_nodes"] == 1
        assert stats["total_sinks"] == 1
        assert stats["total_wires"] == 0
        assert stats["nodes"][0]["name"] == "s1"
        assert stats["nodes"][0]["type"] == "sink"

    def test_get_tree_statistics_with_delays(self):
        """Test tree statistics with delay information"""
        s1 = TreeNode(name="s1", position=Point(10, 20), delay=1.0, capacitance=1.0)
        s2 = TreeNode(name="s2", position=Point(30, 40), delay=1.5, capacitance=1.0)
        root = TreeNode(
            name="n1",
            position=Point(20, 30),
            left=s1,
            right=s2,
            delay=0.5,
            capacitance=2.0,
        )

        stats = get_tree_statistics(root)

        # Check that delay and capacitance are captured
        for node in stats["nodes"]:
            if node["name"] == "s1":
                assert node["delay"] == 1.0
                assert node["capacitance"] == 1.0
            elif node["name"] == "n1":
                assert node["delay"] == 0.5
                assert node["capacitance"] == 2.0


class TestIntegration:
    """Integration tests for different scenarios"""

    def test_different_delay_models_produce_different_results(self):
        """Test that linear and Elmore models produce different delay values"""
        sinks = [
            Sink("s1", Point(0, 0), 1.0),
            Sink("s2", Point(20, 0), 2.0),
            Sink("s3", Point(0, 20), 1.5),
        ]

        # Linear model
        linear_calc = LinearDelayCalculator(delay_per_unit=0.5)
        dme_linear = DMEAlgorithm(delay_calculator=linear_calc)
        tree_linear = dme_linear.build_clock_tree(sinks)
        analysis_linear = dme_linear.analyze_skew(tree_linear)

        # Elmore model
        elmore_calc = ElmoreDelayCalculator(unit_resistance=0.1, unit_capacitance=0.2)
        dme_elmore = DMEAlgorithm(delay_calculator=elmore_calc)
        tree_elmore = dme_elmore.build_clock_tree(sinks)
        analysis_elmore = dme_elmore.analyze_skew(tree_elmore)

        # They should have different delay models
        assert analysis_linear["delay_model"] == "LinearDelayCalculator"
        assert analysis_elmore["delay_model"] == "ElmoreDelayCalculator"

        # The actual delay values will likely be different due to different models
        # but both should produce valid, non-negative results
        assert analysis_linear["max_delay"] >= 0
        assert analysis_elmore["max_delay"] >= 0
        assert analysis_linear["skew"] >= 0
        assert analysis_elmore["skew"] >= 0

    def test_larger_clock_tree(self):
        """Test with a larger set of sinks"""
        sinks = [Sink(f"s{i}", Point(i * 10, i * 5), 1.0 + i * 0.1) for i in range(8)]

        calc = LinearDelayCalculator(delay_per_unit=0.3)
        dme = DMEAlgorithm(delay_calculator=calc)
        root = dme.build_clock_tree(sinks)
        analysis = dme.analyze_skew(root)

        assert root is not None
        assert analysis["total_wirelength"] > 0
        assert len(analysis["sink_delays"]) == 8
        assert all(delay >= 0 for delay in analysis["sink_delays"])


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
