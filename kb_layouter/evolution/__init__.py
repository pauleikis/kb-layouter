from collections.abc import Sequence
from itertools import islice
import random

from kb_layouter.config import CRITERION_MIN, CRITERION_MAX
from kb_layouter.evolution.util import soft_random_generator

class Population:

    def __init__(
        self,
        evaluate,
        generate_random,
        seeded_keycaps=None,
        initial_size=50,
    ):
        self.evaluate = evaluate
        self.generate_random = generate_random
        self.initial_size = initial_size
        self.population = self.init_population(seeded_keycaps)

    def init_population(self, seeded_keycaps):
        result = []
        if seeded_keycaps:
            if isinstance(seeded_keycaps, Sequence):
                result += seeded_keycaps
            else:
                result.append(seeded_keycaps)
        result += [self.generate_random() for _ in range(self.initial_size - len(result))]
        return sorted(result, key=self.evaluate)[:self.initial_size]

    def evolve(self, silent=False):
        best_score = self.evaluate(self.population[0])
        idx = 0
        checkpoint = idx
        while len(self.population) > 1:
            self.step()
            # if not silent:
            print(
                f"{idx:>5} "
                f"- pool size: {len(self.population):>3} "
                f"- best: {self.evaluate(self.population[0]):8,.2f} "
                f"- worst: {self.evaluate(self.population[-1]):8,.2f} "
                f"- temperature: {self._t:8,.2f}",
                end="\r"
            )
            candidate_score = self.evaluate(self.population[0])
            if candidate_score < best_score:
                best_score = candidate_score
                checkpoint = idx
                if not silent:
                    print(" " * 100, end="\r")
                    print(f'{idx} - pool size: {len(self.population):>3}')
                    print(f'{self.population[0]:full}')
            if idx - ((self.initial_size + 10) / (len(self.population) + 10)) ** 3 > checkpoint:
                checkpoint = idx
                self.population = self.population[:-1]
            idx += 1
        # if not silent:
        print(" " * 100, end="\r")
        return self.population[0]

    def step(self):
        op_count = len(self.population) + 10
        pop_generator = soft_random_generator(
            self.population,
            self._t,
            weight_func=self.evaluate
        )
        offsprings = []
        for m, f in islice(zip(pop_generator, pop_generator), op_count):
            offsprings.append((m @ f) >> max(2, int(op_count ** .5)))
        for x in islice(pop_generator, op_count):
            offsprings.append(m >> random.randint(max(1, int((op_count - 10) ** .4)), max(2, int(op_count ** .5))))

        self.population = sorted(
            set(self.population + offsprings),
            key=self.evaluate
        )[:len(self.population)]


    @property
    def _t(self):
        result = -(len(self.population) - 2) ** 2
        # -2 to have temperature depend only on CRITERION_MIN at pop size 2

        result *= (CRITERION_MAX - CRITERION_MIN) ** 2
        result /= (self.initial_size ** 2)
        result -= CRITERION_MIN ** 2
        return result / 10

    def __repr__(self):
        result = ''
        for pop in self.population:
            result += f'{pop}: {self.evaluate(pop):>7.2f}\n'
        return result

    def __format__(self, format):
        return self.__repr__().__format__(format)
