from kb_layouter.criteria import Criterion
from kb_layouter.keycaps import Keycaps
from kb_layouter.hands import Hands
from kb_layouter.keyboard import ANSI
from kb_layouter.config import S, A, B, C, D, E, F, X

class Qwertyness(Criterion):
    qwerty = Keycaps(ANSI, 'planck:QWERTYUIOPASDFGHJKLZXCVBNM')
    qwerty_hands = Hands(ANSI, 'ansi.psi')

    def penalties(self, keycaps):
        result = {}
        for key, letter in keycaps.items():
            qw_key = self.qwerty.get_key(letter)
            if self.hands.hand(key) != self.qwerty_hands.hand(qw_key):
                result[letter] = F
            elif key.col != qw_key.col:
                result[letter] = D
            elif key.row != qw_key.col:
                result[letter] = B
            else:
                result[letter] = S
        return result

    @property
    def minimum(self):
        return S * 26

    @property
    def maximum(self):
        return F * 26
