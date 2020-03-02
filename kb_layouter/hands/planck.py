from itertools import product

from kb_layouter.keyboard import Keyboard, Key, PLANCK
from kb_layouter.hands import Hands
from kb_layouter.config import LEFT, RIGHT, PATH_TO_DATA

def generate_planck():
    kb = PLANCK
    h = Hands(kb)

    for k in kb.keys:
        h.hands[k] = LEFT if k.col < 5 else RIGHT

    strains = [
        ['F', 'B', 'A', 'D', 'E', 'E', 'D', 'A', 'B'],
        ['C', 'A', 'S', 'S', 'C', 'C', 'S', 'S', 'A', 'C'],
        ['D', 'E', 'B', 'A', 'D', 'D', 'A'],
    ]
    for r, row in enumerate(strains):
        for c, rating in enumerate(row):
            h.strains[Key(r, c)] = rating

    # left_keys = [key for key in kb.keys if h.hands[key] == LEFT]
    # right_keys = [key for key in kb.keys if h.hands[key] == RIGHT]
    # for k1, k2 in product(left_keys, left_keys):
    #     h.pairs.setdefault((k1, k2), 'C')
    # p = {}

    # p[Key(row=0, col=0)] = {
    #     Key(row=0, col=3): 'A',
    #     Key(row=0, col=4): 'B',
    #     Key(row=1, col=3): 'B',
    # }
    S, A, B, C, D, E, F, X = 'S', 'A', 'B', 'C', 'D', 'E', 'F', 'X'
    pain = [
        [
            F, E, D, A, B,
            X, E, E, C, B,
            X, F, E, C, C,
        ],
        [
            E, D, B, A, D,
            D, F, C, B, E,
            F, F, F, C, E,
        ],
        [
            E, B, C, A, E,
            C, D, F, S, E,
            F, F, F, C, F,
        ],
        [
            C, B, A, C, C,
            B, D, F, E, B,
            E, F, F, F, D,
        ],
        [
            C, D, C, A, E,
            C, D, E, F, F,
            D, E, X, X, F,
        ],


        [
            X, E, B, B, B,
            F, E, D, S, S,
            X, F, E, A, A,
        ],
        [
            F, F, D, C, F,
            F, D, B, S, E,
            E, F, E, A, D,
        ],
        [
            F, A, E, B, F,
            D, B, C, S, F,
            E, F, F, S, F,
        ],
        [
            C, C, S, E, F,
            B, B, S, B, B,
            E, E, C, E, B,
        ],
        [
            D, E, D, A, F,
            B, D, C, A, D,
            C, E, F, D, F,
        ],


        [
            X, F, E, C, D,
            X, E, D, B, C,
            E, E, C, A, B,
        ],
        [
            F, F, F, F, F,
            E, F, E, D, E,
            E, F, C, A, D,
        ],
        [
            F, F, E, F, F,
            F, E, D, D, F,
            E, D, E, A, E,
        ],
        [
            E, D, C, F, F,
            D, C, S, E, E,
            C, B, S, B, C,
        ],
        [
            E, E, F, C, F,
            E, E, D, B, F,
            D, D, E, B, D,
        ],
    ]

    for a, dests in enumerate(pain):
        a = Key(row=a // 5, col=a % 5)
        for b, penalty in enumerate(dests):
            b = Key(row=b // 5, col=b % 5)
            h.pairs[a, b] = penalty

    # h.add_stretch(row1=0, row2=0, value='B')
    # h.add_stretch(row1=0, row2=1, value='B')
    # h.add_stretch(row1=0, row2=2, value='E')
    # h.add_stretch(row1=1, row2=0, value='D')
    # h.add_stretch(row1=1, row2=1, value='S')
    # h.add_stretch(row1=1, row2=2, value='D')
    # h.add_stretch(row1=2, row2=0, value='F')
    # h.add_stretch(row1=2, row2=1, value='E')
    # h.add_stretch(row1=2, row2=2, value='D')

    # h.add_stretch(col1=0, col2=0, value='F')
    # h.add_stretch(col1=0, col2=1, value='E')
    # h.add_stretch(col1=0, col2=2, value='E')
    # h.add_stretch(col1=0, col2=3, value='A')
    # h.add_stretch(col1=0, col2=4, value='A')

    # h.add_stretch(col1=1, col2=0, value='F')
    # h.add_stretch(col1=1, col2=1, value='F')
    # h.add_stretch(col1=1, col2=2, value='E')
    # h.add_stretch(col1=1, col2=3, value='C')
    # h.add_stretch(col1=1, col2=4, value='D')

    # h.add_stretch(col1=2, col2=0, value='F')
    # h.add_stretch(col1=2, col2=1, value='D')
    # h.add_stretch(col1=2, col2=2, value='F')
    # h.add_stretch(col1=2, col2=3, value='S')
    # h.add_stretch(col1=2, col2=4, value='F')

    # h.add_stretch(col1=3, col2=0, value='C')
    # h.add_stretch(col1=3, col2=1, value='D')
    # h.add_stretch(col1=3, col2=2, value='S')
    # h.add_stretch(col1=3, col2=3, value='D')
    # h.add_stretch(col1=3, col2=4, value='A')

    # h.add_stretch(col1=4, col2=0, value='C')
    # h.add_stretch(col1=4, col2=1, value='D')
    # h.add_stretch(col1=4, col2=2, value='F')
    # h.add_stretch(col1=4, col2=3, value='A')
    # h.add_stretch(col1=4, col2=4, value='E')

    # # neighboring fingers over two rows downwards
    # h.add_stretch(row1=0, row2=2, col1=0, col2=1, value='F')
    # h.add_stretch(row1=0, row2=2, col1=1, col2=2, value='F')
    # h.add_stretch(row1=0, row2=2, col1=1, col2=0, value='F')
    # h.add_stretch(row1=0, row2=2, col1=2, col2=1, value='F')

    # # neighboring fingers over two rows upwards
    # h.add_stretch(row1=2, row2=0, col1=0, col2=1, value='E')
    # h.add_stretch(row1=2, row2=0, col1=1, col2=2, value='F')
    # h.add_stretch(row1=2, row2=0, col1=2, col2=3, value='F')
    # h.add_stretch(row1=2, row2=0, col1=3, col2=4, value='F')
    # h.add_stretch(row1=2, row2=0, col1=1, col2=0, value='F')
    # h.add_stretch(row1=2, row2=0, col1=2, col2=1, value='F')

    # # extra streches to make them super undesirable
    # h.add_stretch(col1=0, col2=0, value='F')
    # h.add_stretch(col1=1, col2=1, value='F')
    # h.add_stretch(col1=0, col2=1, value='E')
    # h.add_stretch(col1=1, col2=0, value='E')
    # h.add_stretch(col1=2, col2=4, value='F')
    # h.add_stretch(col1=4, col2=2, value='F')

    # # penalize downwards outwards movement of index and middle finger
    # h.add_stretch(row1=0, row2=1, col1=4, col2=3, value='F', override=True)
    # h.add_stretch(row1=0, row2=1, col1=3, col2=2, value='F', override=True)
    # h.add_stretch(row1=1, row2=2, col1=4, col2=3, value='F', override=True)
    # h.add_stretch(row1=1, row2=2, col1=3, col2=2, value='F', override=True)
    # h.add_stretch(row1=0, row2=2, col1=4, col2=3, value='F', override=True)
    # h.add_stretch(row1=0, row2=2, col1=3, col2=2, value='F', override=True)

    # for k1, values in p.items():
    #     for k2, v in values.items():
    #         h.pairs[(k1, k2)] = v

    # mirror stretces of the left hand keys
    for (k1, k2), v in list(h.pairs.items()):
        if h.hand(k2) != LEFT != h.hand(k1):
            continue
        k1 = k1._replace(col=9 - k1.col)
        k2 = k2._replace(col=9 - k2.col)
        if k1 in h.strains and k2 in h.strains:
            h.pairs[(k1, k2)] = v

    h._to_file(PATH_TO_DATA / 'hands' / 'planck.psi.txt')


if __name__ == "__main__":
    generate_planck()
    h = Hands(Keyboard('planck'), name='planck.psi')
    print(f'{h:full}')
