from collections import defaultdict
from itertools import permutations
import operator
import sys
import json
import os

here = os.path.abspath(os.path.dirname(__file__))


class Op:
    def __init__(self, label, op):
        self._label = label
        self._op = op

    def __str__(self):
        return self._label

    def __repr__(self):
        return self._label

    def __call__(self, *args, **kwargs):
        return self._op(*args)

    @property
    def commutative(self):
        return self._label in ['+', '*']


class Expr:
    def __init__(self, val1, op=None, val2=None):
        """ Can be unary or binary expression. """
        self._v1 = val1
        self._op = op
        self._v2 = val2

    @property
    def isbinary(self):
        return self._op is not None

    def __str__(self):
        if self.isbinary:
            return f"({self._v1} {self._op} {self._v2})"
        else:
            return str(self._v1)

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(str(self))

    def equivalent(self, other):
        try:
            if self._op == other._op:
                if self._op is None:
                    return self._v1 == other._v1

                if self._v1.equivalent(other._v1) and self._v2.equivalent(other._v2):
                    return True
                if self._op.commutative and self._v1.equivalent(other._v2) and self._v2.equivalent(other._v1):
                    return True
        except:
            print('self', str(self), 'other', other)
            raise
        return False

    @property
    def module(self):
        if self.isbinary:
            return self._v1.module + self._v2.module + self.value
        return self._v1

    @property
    def value(self):
        if self.isbinary:
            return self._op(self._v1.value, self._v2.value)
        return self._v1


def div(a, b):
    return -9999 if (b == 0 or a % b != 0) else a // b


operatorDict = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': div}
operators = [Op(label, op) for label, op in operatorDict.items()]

