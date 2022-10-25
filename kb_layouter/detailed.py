import sys

from kb_layouter.keyboard import PLANCK, ANSI
from kb_layouter.hands import Hands
from kb_layouter.keycaps import Keycaps
from kb_layouter.criteria import Criterion, CriterionSuite
from kb_layouter.util import create_suite


def create_keycaps(keycaps):
    return Keycaps(ANSI, keycaps)

def main(suite, keycaps, detailed=True):
    return suite.summary(keycaps, detailed=detailed)
    # return suite.evaluate(keycaps)

if __name__ == "__main__":
    suite = create_suite()
    if sys.argv[1] == '--seed_file':
        best, minimum = None, 100000
        for line in map(str.strip, open(sys.argv[2])):
            # print(main(suite, create_keycaps(line), detailed=False))
            if (score := suite.evaluate(create_keycaps(line))) < minimum:
                best, minimum = create_keycaps(line), score
        print(main(suite, best))
    else:
        print(main(create_suite(), create_keycaps(sys.argv[1])))
