# Expected outputs

These files are the fixed reference outputs for the manuscript's exact calculations. The verification programs write newly computed reports in the repository root. `run_all.py` compares the JSON objects and CSV records with the copies in this directory and exits with a nonzero status on any mismatch. The expected files are never overwritten by the programs.

- `verification_report.json`: primary counts, survivors, multiplicities, and rational auxiliary checks for thresholds 1/36 and 1/35.
- `candidate_audit.csv`: all 1,665 candidates meeting the 1/36 spectral threshold, with principal minors and the first multiplicity-test outcome.
- `independent_report.json`: Sturm-and-trace verification counts, surviving triples, and the eight consistent trace systems.
- `construction_report.json`: checks of the cycle C7, Odd graph O4, and folded 7-cube.
