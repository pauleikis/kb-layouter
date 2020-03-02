import sys
from collections import Counter
from itertools import combinations, permutations

def pred(a):
    return any(x in a for x in 'O')

def main(path):
    res = Counter()
    analy = set('TESNRLMDHCVPKHAOUIW')
    for line in open(path):
        ngram, freq = line.split()
        if not (set(ngram) < analy) or len(set(ngram)) != len(ngram):
            continue
        if not pred(ngram):
            continue
        freq = float(freq)
        key = ''.join(sorted(ngram))

        res[key] += freq

    for lt in combinations(sorted(analy), 2):
    # for lt in permutations(sorted(analy), 3):
        if not pred(lt):
            continue
        res[''.join(lt)] += 0

    print(res.most_common()[-10:])


if __name__ == "__main__":
    main(sys.argv[1])
