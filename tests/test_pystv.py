#!/usr/bin/env python

"""Tests for `pystv` package."""

from click.testing import CliRunner
from numpy.testing import assert_equal

import pystv
from pystv import cli


def test_2cands_1seat():
    ballots = [
        [2, 1],
        [2, 1],
        [1, 2],
    ]
    results = pystv.run_stv(ballots, num_seats=1)
    assert_equal(results[0], [False, True])
    assert_equal(results[1], [0, 1, 2])


def test_2cands_1seat_undervote():
    ballots = [
        [2, 0],
        [2, 1],
        [1, 2],
    ]
    results = pystv.run_stv(ballots, num_seats=1)
    assert_equal(results[0], [False, True])
    assert_equal(results[1], [0, 1, 2])


def test_3cands_2seats():
    ballots = [
        [2, 1, 3],
        [2, 1, 3],
        [1, 2, 3],
    ]
    results = pystv.run_stv(ballots, num_seats=2)
    assert_equal(results[0], [True, True, False])
    assert_equal(results[1], [0, 1, 2, 0])


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert "pystv.cli.main" in result.output
    help_result = runner.invoke(cli.main, ["--help"])
    assert help_result.exit_code == 0
    assert "--help  Show this message and exit." in help_result.output
