import random
import string

from kb_layouter.config import EMPTY_SYMBOL, MaskException


class Keycaps:
    def __init__(self, keyboard, keycaps, mask=None):
        self.keyboard = keyboard
        self.mask = mask
        kb_name, letters = keycaps.split(':', 1)
        assert len(keyboard.keys) == len(letters)
        assert len(letters) == len(set(letters))
        if mask:
            if any(a != b for a, b in zip(mask, letters) if a != EMPTY_SYMBOL):
                raise MaskException
        self._keycaps = {k: v.upper() for k, v in zip(keyboard.keys, letters)}
        self._reverse_map = {v.upper(): k for k, v in zip(keyboard.keys, letters)}
        self._repr = keycaps

    def __repr__(self):
        return self._repr

    def __format__(self, format):
        if format == 'full':
            return self.keyboard.render(self, name=True) + '\n' + f'  Keycaps: "{self}"'
        return self.__repr__().__format__(format)

    def __eq__(self, other):
        if type(self) == type(other):
            return self.__repr__() == other.__repr__() and self.mask == other.mask
        return False

    def __hash__(self):
        return hash((self.__repr__(), self.mask))

    def __getitem__(self, key):
        return self._keycaps[key]

    def __iter__(self):
        return iter(self._keycaps)

    def items(self):
        return self._keycaps.items()

    def letters(self):
        return self._keycaps.values()

    def get_key(self, letter):
        return self._reverse_map[letter]

    @staticmethod
    def randomizer(keyboard, letters=string.ascii_uppercase, mask=''):
        def random_keycaps():
            source = set(letters)
            if mask:
                source -= set(mask)
            keycaps = "".join(random.sample(list(source), len(source)))
            if mask:
                generated = keycaps
                keycaps = mask
                for letter in generated:
                    keycaps = keycaps.replace(EMPTY_SYMBOL, letter, 1)
                assert EMPTY_SYMBOL not in keycaps
                assert len(keycaps) == len(letters)
            return Keycaps(keyboard, keyboard.name + ':' + keycaps, mask)
        return random_keycaps

    def _reordered(self, letters):
        assert len(letters) == len(self.letters())
        if not isinstance(letters, str):
            letters = ''.join(letters)
        return Keycaps(self.keyboard, self.keyboard.name + ':' + letters, mask=self.mask)

    def __matmul__(self, other):
        assert type(self) == type(other)
        assert self.keyboard == other.keyboard
        assert self.mask == other.mask
        this = list(self.letters())
        that = list(other.letters())
        new = [a if a == b else None for a, b in zip(this, that)]
        missing = set(this) - set(new)
        missing_idx = {idx for idx, letter in enumerate(new) if letter is None}
        still_missing = set()
        while missing:
            letter = random.sample(missing, 1)[0]
            missing.discard(letter)
            for l in random.sample((this, that), 2):
                idx = l.index(letter)
                if new[idx] is None:
                    new[idx] = letter
                    missing_idx.discard(idx)
                    break
            else:
                still_missing.add(letter)
        while still_missing:
            letter = random.sample(still_missing, 1)[0]
            still_missing.discard(letter)
            idx = random.sample(missing_idx, 1)[0]
            missing_idx.discard(idx)
            new[idx] = letter
        return self._reordered(new)

    def _mutated(self):
        if self.mask:
            locked_ids = {idx for idx, letter in enumerate(self.mask) if letter != EMPTY_SYMBOL}
        else:
            locked_ids = ()
        source_idx = random.choice(
            [idx for idx in range(len(self.letters())) if idx not in locked_ids]
        )
        target_idx = random.choice(
            [idx for idx in range(len(self.letters())) if idx != source_idx and idx not in locked_ids]
        )
        letters = list(self.letters())
        letters[target_idx], letters[source_idx] = letters[source_idx], letters[target_idx]
        return self._reordered(letters)

    def __rshift__(self, other):
        result = self
        for _ in range(other):
            result = result._mutated()
        return result

if __name__ == "__main__":
    from kb_layouter.keyboard import PLANCK
    k = Keycaps(PLANCK, 'planck:XMRFGQBOUNLSTDYIAEHZCVKJWP')
    q = Keycaps(PLANCK, 'planck:QWERTYUIOASDFGHJKLPZXCVBNM')
    # print(k)
    # print(k >> 1)
    print(q)
    print(q.randomized())
    print(q.randomized())
    # print(q >> 1)
    # print(k @ q)
