import numpy as np

from connect_four.envs import TwoPlayerGameEnvVariables


diagram_11_1 = TwoPlayerGameEnvVariables(
    state=np.array([
        [
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 1, 1, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 1, 1, 0, 0, 0, ],
        ],
        [
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 1, 1, 1, 0, 0, ],
            [0, 0, 0, 0, 1, 0, 0, ],
        ],
    ]),
    player_turn=0,
)

# A set of difficult positions to prove in Connect Four, from the original paper.
# The positions are in separated by section.
# For each section, positions are sorted in ascending order by estimated difficulty.

# From Section 13.2, these are the promising positions for proving d1, d2.
# Disprove this position.
diagram_13_6_b3 = TwoPlayerGameEnvVariables(
    state=np.array([
        [
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 1, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 1, 0, 0, 0, ],
            [0, 1, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 1, 0, 0, 0, ],
        ],
        [
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 1, 0, 0, 0, ],
            [0, 1, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 1, 0, 0, 0, ],
            [0, 1, 0, 0, 0, 0, 0, ],
        ],
    ]),
    player_turn=0,
)
diagram_13_6 = TwoPlayerGameEnvVariables(
    state=np.array([
        [
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 1, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 1, 0, 0, 0, ],
            [0, 1, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 1, 0, 0, 0, ],
        ],
        [
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 1, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 1, 0, 0, 0, ],
            [0, 1, 0, 0, 0, 0, 0, ],
        ],
    ]),
    player_turn=1,
)
diagram_13_4 = TwoPlayerGameEnvVariables(
    state=np.array([
        [
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 1, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 1, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 1, 0, 0, 0, ],
        ],
        [
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 1, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 1, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
        ],
    ]),
    player_turn=1,
)
diagram_13_2 = TwoPlayerGameEnvVariables(
    state=np.array([
        [
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 1, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 1, 0, 0, 0, ],
        ],
        [
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 1, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
        ],
    ]),
    player_turn=1,
)
# From Section 13.3, these are the promising positions for proving d1, c1.
diagram_13_12_d2 = TwoPlayerGameEnvVariables(
    state=np.array([
        [
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 1, 0, 1, 0, ],
            [0, 0, 0, 1, 0, 1, 0, ],
        ],
        [
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 1, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 1, 0, 0, 0, 1, ],
        ],
    ]),
    player_turn=1,
)
position_d1_c1_f1_g1_f2 = TwoPlayerGameEnvVariables(
    state=np.array([
        [
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 1, 0, ],
            [0, 0, 0, 1, 0, 1, 0, ],
        ],
        [
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 1, 0, 0, 0, 1, ],
        ],
    ]),
    player_turn=1,
)
diagram_13_10 = TwoPlayerGameEnvVariables(
    state=np.array([
        [
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 1, 0, 1, 0, ],
        ],
        [
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 1, 0, 0, 0, 0, ],
        ],
    ]),
    player_turn=1,
)
# From Section 13.4, these are the promising positions for proving d1, b1.
diagram_13_15_f2 = TwoPlayerGameEnvVariables(
    state=np.array([
        [
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 1, 0, ],
            [0, 0, 0, 1, 0, 1, 0, ],
        ],
        [
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 1, 0, 0, 1, 0, 0, ],
        ],
    ]),
    player_turn=1,
)
diagram_13_14 = TwoPlayerGameEnvVariables(
    state=np.array([
        [
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 1, 1, 1, 0, ],
        ],
        [
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 1, 1, 0, 0, 0, 1, ],
        ],
    ]),
    player_turn=0,
)
diagram_13_13 = TwoPlayerGameEnvVariables(
    state=np.array([
        [
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 1, 0, 1, 0, ],
        ],
        [
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 1, 0, 0, 0, 0, 0, ],
        ],
    ]),
    player_turn=1,
)
# From Section 13.5, these are the promising positions for proving d1, a1.
diagram_13_16 = TwoPlayerGameEnvVariables(
    state=np.array([
        [
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 1, 0, 0, ],
            [0, 0, 0, 1, 1, 0, 0, ],
        ],
        [
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [1, 0, 1, 0, 0, 0, 0, ],
        ],
    ]),
    player_turn=1,
)
diagram_13_17 = TwoPlayerGameEnvVariables(
    state=np.array([
        [
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 1, 0, 0, ],
            [0, 0, 0, 1, 1, 0, 0, ],
        ],
        [
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [1, 0, 0, 0, 0, 1, 0, ],
        ],
    ]),
    player_turn=1,
)
position_d1_a1_e1 = TwoPlayerGameEnvVariables(
    state=np.array([
        [
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 1, 1, 0, 0, ],
        ],
        [
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, ],
            [1, 0, 0, 0, 0, 0, 0, ],
        ],
    ]),
    player_turn=1,
)
