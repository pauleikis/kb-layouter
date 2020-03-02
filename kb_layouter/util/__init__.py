from kb_layouter.criteria import Criterion, CriterionSuite
from kb_layouter.hands import Hands
from kb_layouter.keyboard import PLANCK
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
    keyboard = PLANCK
    hands = Hands(keyboard, 'planck.psi')

    return CriterionSuite(
        hands,
        [
            LtStrainCriterion,
            LtStretchCriterion,
            LtPlanckClumsynessCriterion,
            EnStrainCriterion,
            EnStretchCriterion,
            EnPlanckClumsynessCriterion,
            ColemakLikeShortcutsCriterion,
            # TirednessCriterion,
            # Qwertyness,
            Biased,
            # Vowels,
        ],
        weights=[
            1,
            2,
            2,
            1,
            2,
            2,
            2,
            2.5,
            # 2.5,
            # 1,
            # 1,
        ],
    )
