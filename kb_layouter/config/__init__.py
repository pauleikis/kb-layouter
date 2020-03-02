from pathlib import Path

# penalty adjustments
ALPHA = 5
_s, _m, _l, _xl = ALPHA, ALPHA ** 2, ALPHA ** 3, ALPHA ** 4

S, A, B, C, D, E, F, X = 1 / _l, 1 / _m, 1 / _s, 1, _s, _m, _l, _xl
PENALTIES = {
    'S': S,
    'A': A,
    'B': B,
    'C': C,
    'D': D,
    'E': E,
    'F': F,
    'X': X,
}
PENALTY_INDEX = "SABCDEFX"


LEFT = 'L'
RIGHT = 'R'


PATH_TO_DATA = Path('data')


CRITERION_MIN, CRITERION_MAX = 10, 99


EMPTY_SYMBOL = '◆'


class MaskException(Exception):
    pass
