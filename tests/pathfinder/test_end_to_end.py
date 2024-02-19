"""Tests the end-to-end performance of the pathfinder module."""

from __future__ import annotations

import pytest

import mqt.qubomaker as qm
import mqt.qubomaker.pathfinder as pf
import mqt.qubomaker.pathfinder.cost_functions as cf

from .utils_test import get_test_graph_small, paths_equal_with_loops, paths_to_assignment_list

TEST_GRAPH = get_test_graph_small()


@pytest.mark.parametrize(
    ("encoding_type"),
    [
        (cf.EncodingType.ONE_HOT),
        (cf.EncodingType.UNARY),
        (cf.EncodingType.BINARY),
    ],
)
class TestEndToEnd:
    """Tests the end-to-end performance of the `pathfinder` module."""

    def test_tsp(self, encoding_type: pf.EncodingType) -> None:
        """Test the module with a TSP problem.

        Args:
            encoding_type (pf.EncodingType): The encoding type to use.
        """
        settings = pf.PathFindingQUBOGeneratorSettings(
            encoding_type=encoding_type,
            n_paths=1,
            max_path_length=4,
            loops=True,
        )
        generator = pf.PathFindingQUBOGenerator(
            objective_function=cf.MinimizePathLength([1]),
            graph=TEST_GRAPH,
            settings=settings,
        )
        generator.add_constraint(cf.PathIsValid([1]))
        generator.add_constraint(cf.PathContainsVerticesExactlyOnce(TEST_GRAPH.all_vertices, [1]))

        if encoding_type != cf.EncodingType.BINARY:
            # Binary encoding is too complex for evaluation in this test.
            qubo_matrix = generator.construct_qubo_matrix()
            optimal_solution, _ = qm.optimize_classically(qubo_matrix)

            path_representation = generator.decode_bit_array(optimal_solution)

            assert paths_equal_with_loops(path_representation[0], [4, 1, 2, 3])
            assert generator.get_cost(optimal_solution) == 20

        solution = paths_to_assignment_list([[4, 1, 2, 3]], 4, 4, encoding_type)
        assert generator.get_cost(solution) == 20

    def test_2dpp(self, encoding_type: pf.EncodingType) -> None:
        """Test the module with a 2DPP problem.

        Args:
            encoding_type (pf.EncodingType): The encoding type to use.
        """

        settings = pf.PathFindingQUBOGeneratorSettings(
            encoding_type=encoding_type,
            n_paths=2,
            max_path_length=2,
            loops=False,
        )
        generator = pf.PathFindingQUBOGenerator(
            objective_function=cf.MinimizePathLength([1, 2]),
            graph=TEST_GRAPH,
            settings=settings,
        )
        generator.add_constraint(cf.PathIsValid([1, 2]))
        generator.add_constraint(cf.PathsShareNoVertices(1, 2))
        generator.add_constraint(cf.PathStartsAt([1], 1))
        generator.add_constraint(cf.PathStartsAt([2], 2))
        generator.add_constraint(cf.PathEndsAt([3], 1))
        generator.add_constraint(cf.PathEndsAt([4], 2))

        solution = paths_to_assignment_list([[1, 3], [2, 4]], 4, 2, encoding_type)
        assert generator.get_cost(solution) == 9


def setup_tsp() -> pf.PathFindingQUBOGenerator:
    """Set up a `PathFindingQUBOGenerator` for a TSP problem."""
    settings = pf.PathFindingQUBOGeneratorSettings(
        encoding_type=pf.EncodingType.ONE_HOT,
        n_paths=1,
        max_path_length=4,
        loops=True,
    )
    generator = pf.PathFindingQUBOGenerator(
        objective_function=cf.MinimizePathLength([1]),
        graph=TEST_GRAPH,
        settings=settings,
    )
    generator.add_constraint(cf.PathIsValid([1]))
    generator.add_constraint(cf.PathContainsVerticesExactlyOnce(TEST_GRAPH.all_vertices, [1]))
    return generator


def test_fail_get_cost_variable_count() -> None:
    """Tests whether passing an incorrect number of variables to `get_cost()` fails."""
    generator = setup_tsp()
    with pytest.raises(ValueError, match="Invalid assignment length"):
        generator.get_cost([1, 0])


def test_fail_get_cost_variable_values() -> None:
    """Tests whether passing non-binary variables to `get_cost()` fails."""
    generator = setup_tsp()
    with pytest.raises(ValueError, match="Provided values are not binary \\(1/0\\)"):
        generator.get_cost([2, 0])

    with pytest.raises(ValueError, match="Provided values are not binary \\(1/0\\)"):
        generator.get_cost([-1, 0])
