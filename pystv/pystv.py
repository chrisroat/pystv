"""Minimalist implementation of Single Transferable Vote."""

import numpy as np


def run_stv(ballots, num_seats):
    ballots = validate_and_standardize_ballots(ballots)

    weights = np.zeros(ballots.shape, dtype=np.float32)
    weights[:, 0] = 1

    votes_needed = int(1 + ballots.shape[0] / (num_seats + 1))

    num_cands = np.max(ballots)

    while True:
        empty_mask = ballots[:, 0] == 0
        ballots[empty_mask, :-1] = ballots[empty_mask, 1:]
        ballots[empty_mask, -1] = 0

        counts = np.bincount(
            ballots.ravel(), weights=weights.ravel(), minlength=num_cands + 1
        )
        elected = counts[1:] >= votes_needed

        if elected.sum() == num_seats:
            break

        losers = np.where(counts[1:] == counts[1:].min())[0] + 1
        loser = np.random.choice(losers, 1)

        ballots[ballots == loser] = 0

    elected = np.nonzero(elected)[0] + 1

    return elected, counts


def validate_and_standardize_ballots(ballots):
    ballots = np.asarray(ballots)

    if ballots.ndim != 2:
        raise ValueError("Ballot data has wrong dim: %s" % ballots.ndim)

    non_negative_rankings = ballots >= 0
    if not non_negative_rankings.all():
        bad_ballots = ~non_negative_rankings.all(axis=1)
        bad_indices = np.nonzero(bad_ballots)[0].tolist()
        raise ValueError("Negative rankings on ballots: %s" % bad_indices)

    first = ballots[:, :-1] == 0
    second = ballots[:, 1:] == 0
    continuous_rankings = ~first | second

    if not continuous_rankings.all():
        bad_ballots = ~continuous_rankings.all(axis=1)
        bad_indices = np.nonzero(bad_ballots)[0].tolist()
        raise ValueError("Skipped rankings on ballots: %s" % bad_indices)

    return ballots
