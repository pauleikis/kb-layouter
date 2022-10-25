import string
from itertools import product
from functools import lru_cache

from kb_layouter.criteria import Criterion
from kb_layouter.config import PATH_TO_DATA, S, A, B, C, D, E, F, X, LEFT, RIGHT, ALPHA


class StrainCriterion(Criterion):
    valid_chars = string.ascii_uppercase
    data_filename = '1grams.txt'

    def __init__(self, hands):
        super().__init__(hands)
        self._load_data()

    def penalties(self, keycaps) -> dict:
        return {letter: self.hands.strain(key) * self.freqs.get(letter, 0) for key, letter in keycaps.items()}

    @property
    def minimum(self):
        if self._minimum is None:
            strains = sorted(map(self.hands.strain, self.hands.strains))
            freqs = sorted(self.freqs.values(), reverse=True)
            self._minimum = sum(s * f for s, f in zip(strains, freqs))
        return self._minimum

    @property
    def maximum(self):
        if self._maximum is None:
            strains = sorted(map(self.hands.strain, self.hands.strains))
            freqs = sorted(self.freqs.values())
            self._maximum = sum(s * f for s, f in zip(strains, freqs))
        return self._maximum

    def _load_data(self):
        freqs = {}
        for line in open(PATH_TO_DATA / 'languages' / self.lang / self.data_filename):
            gram, freq = line.split()
            if all(l in self.valid_chars for l in gram):
                freqs[gram] = float(freq)
        denominator = sum(freqs.values())  # normalizing sum to be equal to 1
        self.freqs = {k: (v / denominator) ** .7 for k, v in freqs.items() if v / denominator > 0.00001}


class LtStrainCriterion(StrainCriterion):
    lang = 'lt'
    name = "LT - 1gram"


class EnStrainCriterion(StrainCriterion):
    lang = 'en'
    name = "EN - 1gram"


class StretchCriterion(StrainCriterion):
    data_filename = '2grams.txt'

    def penalties(self, keycaps):
        result = {}
        for gram, freq in self.freqs.items():
            result[gram] = self.hands.stretch((keycaps.get_key(gram[0]), keycaps.get_key(gram[1]))) * freq
        return result

    @property
    def minimum(self):
        if self._minimum is None:
            strains = sorted(map(self.hands.stretch, product(self.hands.keys, self.hands.keys)))
            freqs = sorted(self.freqs.values(), reverse=True) + [0] * (len(strains) - len(self.freqs))
            self._minimum = sum(s * f for s, f in zip(strains, freqs))
        return self._minimum

    @property
    def maximum(self):
        if self._maximum is None:
            strains = sorted(map(self.hands.stretch, product(self.hands.keys, self.hands.keys)))
            freqs = [0] * (len(strains) - len(self.freqs)) + sorted(self.freqs.values())
            self._maximum = min(F, sum(s * f for s, f in zip(strains, freqs)))
        return self._maximum

class LtStretchCriterion(StretchCriterion):
    lang = 'lt'
    name = 'LT - 2gram'


class EnStretchCriterion(StretchCriterion):
    lang = 'en'
    name = 'EN - 2gram'


