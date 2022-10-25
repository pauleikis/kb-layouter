from kb_layouter.criteria import Criterion, CriterionSuite
from kb_layouter.hands import Hands
from kb_layouter.keyboard import PLANCK, ANSI
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
from kb_layouter.criteria.similarity import Qwertyness
from kb_layouter.criteria.restrictions import Biased, Vowels

def create_suite():
    keyboard = ANSI
    hands = Hands(keyboard, 'ansi.psi')

    return CriterionSuite(
        hands,
        [
            LtStrainCriterion,
            LtStretchCriterion,
            LtPlanckClumsynessCriterion,
            EnStrainCriterion,
            EnStretchCriterion,
            EnPlanckClumsynessCriterion,
            # ColemakLikeShortcutsCriterion,
            # TirednessCriterion,
            # Qwertyness,
            # Biased,
            # Biased2,
            # Vowels,
        ],
        weights=[
            1.1,
            1.9,
            .95,
            1.1,
            1.9,
            .95,
            # 2,
            # 2,
            # 1.5,
            # 2.2,
            # 1,
            # 1.7,
        ],
    )
