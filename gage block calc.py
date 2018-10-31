def sizes(v, i, S, memo):
    if i >= len(v):
        return 1 if S == 0 else 0
    if (i, S) not in memo:
        count = sizes(v, i + 1, S, memo)
        count += sizes(v, i + 1, S - v[i], memo)
        memo[(i, S)] = count
    return memo[(i, S)]


def g(v, S, memo):
    subset = []
    for i, x in enumerate(v):
        if sizes(v, i + 1, S - x, memo) > 0:
            subset.append(x)
            S -= x
        return subset


blocks = [0.050, 0.100, 0.1001, 0.1002, 0.1003, 0.1004, 0.1005, 0.1006, 0.1007, 0.1008, 0.1009,
          0.101, 0.102, 0.103, 0.104, 0.105, 0.106, 0.107, 0.108, 0.109, 0.11, 0.111, 0.112,
          0.113, 0.114, 0.115, 0.116, 0.117, 0.118, 0.119, 0.12, 0.121, 0.122, 0.123, 0.124,
          0.125, 0.126, 0.127, 0.128, 0.129, 0.13, 0.131, 0.132, 0.133, 0.134, 0.135, 0.136,
          0.137, 0.138, 0.139, 0.14, 0.141, 0.142, 0.143, 0.144, 0.145, 0.146, 0.147, 0.148,
          0.149, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8,
          0.85, 0.9, 0.95, 1.0, 2.0, 3.0, 4.0]
v = [1, 2, 3, 10]

drop = 12
memo = dict()
if sizes(v, 0, drop, memo) == 0:
    print("there are no valid subset")
else:
    print(g(v, drop, memo))
