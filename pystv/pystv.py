"""Minimalist implementation of Single Transferable Vote."""
import collections

import numpy as np

RoundResult = collections.namedtuple("RoundResults", ["count", "elected", "eliminated"])


def run_stv(ballots, num_seats):
    ballots = validate_and_standardize_ballots(ballots)

    weights = np.zeros(ballots.shape, dtype=np.float64)
    weights[:, 0] = 1

    votes_needed = int(1 + ballots.shape[0] / (num_seats + 1))

    num_cands = np.max(ballots)

    round_info = []

    while True:
        counts = np.bincount(
            ballots.ravel(), weights=weights.ravel(), minlength=num_cands + 1
        )
        elected = counts[1:] >= votes_needed
        elected_idx = np.nonzero(elected)[0] + 1

        if elected.sum() == num_seats:
            round_info.append(RoundResult(counts.tolist(), elected_idx.tolist(), None))
            return round_info

        min_count = counts[1:].min()
        eliminated = np.where(counts[1:] == min_count)[0] + 1
        eliminated = np.random.choice(eliminated, 1)

        round_info.append(
            RoundResult(counts.tolist(), elected_idx.tolist(), eliminated)
        )

        for col in range(ballots.shape[1]):
            mask = ballots[:, col] == eliminated
            ballots[mask, col:-1] = ballots[mask, col + 1 :]
            ballots[mask, -1] = 0

        for idx in elected_idx:
            if counts[idx] > votes_needed:
                adjustment = votes_needed / counts[idx]
                location = np.nonzero(ballots == idx)

                next_col = np.minimum(location[1] + 1, ballots.shape[1] - 1)
                next = (location[0], next_col)

                orig = weights[location]
                updated = orig * adjustment
                diff = orig - updated

                weights[location] = updated
                weights[next] = diff


def elected_indices(e):
    elected_idx = np.nonzero(e)[0] + 1
    return elected_idx.tolist()


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
