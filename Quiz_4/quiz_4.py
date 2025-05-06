from functools import reduce
import operator

def add(*args):
    return reduce(lambda x, y: operator.add(x, y), args)

def sub(*args):
    return reduce(lambda x, y: operator.sub(x, y), args)

def ra_sub(*args):
    return reduce(lambda x, y: operator.sub(y, x), reversed(args))

print(add(12, 5, 4))  # 21
print(sub(12, 5, 4))  # 3
print(ra_sub(12, 5, 4))  # 11

def zip(*sequences):
    if not all(sequences):
        return []

    firsts = list(map(lambda seq: seq[0], sequences))
    others = list(map(lambda seq: seq[1:], sequences))

    return [firsts] + zip(*others)
   
print(zip([0, .1, .2], [30, 40, 50], [66, 77, 88]))

def zipwith(f, *sequences):
    if not all(sequences):
        return []

    firsts = list(map(lambda seq: seq[0], sequences))
    others = list(map(lambda seq: seq[1:], sequences))

    return [f(*firsts)] + zipwith(f, *others)

print(zipwith(add, [0, .1, .2], [30, 40, 50], [66, 77, 88]))

def flatten(tree):
    return reduce(lambda a, b: a + (flatten(b) if isinstance(b, list) else [b]), tree, [])

print(flatten([0, [1, [2, [3, 4], [5, [6, 7]], 8], [9], 10]]))

def group_by(f, sequence):
    return reduce(lambda a, b: {**a, f(b): a.get(f(b), []) + [b]}, sequence, {})

print(group_by(len, ["hand", "elbow", "arm", "chest", "foot", "knee", "leg"]))
