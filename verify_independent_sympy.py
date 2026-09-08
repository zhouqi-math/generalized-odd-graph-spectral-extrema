"""Independent validation via Sturm root counts and trace linear equations."""
import sys, json
from pathlib import Path

import sympy as s
from collections import Counter
x=s.symbols('x')
stats=Counter()
survivors=[]
trace_candidates=[]

def powers(g):
    aa=g.all_coeffs()
    d=g.degree()
    ans=[d]
    for j in range(1,6):
        val=sum(aa[i]*ans[j-i] for i in range(1,min(j-1,d)+1))
        if j<=d:
            val += j*aa[j]
        ans.append(-val)
    return ans

for k in range(2,183):
    for mu in range(1,k):
        if k*(k-1)%mu: continue
        v2=k*(k-1)//mu
        for c in range(mu,k):
            if v2*(k-mu)%c: continue
            n=1+k+v2+v2*(k-mu)//c
            if 5*n>=117*k: continue
            stats['order_bound']+=1
            # Derive the polynomial from the matrix, independently of the
            # expanded cubic used by the primary certificate.
            L=s.Matrix([[0,k,0,0],[1,0,k-1,0],
                        [0,mu,0,k-mu],[0,0,c,k-c]])
            chi=L.charpoly(x).as_poly()
            f=chi.exquo(s.Poly(x-k,x))
            assert f.degree()==3 and s.gcd(f,f.diff()).degree()==0
            z=s.Rational(n,36)-k
            below=f.count_roots(-s.oo,z)-int(f.eval(z)==0)
            h=36*k-n
            d2=h*h-1296*k
            d3=h*(d2-1296*mu*(k-1))
            d4=(h+36*(k-c))*d3-1296*c*(k-mu)*d2
            assert (below==0)==(min(h,d2,d3)>0 and d4>=0)
            if below: continue
            stats['sturm_threshold']+=1
            ff=s.factor_list(f)[1]
            pp=[powers(g) for g,e in ff]
            A=s.Matrix([[p[j] for p in pp] for j in [0,1,2,3,5]])
            rhs=s.Matrix([n-1,-k,n*k-k*k,-k**3,-k**5])
            try:
                sol, parameters=A.gauss_jordan_solve(rhs)
            except ValueError:
                stats['inconsistent_traces']+=1
                continue
            assert not parameters.rows
            trace_candidates.append(dict(k=k,mu=mu,c=c,n=n,factors=[str(g.as_expr()) for g,e in ff],multiplicities=[str(m) for m in sol]))
            if not all(m.is_Integer and m>=k for m in sol):
                stats['invalid_multiplicities']+=1
                continue
            survivors.append([k,mu,c,n])
            stats['passed']+=1
assert survivors==[[2,1,1,7],[4,1,2,35],[7,2,3,64]]
report=dict(method='Sturm root counts and trace equations for powers 0,1,2,3,5',counts=dict(stats),survivors=survivors,trace_candidates=trace_candidates)
Path(__file__).with_name('independent_report.json').write_text(json.dumps(report,indent=2),encoding='utf8')
print(json.dumps(report,indent=2))
