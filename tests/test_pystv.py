"""Tests for `pystv` package."""
import numpy as np
import pytest
from click.testing import CliRunner
from numpy.testing import assert_equal

import pystv
from pystv import cli

RR = pystv.RoundResult


def test_2cands_1seat():
    ballots = [
        [2, 1],
        [2, 1],
        [1, 2],
    ]
    results = pystv.run_stv(ballots, num_seats=1)

    assert len(results) == 1
    assert results[0] == RR([0, 1, 2], [2], None)


def test_2cands_1seat_undervote():
    ballots = [
        [2, 0],
        [2, 1],
        [1, 2],
    ]
    results = pystv.run_stv(ballots, num_seats=1)

    assert len(results) == 1
    assert results[0] == RR([0, 1, 2], [2], None)


def test_3cands_2seats_1round():
    ballots = [
        [2, 1, 3],
        [2, 1, 3],
        [2, 1, 3],
        [1, 2, 3],
        [1, 2, 3],
    ]
    results = pystv.run_stv(ballots, num_seats=2)

    assert len(results) == 1
    assert results[0] == RR([0, 2, 3, 0], [1, 2], None)


def test_3cands_1seat_multiround():
    ballots = [
        [1, 2, 3],
        [1, 2, 3],
        [2, 1, 3],
        [2, 1, 3],
        [3, 1, 2],
    ]
    results = pystv.run_stv(ballots, num_seats=1)

    assert len(results) == 2
    assert results[0] == RR([0, 2, 2, 1], [], 3)
    assert results[1] == RR([0, 3, 2, 0], [1], None)


def test_3cands_2seats_multiround():
    ballots = [
        [1, 3, 2],
        [1, 3, 2],
        [2, 1, 3],
        [2, 1, 3],
        [2, 1, 3],
        [2, 1, 3],
        [3, 1, 2],
        [3, 2, 1],
        [3, 2, 1],
    ]
    results = pystv.run_stv(ballots, num_seats=2)
    assert len(results) == 2
    assert results[0] == RR([0, 2, 4, 3], [2], 1)
    assert results[1] == RR([0, 0, 4, 5], [2, 3], None)


def test_3cands_2seats_multiround_with_adjust():
    ballots = [
        [1, 3, 2],
        [1, 3, 2],
        [2, 1, 3],
        [2, 1, 3],
        [2, 1, 3],
        [2, 1, 3],
        [2, 1, 3],
        [3, 1, 2],
        [3, 2, 1],
        [3, 2, 1],
    ]
    results = pystv.run_stv(ballots, num_seats=2)
    assert len(results) == 2
    assert results[0] == RR([0, 2, 5, 3], [2], 1)
    assert results[1] == RR([0, 0, 5, 5], [2, 3], None)


def test_validate_and_standardize_ballots_ok():
    ballots = [
        [1, 0, 0],
        [1, 2, 0],
        [1, 2, 3],
    ]
    pystv.validate_and_standardize_ballots(ballots)


def test_validate_and_standardize_ballots_negative():
    ballots = [[1, 0, 0], [1, 2, -1], [1, 2, 3]]
    with pytest.raises(ValueError, match=r"Negative rankings on ballots: \[1\]"):
        pystv.validate_and_standardize_ballots(ballots)


@pytest.mark.filterwarnings("ignore", category=np.VisibleDeprecationWarning)
def test_validate_and_standardize_ballots_ragged():
    ballots = [[1, 0, 0], [1, 2], [1, 2, 3]]
    with pytest.raises(ValueError, match=r"Ballot data has wrong dim"):
        pystv.validate_and_standardize_ballots(ballots)


def test_validate_and_standardize_ballots_invalid_ranking():
    ballots = [[1, 0, 0], [0, 1, 0], [1, 2, 0], [0, 0, 1]]
    with pytest.raises(ValueError, match=r"Skipped rankings on ballots: \[1, 3\]"):
        pystv.validate_and_standardize_ballots(ballots)


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert "pystv.cli.main" in result.output
    help_result = runner.invoke(cli.main, ["--help"])
    assert help_result.exit_code == 0
    assert "--help  Show this message and exit." in help_result.output
