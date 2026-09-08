"""Check the three constructions directly, using only Python's standard library."""
from collections import deque
from pathlib import Path
import json


def distances(adj, root):
    dist = {root: 0}
    queue = deque([root])
    while queue:
        v = queue.popleft()
        for w in adj[v]:
            if w not in dist:
                dist[w] = dist[v]+1
                queue.append(w)
    return dist


def intersection_array(adj):
    n, k = len(adj), len(adj[0])
    assert all(len(neighbors) == k for neighbors in adj)
    parameters = {}
    layers = None
    for root in range(n):
        d = distances(adj, root)
        assert len(d) == n and max(d.values()) == 3
        sizes = [sum(a == i for a in d.values()) for i in range(4)]
        if layers is None:
            layers = sizes
        assert layers == sizes
        for v in range(n):
            i = d[v]
            local = tuple(sum(d[w] == j for w in adj[v]) for j in (i-1,i,i+1))
            parameters.setdefault(i, local)
            assert parameters[i] == local
    return {'layers': layers, 'c_a_b': [parameters[i] for i in range(4)]}


def left_multiply(adj, mat):
    n = len(adj)
    return [[sum(mat[w][j] for w in adj[i]) for j in range(n)] for i in range(n)]


def verify(name, adj, expected_layers, expected_cab, roots_polynomial):
    n = len(adj)
    assert all(v not in adj[v] for v in range(n))
    assert all(v in adj[w] for v in range(n) for w in adj[v])
    actual = intersection_array(adj)
    assert actual['layers'] == expected_layers
    assert actual['c_a_b'] == expected_cab
    ident = [[int(i == j) for j in range(n)] for i in range(n)]
    power, traces = ident, [n]
    for exponent in range(1,8):
        power = left_multiply(adj, power)
        traces.append(sum(power[i][i] for i in range(n)))
    assert all(traces[i] == 0 for i in (1,3,5)) and traces[7] > 0
    p = [[roots_polynomial[-1]*int(i==j) for j in range(n)] for i in range(n)]
    for a in reversed(roots_polynomial[:-1]):
        p = left_multiply(adj, p)
        for i in range(n):
            p[i][i] += a
    assert not any(any(row) for row in p)
    return dict(name=name,n=n,valency=len(adj[0]),diameter=3,odd_girth=7,
                intersection_checks=actual,traces_0_to_7=traces,
                annihilating_polynomial=roots_polynomial,
                polynomial_of_adjacency_is_zero=True)


def main():
    c7 = [{(i-1)%7, (i+1)%7} for i in range(7)]
    subsets = [x for x in range(128) if bin(x).count('1') == 3]
    o4 = [{j for j,y in enumerate(subsets) if not x&y} for x in subsets]
    fq7 = []
    for x in range(64):
        neighbors = set()
        for i in range(7):
            y = x^(1<<i)
            neighbors.add(min(y,y^127))
        fq7.append(neighbors)
    report = [
        verify('C7',c7,[1,2,2,2],[(0,0,2),(1,0,1),(1,0,1),(1,1,0)],
               [2,3,-4,-1,1]),
        verify('O4 = KG(7,3)',o4,[1,4,12,18],[(0,0,4),(1,0,3),(1,0,3),(2,2,0)],
               [24,14,-13,-2,1]),
        verify('Folded 7-cube',fq7,[1,7,21,35],[(0,0,7),(1,0,6),(2,0,5),(3,4,0)],
               [105,76,-34,-4,1])]
    path = Path(__file__).with_name('construction_report.json')
    path.write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    main()
