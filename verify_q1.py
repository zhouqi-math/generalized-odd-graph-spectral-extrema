"""Exact certificate for the spectral-extremum manuscript (Python >= 3.8).

No third-party packages, floating-point arithmetic, graph databases, or network
access are used. Polynomial coefficients are stored in ascending degree order.
Run: python verify_q1.py
"""
from fractions import Fraction as F
from math import isqrt
from collections import Counter
from pathlib import Path
import csv
import json


def trim(p):
    p = list(p)
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p


def divide(p, q):
    p, q = list(map(F, p)), trim(list(map(F, q)))
    if q == [0]:
        raise ZeroDivisionError('zero polynomial')
    out = [F(0)] * max(1, len(p) - len(q) + 1)
    while len(p) >= len(q) and p != [0]:
        j, a = len(p) - len(q), p[-1] / q[-1]
        out[j] = a
        for i, b in enumerate(q):
            p[i+j] -= a*b
        p = trim(p)
    return trim(out), p


def evaluate(p, z):
    ans = 0
    for a in reversed(p):
        ans = ans*z + a
    return ans


def factors(f, k):
    """Factor the monic cubic over Q. All its roots lie in [-k,k]."""
    for r in range(-k, k+1):
        if evaluate(f, r) == 0:
            q, rem = divide(f, [-r, 1])
            assert rem == [0] and all(a.denominator == 1 for a in q)
            q = list(map(int, q))
            disc = q[1]**2 - 4*q[0]
            assert disc > 0
            root = isqrt(disc)
            if root*root == disc:
                assert (-q[1]+root) % 2 == 0
                u, v = (-q[1]+root)//2, (-q[1]-root)//2
                assert len({r, u, v}) == 3
                return [[-r, 1], [-u, 1], [-v, 1]]
            return [[-r, 1], q]
    return [f]


def multiplicities(k, mu, c, n):
    a, b = mu*(c-k+1)-k, -c*(k-mu)
    f = [b, a, c, 1]
    # chi=(x-k)f; cofactor is the (0,0) resolvent numerator.
    chi_prime = [b-k*a, 2*(a-k*c), 3*(c-k), 4]
    cofactor = [(k-c)*mu*(k-1), -mu*(k-1)-c*(k-mu), c-k, 1]
    out = []
    for g in factors(f, k):
        dp = divide(chi_prime, g)[1]
        cp = divide([n*a for a in cofactor], g)[1]
        size = max(len(dp), len(cp))
        dp += [F(0)]*(size-len(dp))
        cp += [F(0)]*(size-len(cp))
        assert any(dp), 'intersection eigenvalues must be simple'
        j = next(i for i, a in enumerate(dp) if a)
        m = cp[j]/dp[j]
        if any(m*a != b for a, b in zip(dp, cp)):
            return None, 'nonconstant_conjugate_multiplicity'
        if m.denominator != 1:
            return None, 'noninteger_multiplicity'
        if m < k:
            return None, 'multiplicity_below_valency'
        out.append({'factor': g, 'multiplicity': int(m)})
    assert 1 + sum((len(z['factor'])-1)*z['multiplicity'] for z in out) == n
    return out, 'passed'


def certificate(M, limit, order_numerator, order_denominator):
    count = Counter()
    survivors, audit = [], []
    scale = M*M
    for k in range(2, limit+1):
        for mu in range(1, k):
            for c in range(mu, k):
                count['parameter_triples'] += 1
                if k*(k-1) % mu:
                    continue
                k2 = k*(k-1)//mu
                if k2*(k-mu) % c:
                    continue
                k3 = k2*(k-mu)//c
                n = 1+k+k2+k3
                count['integer_layers'] += 1
                if order_denominator*n >= order_numerator*k:
                    continue
                count['order_bound'] += 1
                h = M*k-n
                d2 = h*h-scale*k
                d3 = h*(d2-scale*mu*(k-1))
                d4 = (h+M*(k-c))*d3-scale*c*(k-mu)*d2
                if min(h, d2, d3) <= 0 or d4 < 0:
                    continue
                count['spectral_threshold'] += 1
                ms, reason = multiplicities(k, mu, c, n)
                audit.append((k, mu, c, n, h, d2, d3, d4, reason))
                count[reason] += 1
                if ms is not None:
                    survivors.append(dict(k=k, mu=mu, c=c, n=n,
                                          layers=[1,k,k2,k3], factors=ms))
    return {'threshold': f'1/{M}', 'maximum_valency': limit,
            'counts': dict(count), 'survivors': survivors}, audit


def exact_auxiliary_checks():
    # These are the exact inequalities used in the two valency reductions.
    r = F(7,20)
    assert r**3*(35-36*r) == F(2401,2500) < 1
    assert (35-36*r)/r**2 == F(8960,49) < 183
    r = F(9,25)
    assert r**3*(34-35*r) == F(78003,78125) < 1
    assert (34-35*r)/r**2 == F(13375,81) < 166
    # The smallest C7 eigenvalue lies between these two rational numbers.
    c7 = [-1,-2,1,1]
    left, right = F(-65,36), F(-9,5)
    assert evaluate(c7,left) < 0 < evaluate(c7,right)
    return {'C7_polynomial_at_minus_65_over_36': str(evaluate(c7,left)),
            'C7_polynomial_at_minus_9_over_5': str(evaluate(c7,right))}


def main():
    main_report, audit = certificate(36, 182, 117, 5)
    focused_report, _ = certificate(35, 165, 112, 5)
    actual = {(r['k'], r['mu'], r['c']) for r in main_report['survivors']}
    assert actual == {(2,1,1), (4,1,2), (7,2,3)}, actual
    assert {(r['k'],r['mu'],r['c']) for r in focused_report['survivors']} == {
        (4,1,2), (7,2,3)}
    report = {'arithmetic': 'integers and fractions only', 'dependencies': [],
              'main_certificate': main_report, 'focused_certificate': focused_report,
              'auxiliary_checks': exact_auxiliary_checks()}
    dest = Path(__file__).resolve().parent
    (dest/'verification_report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
    with (dest/'candidate_audit.csv').open('w',newline='',encoding='utf8') as stream:
        writer=csv.writer(stream)
        writer.writerow(['k','mu','c','n','D1','D2','D3','D4','multiplicity_test'])
        writer.writerows(audit)
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    main()
