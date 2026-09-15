# Spectral extrema in generalized odd graphs

Computational materials accompanying **Spectral bipartiteness in generalized odd graphs of diameter three**, by Qi Zhou.

Repository: https://github.com/zhouqi-math/generalized-odd-graph-spectral-extrema

## Mathematical revision of 15 September 2026

The revised proof isolates one finite calculation. All multiplicity restrictions, the final exclusions, graph constructions, uniqueness arguments, seven-cycle counts, and maximum-cut results are proved in the manuscript.

The required certificate is `verify_reduced.py`. It lists the five parameter triples in Lemma 3.1. The cycle case is proved separately, so its loop starts at valency 3. No external Python package is required.

```text
python verify_reduced.py
```

Use Python 3.8 or later, with assertions enabled (without `-O` or `PYTHONOPTIMIZE`). The command prints its report and writes `verify_reduced.json` beside the script. The expected report is supplied at `expected/verify_reduced.json`. Compare parsed JSON objects; line-ending differences are immaterial. Running the script again replaces only its generated report.

The program uses integer arithmetic for the following mathematically derived necessary conditions:

- `3 <= k <= 182` and `1 <= mu <= c < k`;
- integral distance layers `k2 = k(k-1)/mu`, `k3 = k2(k-mu)/c`;
- the order bound `5n < 117k`;
- the strict simultaneous multiplicity bound `n > 3k + c^2 + 2mu(k-c-1)` (equality corresponds to the separately handled cycle);
- the four tridiagonal determinant signs equivalent to the spectral threshold `sigma >= 1/36`;
- an integer root in `(-k,k)` of the nonprincipal cubic.

The last condition follows from the manuscript's proof that an irreducible cubic is possible only for the cycle. The script does not assume that the integer root is -1.

| Stage | Count |
|---|---:|
| Parameter triples with k >= 3 | 1,004,730 |
| Integral distance layers | 21,833 |
| Order bound | 5,777 |
| Strict simultaneous multiplicity bound | 204 |
| Spectral threshold | 17 |
| Integer nonprincipal eigenvalue | 5 |

The five output rows are:

| (k, mu, c) | n | Nonprincipal cubic |
|---|---:|---|
| (4,1,2) | 35 | (z+1)(z-2)(z+3) |
| (6,2,3) | 42 | (z+1)(z^2+2z-12) |
| (7,2,3) | 64 | (z+1)(z-3)(z+5) |
| (8,2,3) | 93 | (z+1)(z^2+2z-18) |
| (9,3,4) | 70 | (z+1)(z^2+3z-24) |

The report also records each cubic in ascending coefficient order, its integer roots, and all four exact leading minors. The final assertion checks the computed list after enumeration; it does not restrict the loop to those five rows.

The manuscript proves that a graph in this class with eigenvalue -1 must have an entirely integral spectrum. The nonsquare quadratic discriminants 52, 76, and 105 therefore eliminate three rows by a short trace argument. The remaining arrays give the Odd graph O4 and the folded 7-cube; adding the separately proved C7 case gives the three extremal graphs. The finite parameter test alone is not an existence proof.

## Earlier certificate and optional checks

The earlier proof materials and their reference outputs are preserved unchanged. Release [v1.0.0](https://github.com/zhouqi-math/generalized-odd-graph-spectral-extrema/releases/tag/v1.0.0) reproduces the original certificate.

| File | Role in the earlier package |
|---|---|
| `verify_q1.py` | Exact factorization, resolvent residues, and principal-minor tests for the original 1,665 threshold candidates |
| `verify_independent_sympy.py` | Optional independent Sturm and trace-equation verification |
| `verify_constructions.py` | Optional direct checks of the three graph constructions |
| `run_all.py` | Runs the earlier programs and compares their outputs with their unchanged expected reports |
| `requirements.txt` | Optional SymPy dependency for the earlier independent verification |

These are supplementary historical checks. They are not required to reproduce Lemma 3.1 in the revised mathematical proof, and `run_all.py` does not invoke `verify_reduced.py`.

The original standard-library checks can still be run with `python run_all.py`. To run all historical checks, install the optional dependency using `python -m pip install -r requirements.txt`, then run `python run_all.py --with-independent`. The historical main counts are 1,004,731 -> 21,834 -> 5,778 -> 1,665 -> 3. Its additional threshold 1/35 calculation is an optional consistency check.

The threshold 1/36 separates the three stated extrema. Neither certificate determines the fourth-largest value.

## Citation

Qi Zhou. *Computational materials for spectral bipartiteness in generalized odd graphs of diameter three*, mathematical revision of 15 September 2026. Cite this repository together with the commit used. The existing `CITATION.cff` describes the preserved v1.0.0 release.