class PlanckClumsynessCriterion(StrainCriterion):
    data_filename = '3grams.txt'

    def __init__(self, hands):
        super().__init__(hands)
        # the implementation bases some decisions on 3x10 letter layout
        # until general solution is implemented, this can work only on planck keyb
        assert self.hands.keyboard.name in ('planck', 'ansi'), self.hands.keyboard.name

    @lru_cache(None)
    def penalty(self, keys):
        a, b, c = keys
        if self.hands.hand(a) != self.hands.hand(b) != self.hands.hand(c):
            return self.hands.stretch((a, c)) / ALPHA ** 2
        if self.hands.hand(a) != self.hands.hand(b) or self.hands.hand(b) != self.hands.hand(c):
            return S
        if a.col == b.col == c.col and a.row != b.row != c.row != a.row:
            return X
        if a.col == b.col == c.col and (a.row != b.row or b.row != c.row):
            return E
        if a == b or b == c or c == a:
            return C
        if self.hands.hand(a) == self.hands.hand(b) == self.hands.hand(c):
            if a.col == b.col and c.col in (a.col - 1, a.col + 1) and a.row != b.row:
                if b.col in (2, 3, 4, 5, 6, 7):
                    if (self.down(a, b) and self.outwards(b, c)) or self.up(a, b) and self.inwards(b, c):
                        return C
                    return E
                return X
            if b.col == c.col and a.col in (b.col - 1, b.col + 1) and b.row != c.row:
                if b.col in (2, 3, 4, 5, 6, 7):
                    if (self.down(b, c) and self.outwards(a, b)) or (self.up(b, c) and self.inwards(a, b)):
                        return C
                    return E
                return X
            if b.col in (1, 2, 3, 6, 7, 8):
                if a.col in (0, 9) and c.col in (4, 5):
                    return E
                if c.col in (0, 9) and a.col in (4, 5):
                    return E
        if self.hands.hand(a) == self.hands.hand(b) == self.hands.hand(c) == LEFT:
            if a.col < b.col < c.col and a.row >= b.row <= c.row:
                return S
            if a.col > b.col > c.col and a.row >= b.row <= c.row:
                return B
            if a.col == c.col < b.col and a.row <= b.row >= c.row and b.col > 2:
                return B
        elif self.hands.hand(a) == self.hands.hand(b) == self.hands.hand(c) == RIGHT:
            if a.col > b.col > c.col and a.row >= b.row <= c.row:
                return S
            if a.col < b.col < c.col and a.row >= b.row <= c.row:
                return B
            if a.col == c.col > b.col and a.row <= b.row >= c.row and b.col < 7:
                return B
        if self.hands.hand(a) == self.hands.hand(b) == self.hands.hand(c):
            if (a.col == b.col or b.col == c.col) and b.col in (4, 5):
                return X
            return F

        return  # all cases should be covered

    def up(self, a, b):
        return a.row > b.row

    def down(self, a, b):
        return a.row < b.row

    def inwards(self, a, b):
        if self.hands.hand(a) != self.hands.hand(b):
            return False
        return (a.col < b.col) == (self.hands.hand(a) == LEFT)

    def outwards(self, a, b):
        if self.hands.hand(a) != self.hands.hand(b):
            return False
        return (a.col > b.col) == (self.hands.hand(a) == LEFT)

    def penalties(self, keycaps):
        result = {}
        keys = keycaps._reverse_map
        for gram, freq in self.freqs.items():
            result[gram] = freq * self.penalty((
                keys[gram[0]],
                keys[gram[1]],
                keys[gram[2]],
            ))
        return result

    @property
    def minimum(self):
        if self._minimum is None:
            strains = sorted(map(self.penalty, product(self.hands.keys, self.hands.keys, self.hands.keys)))
            freqs = sorted(self.freqs.values(), reverse=True) + [0] * (len(strains) - len(self.freqs))
            self._minimum = max(A, sum(s * f for s, f in zip(strains, freqs)))
        return self._minimum

    @property
    def maximum(self):
        if self._maximum is None:
            strains = sorted(map(self.penalty, product(self.hands.keys, self.hands.keys, self.hands.keys)))
            freqs = [0] * (len(strains) - len(self.freqs)) + sorted(self.freqs.values())
            self._maximum = min(E, sum(s * f for s, f in zip(strains, freqs)))
        return self._maximum

class LtPlanckClumsynessCriterion(PlanckClumsynessCriterion):
    lang = 'lt'
    name = 'LT - 3gram'

class EnPlanckClumsynessCriterion(PlanckClumsynessCriterion):
    lang = 'en'
    name = 'EN - 3gram'


class TirednessCriterion(Criterion):
    valid_chars = string.ascii_uppercase
    data_filename = 'ospd.txt'
    lang = 'en'
    penalty_weights = {
        1: S,
        2: S,
        3: S,
        4: A,
        5: C,
        6: D,
        7: E,
        8: F
    }

    def __init__(self, hands):
        super().__init__(hands)
        self._load_data()

    def _load_data(self):
        self.words = []
        for line in open(PATH_TO_DATA / 'languages' / self.lang / self.data_filename):
            self.words.append(line.strip().upper())

    def penalties(self, keycaps):
        penalties = {}
        for word in self.words:
            hand = None
            count = 1
            max_count = 0
            for letter in word:
                if self.hands.hand(keycaps.get_key(letter)) == hand:
                    count += 1
                else:
                    if count > max_count:
                        max_count = count
                    hand = self.hands.hand(keycaps.get_key(letter))
                    count = 1
            if count > max_count:
                max_count = count
            penalties[word] = self.penalty_weights[max_count]
        return penalties

    @property
    def minimum(self):
        if self._minimum is None:
            self._minimum = S * len(self.words)
        return self._minimum

    @property
    def maximum(self):
        if self._maximum is None:
            self._maximum = sum(self.penalty_weights[len(w)] for w in self.words)
        return self._maximum
