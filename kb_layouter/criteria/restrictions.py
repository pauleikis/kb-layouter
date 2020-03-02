from kb_layouter.criteria import Criterion
from kb_layouter.keyboard import Key
from kb_layouter.config import S, F, E, C

class Biased(Criterion):

    @property
    def minimum(self):
        return S * 26

    @property
    def maximum(self):
        return F * 26

    def penalties(self, keycaps):
        return {l: self.penalty(k, l) for k, l in keycaps.items()}

    def penalty(self, key, letter):
        # if letter in "QXZCBJ" and key in (
        #     Key(0, 0),
        #     Key(0, 4),
        #     Key(0, 5),
        #     Key(2, 0),
        #     Key(2, 1),
        #     Key(2, 2),
        # ):
        #     return S
        # if letter in "KPVYFG" and key in (
        #     Key(1, 4),
        #     Key(1, 5),
        #     Key(2, 4),
        #     Key(2, 5),
        #     Key(1, 0),
        #     Key(1, 9),
        # ):
        #     return S
        # if letter in "FP" and key in (Key(0, 3), Key(0, 6)):
        #     return S
        if letter in 'W' and key in (Key(0, 0), ):
            return F
        if letter in "IAEOTSNU" and key in (
            Key(1, 1),
            Key(1, 2),
            Key(1, 3),
            Key(2, 3),
            Key(2, 6),
            Key(1, 6),
            Key(1, 7),
            Key(1, 8),
        ):
            return S
        # if letter in "RLHMDW" and key in (
        #     Key(0, 1),
        #     Key(0, 2),
        #     Key(0, 7),
        #     Key(0, 8),
        #     Key(0, 3),
        #     Key(0, 6),
        # ):
        #     return S
        if key not in (
            Key(1, 1),
            Key(1, 2),
            Key(1, 3),
            Key(2, 3),
            Key(2, 6),
            Key(1, 6),
            Key(1, 7),
            Key(1, 8),
        ):
            return S
        return F

class Vowels(Criterion):

    @property
    def minimum(self):
        return S * 4

    @property
    def maximum(self):
        return F * 4

    def penalties(self, keycaps):
        keys = {l: keycaps.get_key(l) for l in 'IAOEU'}
        return {l: self.penalty(l, keys) for l in 'IAOE'}

    def penalty(self, letter, keys):
        if any(self.row_neighbour(keys[letter], k) for l, k in keys.items() if l != letter):
            return F
        if any(self.column_neighbour(keys[letter], k) for l, k in keys.items() if l != letter):
            return E
        return S

    def row_neighbour(self, a, b):
        return a.row == b.row and ((a.col + 1 == b.col) or (a.col - 1 == b.col))

    def column_neighbour(self, a, b):
        return a.col == b.col and ((a.row + 1 == b.row) or (a.row - 1 == b.row))
