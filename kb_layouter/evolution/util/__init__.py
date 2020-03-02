from statistics import stdev
from math import exp
import random

def weighted_choice(seq, weights):
    assert len(weights) == len(seq), f'{len(weights)}, {len(seq)}'
    assert abs(1. - sum(weights)) < 1e-6
    x = random.random()
    for elmt, weight in zip(seq, weights):
        if x <= weight:
            return elmt
        x -= weight

def softmax(seq, t):
    if t < 0:
        adj = min(seq)
    else:
        adj = max(seq)

    zs = [exp((1/t) * (e - adj)) for e in seq]
    sum_z = sum(zs)
    return [z / sum_z for z in zs]

# def soft_choices(seq, t, k=1, weight_func=lambda x: x):
#     seq = list(seq)
#     assert len(seq) >= k
#     result = []
#     for _ in range(k):
#         choice = weighted_choice(seq, softmax(list(map(weight_func, seq)), t))
#         result.append(choice)
#         seq.remove(choice)
#     return result

def soft_random_generator(seq, t, weight_func=None):
    if weight_func is None:
        soft_distribution = softmax(seq, t)
    else:
        soft_distribution = softmax(list(map(weight_func, seq)), t)
    while True:
        yield weighted_choice(seq, soft_distribution)

if __name__ == '__main__':
    t = -100
    print(softmax([100, 200, 300], t))
    print(softmax([10, 20, 30], t))
    print(softmax([.1, .2, .3], t))
    print()
    print(softmax([1, 2, 3], t))
    print(softmax([11, 12, 13], t))
    print(softmax([-1, 0, 1], t))
    print(softmax([-9, 1, 11], t))
    print()
    print('(╯°□°）╯︵ ┻━┻')

    print(softmax([10, 20, 30, 30, 30, 30, 30], t))
