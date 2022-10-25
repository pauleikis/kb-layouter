import sys

from kb_layouter.keyboard import PLANCK, ANSI
from kb_layouter.keycaps import Keycaps
from kb_layouter.criteria.lang import (
    LtStrainCriterion,
    EnStrainCriterion,
    LtStretchCriterion,
    EnStretchCriterion,
    LtPlanckClumsynessCriterion,
    EnPlanckClumsynessCriterion,
    TirednessCriterion,
)
from kb_layouter.criteria.shortcuts import ColemakLikeShortcutsCriterion
from kb_layouter.evolution import Population
from kb_layouter.util import create_suite
from kb_layouter.config import MaskException


if __name__ == "__main__":
    # keyboard = ANSI
    suite = create_suite()

    mask = None
    # mask = "◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆"
    # mask = "X◆◆◆BQ◆◆◆" "O◆◆AJW◆◆◆◆" "ZCV◆GY◆"
    # mask = "X◆◆◆QY◆◆◆" "◆◆◆◆◆◆◆◆◆◆" "CZB◆GJ◆"
    # mask = "◆◆◆◆◆◆W◆◆" "V◆◆A◆◆I◆◆◆" "C◆◆O◆◆U"
    # mask = "Q◆◆◆◆◆◆◆◆" "◆◆◆◆◆◆◆◆◆◆" "ZXCV◆◆◆"
    mask = "◆L◆D◆◆◆Y◆" "RNST◆UOIEA" "ZXCV◆H◆"
    # mask = "X◆DHQFWPL" "VTSAGYIENR" "CZ◆OBJU"
    caps = []
    # caps = [Keycaps(keyboard, "planck:XDNGWQYMURTSABHOLEPZCVKFJI", mask=mask)]
    # caps = [Keycaps(keyboard, "planck:XDNJWQYKPRMSABGOLIUZCVTFHE", mask=mask)]
    # caps = [Keycaps(keyboard, "planck:QDNJXWYKURSLABPIMEHZCVTFGO", mask=mask)]
    # caps = [Keycaps(keyboard, "planck:XDMGQWHPURSTABJNIEKZCVOFYL", mask=mask)]
    # caps = [Keycaps(keyboard, "planck:XDNYQWBMUPSRAJGITELZCVOHFK", mask=mask)]
    # caps = [Keycaps(keyboard, "planck:XDNYQWBMUPTRAJGISELZCVOHFK", mask=mask)]
    # caps = [Keycaps(keyboard, "planck:QWFPBJLUYARSTGKNEIOZXCDVMH", mask=mask)]
    # caps = [Keycaps(keyboard, "planck:XDPFQWHLUKTSOGMINEYZCVABJR", mask=mask)]

    # if len(sys.argv) > 1 and sys.argv[1] == '--seed_file':
    #     caps = []
    #     print(f'Using seed file: {sys.argv[2]}')
    #     for line in open(sys.argv[2]):
    #         try:
    #             caps.append(Keycaps(keyboard, line.strip(), mask=mask))
    #             print(f'Seeding {line.strip()}')
    #         except MaskException:
    #             pass

    # keycaps = Keycaps(keyboard, 'planck:XMRFGQBOUNLSTDYIAEHZCVKJWP')
    # print(suite.summary(keycaps, detailed=True))

    # keycaps = Keycaps(keyboard, 'planck:QWERTYUIOASDFGHJKLPZXCVBNM')
    # print(suite.summary(keycaps, detailed=False))


    for i in range(10):
        p = Population(
            suite.evaluate,
            Keycaps.randomizer(suite.hands.keyboard, mask=mask),
            initial_size=50,
            seeded_keycaps=caps,
        )
        # print(p)
        # kc = p.evolve(silent=True)
        kc = p.evolve()
        with open('results.txt', 'a') as out:
            out.write(suite.summary(kc) + '\n')
        with open('ansi.seeds.txt', 'a') as out:
            out.write(f'{kc}\n')
        print(suite.summary(kc))

    # keycaps = Keycaps(keyboard, 'planck:QWFPBJLUYARSTGKNEIOZXCDVMH')
    # print(suite.summary(keycaps, detailed=True))
