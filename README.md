# Spectral extrema in generalized odd graphs

Computational certificates accompanying **Spectral bipartiteness in generalized odd graphs of diameter three**, by Qi Zhou.

Repository: https://github.com/zhouqi-math/generalized-odd-graph-spectral-extrema

The manuscript cites the fixed release **v1.0.0**. Download that version to reproduce the reported calculation.

The main certificate classifies the nonbipartite distance-regular graphs of diameter three and odd girth seven satisfying `(largest eigenvalue + smallest eigenvalue) / order >= 1/36`. The survivors are `C7`, `O4 = KG(7,3)`, and the folded 7-cube. The valency cutoff `k <= 182` and order bound `5n < 117k` are proved before the search in Proposition 3.3 of the manuscript.

## Files

| File | Role | Generated output |
|---|---|---|
| `verify_q1.py` | Primary certificate: exact factorization, resolvent residues, and tridiagonal principal minors; corresponding to Section 4 of the manuscript | `verification_report.json`, `candidate_audit.csv` |
| `verify_independent_sympy.py` | Second verification: characteristic polynomial computed from the 4-by-4 intersection matrix, exact Sturm root counts, and rational trace equations | `independent_report.json` |
| `verify_constructions.py` | Direct adjacency constructions and checks of all three surviving graphs | `construction_report.json` |
| `run_all.py` | Executes the programs and compares all outputs with `expected/` | `run_summary.json` |
| `expected/` | Fixed reference copies of the four JSON/CSV outputs | Never overwritten by the programs |
| `requirements.txt` | Pinned optional SymPy dependency | None |

No graph database or network access is used by the verification programs. Installing the optional dependency is a separate environment preparation step. The mathematical derivation of the finite range and the uniqueness arguments are given in the accompanying manuscript.

## Primary and construction verification

Python 3.8 or later is sufficient; no third-party packages are required. Clone this repository or download the source archive for release v1.0.0, then run from the directory containing this README:

```text
python run_all.py
```

The command runs the primary certificate and construction checks and compares their reports with the supplied expected data. JSON objects and CSV records are compared, so line-ending conventions do not affect the checks. Success gives two `PASS` lines and the three survivor tuples. Any failed assertion, process, or comparison causes a nonzero exit status. Run with assertions enabled, without `-O` or `PYTHONOPTIMIZE`.

Individual commands are also available:

```text
python verify_q1.py
python verify_constructions.py
```

Outputs are written beside the scripts. Re-running them replaces generated outputs, while the `expected/` copies remain unchanged.

## Optional second verification

The full package was checked with Python 3.12.14 and SymPy 1.14.0. To prepare the optional dependency and execute all three programs:

```text
python -m pip install -r requirements.txt
python run_all.py --with-independent
```

Alternatively run `python verify_independent_sympy.py` directly. It does not import the primary certificate. For each of the 5,778 triples meeting the order bound it constructs the intersection matrix, obtains its characteristic polynomial, divides out the principal factor, and counts roots strictly below the rational threshold using Sturm's method. It checks agreement with the principal-minor criterion on that whole set, including the treatment of threshold equality. Multiplicities are determined from exact trace equations for powers 0, 1, 2, 3, and 5; conjugate roots have a common multiplicity.

The two programs share the mathematically proved range and necessary conditions, but use different polynomial and spectral tests. This is algorithmic cross-verification, not a claim of external peer review.

## Expected main output

| Stage | Parameter triples |
|---|---:|
| Entire proved range | 1,004,731 |
| Integral distance layers | 21,834 |
| Order bound | 5,778 |
| Spectral threshold | 1,665 |
| Nonconstant conjugate multiplicity: rejected | 1,531 |
| Nonintegral multiplicity: rejected | 130 |
| Multiplicity below valency: rejected | 1 |
| All tests passed | 3 |

The survivor tuples `(k, mu, c, n)` are `(2,1,1,7)`, `(4,1,2,35)`, and `(7,2,3,64)`. Rejection categories in the CSV indicate the first failed factor test and are mutually exclusive. All 1,665 threshold candidates are recorded.

The second program finds the same threshold candidates and survivors: 1,657 trace systems are inconsistent, and five more candidates fail the multiplicity conditions. The construction checker tests every distance layer around every vertex, all intersection parameters, vanishing traces at odd powers 1, 3 and 5, a positive trace at power 7, and the stated adjacency annihilating polynomials. These checks certify existence of the examples. Uniqueness is justified in Section 5 by Huang and Liu's Main Theorem on page 196, rather than by the search alone.

## Optional threshold 1/35 calculation

For convenience, the primary program also runs the threshold `1/35` with the separately proved cutoff `k <= 165` and order bound `5n < 112k`. It leaves `O4` and the folded 7-cube. This is an optional consistency check embedded in the supplied script; it is not logically required for the second or third extremum, which follow from the `1/36` classification. Its counts and outputs appear under `focused_certificate` in `verification_report.json`.

The rational threshold `1/36` separates the three displayed values from all other values in the class. No fourth-largest value is determined.

## Inspecting the source and outputs

Polynomial coefficient lists in the primary and construction programs are in ascending degree order. SymPy's displayed polynomial factors use its ordinary algebraic notation. All decisions use integer or rational arithmetic. No approximate eigenvalue tolerance is used.

The assertion of the final survivor list is a check after the exhaustive loops; it does not restrict the search to those graphs. The reported counts and output comparisons make omissions or accidental changes detectable. Running the certificate is required to reproduce the computational part; merely passing necessary parameter conditions does not prove graph existence.

## Citation

Qi Zhou. *Exact certificates for spectral bipartiteness in generalized odd graphs of diameter three*, version 1.0.0. https://github.com/zhouqi-math/generalized-odd-graph-spectral-extrema

The accompanying manuscript is *Spectral bipartiteness in generalized odd graphs of diameter three*. No journal publication identifier is assigned here. Machine-readable software citation information is provided in `CITATION.cff`.
