from kb_layouter.config import RIGHT, LEFT, S, A, B, C, D, E, F, X
from kb_layouter.criteria import Criterion

class ShortcutCriterion(Criterion):

    def penalty(self, key, letter):
        return None

    def penalties(self, keycaps):
        result = {}
        for key, letter in keycaps.items():
            penalty = self.penalty(key, letter)
            if penalty is not None:
                result[letter] = penalty
        return result


class ColemakLikeShortcutsCriterion(ShortcutCriterion):
    name = 'COLEMAK shortcuts'

    def penalty(self, key, letter):
        if letter in 'CV':
            if key.col > 2:
                return X
            return S
        if letter in 'AZ':
            if key.col > 3:
                return E
            return S
        if letter in 'D':
            if key.col > 3:
                return E
            return B
        if letter in 'RFKTNEWBX':
            if key.col > 3:
                return D
            return C
        if letter in 'Q':
            # I don't want to press cmd+q accidentally
            # this is a deviation from COLEMAK philosophy
            if self.hands.hand(key) == LEFT and (key.col != 4 or key.row != 0):
                return E
            return S
        return None

    @property
    def minimum(self):
        return S * 2 + S * 2 + B * 1 + C * 9 + S * 1

    @property
    def maximum(self):
        return X * 2 + E * 2 + E * 1 + D * 9 + E * 1
