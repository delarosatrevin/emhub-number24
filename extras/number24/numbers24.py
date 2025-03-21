from collections import defaultdict
from itertools import permutations
import operator
import sys
import json
import os

here = os.path.abspath(os.path.dirname(__file__))


def div(a, b):
    return -9999 if b < a or b == 0 or a % b else a / b

operators = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': div }

total = 0
unique = defaultdict(list)


def revrange(m):
    return reversed(range(1, 10))


def uniq(s):
    return ''.join(str(x) for x in sorted(s, reverse=True))


def join(s):
    return ''.join(str(x) for x in s)


def solve_1x1(a, b):
    for label, op in operators.items():
        if op(a, b) == 24:
            return label
    return None


def solve_2x2(s):
    solutions = []
    for label1, op1 in operators.items():
        for label2, op2 in operators.items():
            a = op1(s[0], s[1])
            b = op2(s[2], s[3])
            op = solve_1x1(a, b)
            if op and a > 0 and b > 0:
                solutions.append(f"({s[0]} {label1} {s[1]}) {op} "
                                 f"({s[2]} {label2} {s[3]})")

            a = op1(s[0], s[1])
            b = op2(a, s[2])
            op = solve_1x1(b, s[3])
            if op and a > 0 and b > 0:
                sol = f"(({s[0]} {label1} {s[1]}) {label2} {s[2]}) {op} {s[3]}"
                solutions.append(sol)

            a = op1(s[1], s[2])
            b = op2(s[0], a)
            op = solve_1x1(b, s[3])
            if op and a > 0 and b > 0:
                sol = f"({s[0]} {label2} ({s[1]} {label1} {s[2]})) {op} {s[3]}"
                solutions.append(sol)


    return solutions


def solve(s, permute=False):
    if permute:
        alls = permutations(s)
    else:
        alls = [s]

    solutions = []
    for seq in alls:
        solutions.extend(solve_2x2(seq))
    return solutions


def uniqsols(solutions):
    uniqSols = set()
    for sol in solutions:
        if sol not in uniqSols:
            uniqSols.add(sol)
    return uniqSols


def printseq(s, permute=False):
    u = uniq(s)
    print(u, ":  ", s)
    solutions = solve(s, permute=permute)
    uniqSols = uniqsols(solutions)
    for sol in uniqSols:
        print("   ", sol)
    return len(uniqSols)


if __name__ == '__main__':

    n = len(sys.argv)

    if n == 1:
        sols = set()
        sequences = {}

        for i in revrange(10):
            for i2 in revrange(i):
                for i3 in revrange(i2):
                    for i4 in revrange(i3):
                        total += 1
                        s = [i, i2, i3, i4]
                        u = uniq(s)
                        unique[u].append(u)
                        if solutions := uniqsols(solve(s, permute=True)):
                            sol = e = next(iter(solutions))
                            print(u, ":  ", s, "sols: ", len(solutions), "first: ", sol)
                            sols.add(u)
                            sequences[u] = {'pts': 1, 'sols': [sol]}

        print("Total", total, "  Unique: ", len(unique), "Solutions: ", len(sols))

        with open(os.path.join(here, 'sequences.json'), 'w') as f:
            json.dump(sequences, f, indent=4)

    elif n == 5:
        s = [int(a) for a in sys.argv[1:]]
        print(sys.argv)
        print('s', s)
        printseq(s, permute=True)


else:
    raise Exception("Pass none or 4 arguments")