DATA = {1: [["1", "2", "3", "4"], ["8", "8", "7", "3"], ["1", "9", "5", "5"], ["1", "1", "4", "4"],
        ["1", "1", "5", "6"], ["3", "3", "5", "6"], ["8", "8", "4", "9"], ["2", "2", "4", "6"], ["3", "9", "9", "7"],
        ["2", "2", "8", "6"], ["9", "3", "6", "6"], ["2", "3", "5", "9"], ["1", "4", "8", "8"], ["1", "5", "8", "8"],
        ["6", "3", "6", "6"], ["4", "8", "5", "7"], ["3", "3", "4", "8"], ["1", "1", "4", "8"], ["3", "7", "7", "7"],
        ["1", "2", "6", "6"], ["3", "4", "5", "5"], ["3", "8", "8", "8"], ["3", "4", "6", "8"], ["4", "4", "8", "8"],
        ["3", "9", "9", "9"], ["1", "1", "2", "9"], ["2", "4", "8", "8"], ["1", "2", "4", "4"], ["1", "5", "7", "8"],
        ["5", "5", "7", "7"], ["1", "8", "7", "9"], ["6", "6", "6", "6"], ["1", "2", "5", "9"], ["4", "4", "5", "8"],
        ["2", "3", "3", "6"], ["4", "6", "7", "7"], ["1", "6", "8", "9"], ["1", "2", "5", "8"], ["1", "7", "8", "8"],
        ["1", "2", "6", "8"], ["5", "6", "6", "7"], ["2", "4", "4", "8"], ["1", "4", "5", "5"], ["4", "6", "6", "8"],
        ["3", "4", "5", "7"], ["1", "3", "3", "4"], ["1", "1", "4", "7"], ["1", "2", "2", "7"]],
        2: [["3", "5", "6", "7"], ["1", "4", "9", "7"], ["4", "7", "8", "8"], ["2", "4", "6", "6"], ["1", "2", "9", "6"],
        ["5", "6", "7", "8"], ["1", "5", "7", "9"], ["1", "3", "5", "9"], ["1", "5", "6", "8"], ["1", "2", "4", "9"],
        ["2", "2", "2", "5"], ["1", "3", "9", "3"], ["2", "3", "4", "6"], ["4", "5", "7", "7"], ["3", "3", "3", "9"],
        ["1", "2", "8", "8"], ["4", "4", "5", "6"], ["1", "6", "7", "9"], ["1", "1", "6", "9"], ["2", "4", "4", "4"],
        ["3", "3", "4", "5"], ["2", "3", "4", "4"], ["1", "4", "4", "9"], ["5", "6", "6", "8"], ["3", "5", "5", "7"],
        ["4", "4", "4", "9"], ["2", "3", "3", "8"], ["2", "2", "4", "7"], ["6", "8", "8", "8"], ["4", "5", "8", "9"],
        ["2", "7", "3", "6"], ["2", "2", "6", "7"], ["1", "3", "5", "6"], ["2", "4", "6", "7"], ["1", "3", "6", "8"],
        ["1", "3", "5", "8"], ["4", "4", "4", "5"], ["2", "3", "5", "6"], ["2", "6", "7", "9"], ["3", "4", "8", "9"],
        ["2", "2", "3", "6"], ["1", "3", "6", "6"], ["3", "4", "9", "9"], ["4", "5", "6", "9"], ["3", "4", "5", "9"],
        ["2", "5", "6", "8"], ["2", "2", "4", "8"], ["7", "8", "8", "9"]],
        3: [["2", "3", "7", "9"], ["2", "2", "5", "7"], ["2", "4", "7", "9"], ["2", "3", "6", "8"], ["1", "2", "2", "8"],
        ["4", "4", "8", "5"], ["2", "6", "8", "9"], ["3", "5", "9", "9"], ["1", "4", "6", "9"], ["5", "8", "8", "8"],
        ["2", "2", "2", "7"], ["1", "4", "5", "8"], ["2", "5", "6", "9"], ["6", "7", "9", "9"], ["3", "4", "7", "7"],
        ["2", "2", "5", "9"], ["3", "3", "5", "7"], ["3", "3", "3", "5"], ["2", "5", "5", "8"], ["4", "8", "9", "9"],
        ["2", "2", "6", "9"], ["1", "3", "8", "8"], ["5", "8", "8", "9"], ["3", "3", "6", "8"], ["2", "5", "7", "9"],
        ["2", "3", "8", "9"], ["5", "6", "6", "9"], ["5", "7", "8", "9"], ["2", "7", "8", "9"], ["4", "4", "8", "9"],
        ["1", "3", "4", "8"], ["4", "5", "9", "9"], ["1", "4", "6", "7"], ["2", "2", "3", "5"], ["1", "4", "6", "8"],
        ["1", "2", "4", "5"], ["3", "5", "7", "9"], ["3", "4", "4", "9"], ["4", "5", "5", "7"], ["5", "7", "8", "8"],
        ["1", "4", "6", "6"], ["2", "4", "5", "5"], ["3", "5", "8", "9"], ["2", "3", "5", "7"], ["2", "3", "8", "6"],
        ["4", "7", "7", "7"], ["3", "4", "4", "4"], ["3", "3", "6", "6"]]}




def revrange(m):
    return reversed(range(1, 10))


def uniq(s):
    return ''.join(str(x) for x in sorted(s, reverse=True))


def join(s):
    return ''.join(str(x) for x in s)


def solve_1x1(a, b):
    for op in operators:
        if op(a, b) == 24:
            return op
    return None


