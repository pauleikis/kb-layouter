from functools import lru_cache

from kb_layouter.config import CRITERION_MIN, CRITERION_MAX

class Criterion:
    _minimum = None
    _maximum = None

    def __init__(self, hands):
        self.hands = hands

    def evaluate(self, keycaps):
        return self.adjust(sum(self.penalties(keycaps).values()))

    def penalties(self, keycaps) -> dict:
        raise NotImplementedError

    @property
    def minimum(self):
        raise NotImplementedError

    @property
    def maximum(self):
        raise NotImplementedError

    def adjust(self, value):
        minimum, maximum = self.minimum, self.maximum
        assert minimum < maximum
        length = maximum - minimum
        return CRITERION_MIN + (CRITERION_MAX - CRITERION_MIN) * (value - minimum) / length

    @property
    def name(self):
        return self.__class__.__name__

    def __repr__(self):
        return self.name

    def detailed(self, keycaps) -> str:
        penalties = self.penalties(keycaps)
        top = sorted(penalties, key=penalties.get, reverse=True)[:5]
        total = sum(penalties.values())
        result = f'{self!s:>20}: {self.evaluate(keycaps):8.3f}\n'
        for t in top:
            result += f'{t:>27}: {penalties[t] / total:>5.1%}\n'
        return result.rstrip()


class CriterionSuite:

    def __init__(self, hands, criteria, weights=None):
        self.hands = hands
        if weights is None:
            weights = [2] * len(criteria)
        self.criteria = {cr(hands): w for cr, w in zip(criteria, weights)}

    @lru_cache(maxsize=1024)
    def evaluate(self, keycaps) -> float:
        return self.adjust(
            sum(
                cr.evaluate(keycaps) ** w for cr, w in self.criteria.items()
            )
        )

    def adjust(self, value):
        minimum = sum(CRITERION_MIN ** w for w in self.criteria.values())
        maximum = sum(CRITERION_MAX ** w for w in self.criteria.values())
        assert minimum < maximum
        length = maximum - minimum
        length **= .5
        return CRITERION_MIN + (CRITERION_MAX - CRITERION_MIN) * (value - minimum) / length

    def summary(self, keycaps, detailed=False) -> str:
        result = f'{keycaps:full}\n'
        result += f'    Hands: {self.hands.name}\n Criteria:\n'
        for cr, w in self.criteria.items():
            if detailed:
                result += cr.detailed(keycaps) + '\n\n'
            else:
                loss = cr.evaluate(keycaps)
                result += f"{cr!s:>20}: {loss ** w:9.2f}  ({loss:>8.3f} ** {w:<0.5g} )\n"
        result += f"{'AVERAGE':>20}: {self.evaluate(keycaps):9.2f}"
        return result

if __name__ == "__main__":
    pass
