"""Minimalist implementation of Single Transferable Vote."""

import numpy as np


def run_stv(ballots, num_seats):
    ballots = np.asarray(ballots)

    weights = np.zeros(ballots.shape, dtype=np.float32)
    weights[:, 0] = 1

    votes_needed = ballots.shape[0] / (num_seats + 1)

    num_cands = np.max(ballots)

    while True:
        counts = np.bincount(
            ballots.ravel(), weights=weights.ravel(), minlength=num_cands + 1
        )
        elected = counts[1:] >= votes_needed

        if elected.sum() == num_seats:
            break

    return elected, counts
