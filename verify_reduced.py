"""Exact finite enumeration for the mathematical manuscript revision (2026-09-15).
Run with Python 3.8 or later; no external package is required.
The cycle case k=2 is settled by the proof, so enumeration starts at k=3.
"""
import json
from pathlib import Path

records = []
counts = dict(parameter_triples=0, integer_layers=0, order_bound=0,
              multiplicity_second_moment_bound=0, spectral_threshold=0,
              integer_nonprincipal_eigenvalue=0)
for k in range(3, 183):
    for mu in range(1, k):
        if k*(k-1) % mu:
            counts['parameter_triples'] += k-mu
            continue
        k2 = k*(k-1)//mu
        for c in range(mu, k):
            counts['parameter_triples'] += 1
            if k2*(k-mu) % c:
                continue
            k3 = k2*(k-mu)//c
            n = 1+k+k2+k3
            counts['integer_layers'] += 1
            if 5*n >= 117*k:
                continue
            counts['order_bound'] += 1
            bound = 3*k+c*c+2*mu*(k-c-1)
            if n <= bound:
                continue
            counts['multiplicity_second_moment_bound'] += 1
            h = 36*k-n
            d2 = h*h-36**2*k
            d3 = h*(d2-36**2*mu*(k-1))
            d4 = (h+36*(k-c))*d3-36**2*c*(k-mu)*d2
            if h <= 0 or d2 <= 0 or d3 <= 0 or d4 < 0:
                continue
            counts['spectral_threshold'] += 1
            a, b = mu*(c-k+1)-k, -c*(k-mu)
            roots = [r for r in range(1-k, k)
                     if r*r*r+c*r*r+a*r+b == 0]
            if not roots:
                continue
            counts['integer_nonprincipal_eigenvalue'] += 1
            records.append(dict(k=k,mu=mu,c=c,n=n,cubic=[b,a,c,1],
                                integer_roots=roots,minors=[h,d2,d3,d4]))
assert [(r['k'],r['mu'],r['c']) for r in records] == [
    (4,1,2),(6,2,3),(7,2,3),(8,2,3),(9,3,4)]
report = dict(arithmetic='integers only',counts=counts,candidates=records)
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n', encoding='utf-8')
print(json.dumps(report,indent=2))
