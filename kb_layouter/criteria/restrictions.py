from collections import Counter

from kb_layouter.criteria import Criterion
from kb_layouter.keyboard import Key
from kb_layouter.config import S, F, E, B, C, X, A, D, LEFT, RIGHT


class Biased(Criterion):
    zones = {
        1: (
            {
                Key(1, 0),
                Key(1, 1),
                Key(1, 2),
                Key(1, 3),
                Key(1, 6),
                Key(1, 7),
                Key(1, 8),
                Key(1, 9),
            },
            "OTSAENRI"
        ),
        3: ({
            Key(0, 1),
            Key(0, 2),
            Key(0, 7),
            Key(0, 8),
            Key(2, 3),
            Key(2, 6),
            Key(1, 4),
            Key(1, 5),
        }, "KULDMHPY"),
        5: ({
            Key(0, 3),
            Key(0, 6),
            Key(2, 0),
            Key(2, 2),
            Key(2, 5),
        }, "VJFWG"),
        8: ({
            Key(0, 0),
            Key(0, 4),
            Key(0, 5),
            Key(2, 1),
            Key(2, 4),
        }, "BZCXQ"),
    }
    penalty_list = [S, A, B, C, D, E, F, X]

    def __init__(self, hands):
        super().__init__(hands)
        assert len(set().union(*(keys for keys, _ in self.zones.values()))) == 26
        assert len(set().union(*(letters for _, letters in self.zones.values()))) == 26


    @property
    def minimum(self):
        return S * 26

    @property
    def maximum(self):
        return C * 26

    def penalties(self, keycaps):
        return {l: self.penalty(k, l) for k, l in keycaps.items()}

    def penalty(self, key, letter):
        for zone, (keys, letters) in self.zones.items():
            if key in keys:
                actual_zone = zone
            if letter in letters:
                target_zone = zone
        diff = abs(actual_zone - target_zone)
        return self.penalty_list[diff]

class Vowels(Criterion):

    @property
    def minimum(self):
        return S

    @property
    def maximum(self):
        return F

    def penalties(self, keycaps):
        c = Counter(self.hands.hand(keycaps.get_key(l)) for l in "IAOE")
        if c[LEFT] == 2:
            return {'vowels': S}
        if c[LEFT] in (1, 3):
            return {'vowels': B}
        return {'vowels': F}
