from collections import namedtuple

from kb_layouter.config import PATH_TO_DATA

class Key(namedtuple('Key', ['row', 'col'])):
    __slots__ = ()
    def __repr__(self):
        return f'{self.row}{self.col:02d}'

    def __format__(self, format):
        return self.__repr__().__format__(format)

    @classmethod
    def from_repr(cls, repr):
        return cls(row=int(repr[:1]), col=int(repr[1:]))

class Keyboard:
    key_placeholder = 'TTT'

    def __init__(self, name=None):
        self.name = name
        self._template, self._keys = self._parse(PATH_TO_DATA / 'keyboards' / f'{name}.txt')

    @property
    def keys(self):
        return self._keys

    def render(self, keys=None, format=None, name=None):
        if keys is None:
            keys = {k: k for k in self.keys}

        template = self._template
        if format is not None:
            template = template.replace(f'{{:^{len(self.key_placeholder)}}}', f'{{:{format}}}')
        result = template.format(*(keys[k] for k in self.keys))
        if name:
            result += '\n Keyboard: ' + self.name if name is True else name
        return result

    def _parse(self, file):
        with open(file) as inp:
            contents = inp.read()

            template = contents.rstrip().replace(self.key_placeholder, f'{{:^{len(self.key_placeholder)}}}')
            result = []
            idx = 0
            for row in contents.split('\n'):
                if not self.key_placeholder in row:
                    continue
                result += [Key(idx, col) for col in range(row.count(self.key_placeholder))]
                idx += 1
            return template, tuple(result)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._template == other._template and self._keys == other._keys
        return False

    def __hash__(self):
        return hash((self._template, self._keys))

try:
    PLANCK = Keyboard('planck')
except Exception:
    PLANCK = None

try:
    ANSI = Keyboard('ansi')
except Exception:
    ANSI = None
