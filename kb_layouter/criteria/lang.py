import string
from itertools import product

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
        self.freqs = {k: v / denominator for k, v in freqs.items() if v / denominator > 0.0001}


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
            self._maximum = sum(s * f for s, f in zip(strains, freqs))
        return self._maximum


class LtStretchCriterion(StretchCriterion):
    lang = 'lt'
    name = 'LT - 2gram'


class EnStretchCriterion(StretchCriterion):
    lang = 'en'
    name = 'EN - 2gram'


class AlternationCriterion(StretchCriterion):

    def penalties(self, keycaps):
        result = {}
        for gram, freq in self.freqs.items():
            result[gram] = freq * (
                C
                if
                    self.hands.hand(keycaps.get_key(gram[0])) == self.hands.hand(keycaps.get_key(gram[1]))
                else
                    A
            )
        return result

    @property
    def minimum(self):
        if self._minimum is None:
            self._minimum = sum(self.freqs.values()) * A
        return self._minimum

    @property
    def maximum(self):
        if self._maximum is None:
            self._maximum = sum(self.freqs.values()) * C
        return self._maximum


class LtAlternationCriterion(AlternationCriterion):
    lang = 'lt'
    name = 'LT - 2gram'


class EnAlternationCriterion(AlternationCriterion):
    lang = 'en'
    name = 'EN - 2gram'


class PlanckClumsynessCriterion(StrainCriterion):
    data_filename = '3grams.txt'

    def __init__(self, hands):
        super().__init__(hands)
        # the implementation bases some decisions on 3x10 letter layout
        # until general solution is implemented, this can work only on planck keyb
        assert self.hands.keyboard.name == 'planck'

    def penalty(self, keys):
        a, b, c = keys
        if self.hands.hand(a) != self.hands.hand(b) != self.hands.hand(c):
            return self.hands.stretch((a, c)) / ALPHA ** 2
        if self.hands.hand(a) != self.hands.hand(b) or self.hands.hand(b) != self.hands.hand(c):
            return B
        if a == b or b == c or c == a:
            return C
        if a.col == b.col == c.col and a.row != b.row != c.row != a.row:
            return X
        if a.col == b.col == c.col and (a.row != b.row or b.row != c.row):
            return E
        if self.hands.hand(a) == self.hands.hand(b) == self.hands.hand(c):
            if a.col == b.col and c.col in (a.col - 1, a.col + 1) and a.row != b.row:
                if b.col in (2, 7) and a.row > b.row:
                    return E
                if b.col in (3, 4, 5, 6):
                    return E
                return X
            if b.col == c.col and a.col in (b.col - 1, b.col + 1) and b.row != c.row:
                if b.col in (2, 7) and c.row > b.row:
                    return E
                if b.col in (3, 4, 5, 6):
                    return E
                return X
        if self.hands.hand(a) == self.hands.hand(b) == self.hands.hand(c) == LEFT:
            if a.col < b.col < c.col and a.row >= b.row <= c.row:
                return S
            if a.col > b.col > c.col and a.row >= b.row <= c.row:
                return A
            if a.col == c.col < b.col and a.row <= b.row >= c.row and b.col > 2:
                return A
        elif self.hands.hand(a) == self.hands.hand(b) == self.hands.hand(c) == RIGHT:
            if a.col > b.col > c.col and a.row >= b.row <= c.row:
                return S
            if a.col < b.col < c.col and a.row >= b.row <= c.row:
                return A
            if a.col == c.col > b.col and a.row <= b.row >= c.row and b.col < 7:
                return A
        if self.hands.hand(a) == self.hands.hand(b) == self.hands.hand(c):
            return D

        return C

    def penalties(self, keycaps):
        result = {}
        for gram, freq in self.freqs.items():
            result[gram] = freq * self.penalty((
                keycaps.get_key(gram[0]),
                keycaps.get_key(gram[1]),
                keycaps.get_key(gram[2]),
            ))
        return result

    @property
    def minimum(self):
        if self._minimum is None:
            strains = sorted(map(self.penalty, product(self.hands.keys, self.hands.keys, self.hands.keys)))
            freqs = sorted(self.freqs.values(), reverse=True) + [0] * (len(strains) - len(self.freqs))
            self._minimum = sum(s * f for s, f in zip(strains, freqs))
        return self._minimum

    @property
    def maximum(self):
        if self._maximum is None:
            strains = sorted(map(self.penalty, product(self.hands.keys, self.hands.keys, self.hands.keys)))
            freqs = [0] * (len(strains) - len(self.freqs)) + sorted(self.freqs.values())
            self._maximum = sum(s * f for s, f in zip(strains, freqs))
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
