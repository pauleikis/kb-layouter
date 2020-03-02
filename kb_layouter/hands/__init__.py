from kb_layouter.config import PENALTIES, C, LEFT, RIGHT, PENALTY_INDEX, PATH_TO_DATA
from kb_layouter.keyboard import Key

class Hands:

    def __init__(self, keyboard, name=None):
        self.keyboard = keyboard

        self.strains = {}
        self.pairs = {}
        self.hands = {}

        if name:
            self._load_from_file(PATH_TO_DATA / 'hands' / f'{name}.txt')
        self.name = name or '<ANONYMOUS>'

    @property
    def keys(self):
        return self.strains.keys()

    def stretch(self, keys):
        return PENALTIES.get(self.pairs.get(keys, 'B'))

    def strain(self, key):
        return PENALTIES[self.strains[key]]

    def hand(self, key):
        return self.hands[key]

    def add_stretch(self, row1=None, row2=None, col1=None, col2=None, value='C', override=False):
        for k1 in self.keyboard.keys:
            for k2 in self.keyboard.keys:
                if self.hand(k1) != self.hand(k2):
                    continue
                if row1 is not None and row1 != k1.row:
                    continue
                if row2 is not None and row2 != k2.row:
                    continue
                if col1 is not None and col1 != k1.col:
                    continue
                if col2 is not None and col2 != k2.col:
                    continue
                old_value = self.pairs.get((k1, k2))
                if not old_value or override:
                    self.pairs[(k1, k2)] = value
                else:
                    oi = PENALTY_INDEX.find(old_value)
                    ni = PENALTY_INDEX.find(value)
                    self.pairs[(k1, k2)] = PENALTY_INDEX[round((oi + ni)/2)]

    def _validate(self):
        keys = set(self.keyboard.keys)
        assert keys == set(self.strains)
        assert keys == set(self.hands)
        assert all(k1 in self.strains and k2 in self.strains for k1, k2 in self.pairs)

    def _load_from_file(self, file):
        strains, pairs, hands = False, False, False
        for line in open(file):
            if line.startswith('keyboard: '):
                assert self.keyboard.name == line.replace('keyboard: ', '').strip()
            if line == '--strains--\n':
                strains, pairs, hands = True, False, False
                continue
            if line == '--pairs--\n':
                strains, pairs, hands = False, True, False
                continue
            if line == '--hands--\n':
                strains, pairs, hands = False, False, True
                continue
            if strains:
                k, v = line.strip().split('-')
                self.strains[Key.from_repr(k)] = v
            if pairs:
                k1, k2, v = line.strip().split('-')
                self.pairs[Key.from_repr(k1), Key.from_repr(k2)] = v
            if hands:
                k, v = line.strip().split('-')
                self.hands[Key.from_repr(k)] = v
        self._validate()
        self.name = file

    def _to_file(self, file):
        with open(file, 'w') as out:
            out.write(f'keyboard: {self.keyboard.name}\n')
            out.write('--strains--\n')
            for k, v in self.strains.items():
                out.write(f'{k}-{v}\n')
            out.write('--pairs--\n')
            for k, v in self.pairs.items():
                out.write(f'{k[0]}-{k[1]}-{v}\n')
            out.write('--hands--\n')
            for k, v in self.hands.items():
                out.write(f'{k}-{v}\n')

    def __repr__(self):
        result = self.keyboard.render() + '\n'
        result += self.keyboard.render(self.strains) + '\n'
        result += self.keyboard.render(self.hands)
        return result

    def __format__(self, format):
        if format in ('full', 'left', 'right'):
            result = self.__repr__() + '\n'
            for k1 in self.keyboard.keys:
                if format == 'left' and self.hand(k1) == RIGHT:
                    continue
                if format == 'right' and self.hand(k1) == LEFT:
                    continue
                o_rep = self.keyboard.render({k: k if k == k1 else ' ' for k in self.keyboard.keys})
                key_dict = {}
                for k2 in self.keyboard.keys:
                    if (k1, k2) in self.pairs:
                        key_dict[k2] = self.pairs[(k1, k2)]
                    else:
                        key_dict[k2] = ' '
                d_rep = self.keyboard.render(key_dict)
                for o_line, d_line in zip(o_rep.split('\n'), d_rep.split('\n')):
                    result += o_line.strip() + d_line.strip() + '\n'
            return result
        return self.__repr__().__format__(format)



if __name__ == "__main__":
    pass