def solve_2x2(sequence):
    solutions = []
    s1, s2, s3, s4 = sequence
    e1, e2, e3, e4 = [Expr(s) for s in sequence]

    for op1 in operators:
        for op2 in operators:
            a = op1(s1, s2)
            b = op2(s3, s4)
            if a >= 0 and b >= 0:
                if op := solve_1x1(a, b):
                    solutions.append(Expr(
                        Expr(e1, op1, e2), op, Expr(e3, op2, e4)
                    ))
                    # solutions.append(f"({s[0]} {label1} {s[1]}) {op} "
                    #                  f"({s[2]} {label2} {s[3]})")

            b = op2(a, s3)
            if a >= 0 and b >= 0:
                if op := solve_1x1(b, s4):
                    solutions.append(Expr(
                        Expr(Expr(e1, op1, e2), op2, e3), op, e4
                    ))
                    # sol = f"(({s[0]} {label1} {s[1]}) {label2} {s[2]}) {op} {s[3]}"
                    # solutions.append(sol)

            a = op1(s2, s3)
            b = op2(s1, a)
            if a >= 0 and b >= 0:
                if op := solve_1x1(b, s4):
                    solutions.append(Expr(
                        Expr(e1, op2, Expr(e2, op1, e3)), op, e4
                    ))
                    # sol = f"({s[0]} {label2} ({s[1]} {label1} {s[2]})) {op} {s[3]}"
                    # solutions.append(sol)

            b = op2(a, s4)
            if a >= 0 and b >= 0:
                if op := solve_1x1(s1, b):
                    solutions.append(Expr(e1, op, Expr(Expr(e2, op1, e3), op2, e4)))

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
    sols = []
    for s in solutions:
        if not any(s.equivalent(s2) for s2 in sols):
            sols.append(s)

    return sols


def printseq(s, permute=False):
    u = uniq(s)
    print(u, ":  ", s)
    solutions = solve(s, permute=permute)
    uniqSols = uniqsols(solutions)
    for sol in uniqSols:
        print("   ", sol)
    print("Total: ", len(solutions), "Uniq: ", len(uniqSols))


if __name__ == '__main__':

    n = len(sys.argv)

    if n == 1:
        sols = set()
        sequences = {}
        seqs = []

        total = 0
        total_uniq = 0
        bins = defaultdict(lambda : 0)

        for i in revrange(10):
            for i2 in revrange(i):
                for i3 in revrange(i2):
                    for i4 in revrange(i3):
                        total += 1
                        s = [i, i2, i3, i4]
                        u = uniq(s)
                        if u in sequences:
                            continue
                        total_uniq += 1
                        if solutions := uniqsols(solve(s, permute=True)):
                            sol = solutions[0]
                            mod = sol.module
                            for s in solutions[1:]:
                                if s.module < mod:
                                    sol = s
                                    mod = s.module
                            ssol = str(sol)
                            mod -= 40
                            b = mod // 10
                            bins[b] += 1
                            #print(u, ":  ", s, "sols: ", len(solutions), "first: ", ssol, "module: ", mod)
                            seqStr = f"{u}: {s}, sols: {len(solutions)}, first: {ssol}, mod: {mod}"
                            sols.add(u)
                            seqs.append({
                                'u': u,
                                'str': seqStr,
                                'mod': mod,
                                'sols': len(solutions)
                            })
                            if mod >= 20:
                                pts = 3
                            elif mod > 9:
                                pts = 2
                            else:
                                pts = 1
                            sequences[u] = {'pts': pts, 'sols': [str(s) for s in solutions], 'sol': ssol, 'mod': mod}

        for s in sorted(seqs, key=lambda s: s['mod'], reverse=False):
            print(s['str'])

        for pts, lst in DATA.items():
            for seq in lst:
                u = uniq(seq)
                if u not in sequences:
                    print("Missing: ", u)

        for i in range(20):
            a = i * 10
            b = a + 9
            print(f"{a} - {b}: {bins[i]}")

        print("Total", total, "  Unique: ", total_uniq, "Solutions: ", len(sols))

        with open(os.path.join(here, 'sequences.json'), 'w') as f:
            json.dump(sequences, f, indent=4)

    elif n == 5:
        s = [int(a) for a in sys.argv[1:]]
        print(sys.argv)
        print('s', s)
        printseq(s, permute=True)

    else:
        raise Exception("Pass none or 4 arguments")
