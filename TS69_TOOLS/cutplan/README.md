# CutPlan — TS69 Workshop Tools

A working, dependency-free Python cut-list calculator for carpenters, workshop makers and anyone cutting repeat lengths from identical stock. It reads dimensions from a CSV and prints a board-by-board cutting plan, including blade kerf and offcuts. No signup, network access or paid service.

## CutPlan Mobile — standalone browser version

[**Download CutPlan Mobile (single HTML file)**](https://raw.githubusercontent.com/thotsl4yer69/thotsl4yer69/main/TS69_TOOLS/cutplan/cutplan-mobile.html) · [View source](./cutplan-mobile.html)

Save the linked HTML file to your device and open it in a modern browser. It runs entirely offline, without installing Python or sending measurements anywhere. Enter a CSV cut list, calculate board allocations, print the cutting plan, or export a board-by-board CSV. This version uses the same best-fit decreasing method and conservative kerf convention as the Python tool.

**Validation:** the browser algorithm was checked against the documented 9-piece sample (3 boards, 1,091.2 mm combined offcut). Browser UI automation and field use have **not** yet been verified; do not interpret the algorithm check as a complete mobile-browser QA pass.

**Run (Python 3.9+):**

```bash
python cutplan.py --stock 2400 --kerf 3.2 --csv cuts.csv
```

CSV input (millimetres):

```csv
length_mm,quantity
1200,2
760,3
350,4
```

Verified output for this example:

```text
TS69 CutPlan | 9 pieces | 3 boards of 2400 mm | kerf 3.2 mm
Board  1: 1200 + 760 + 350 | offcut 80.4 mm
Board  2: 1200 + 760 + 350 | offcut 80.4 mm
Board  3: 760 + 350 + 350 | offcut 930.4 mm
Total offcuts 1091.2 mm; reserved kerf 28.8 mm
```

Structured output: `python cutplan.py --stock 2400 --kerf 3.2 --csv cuts.csv --json`.

Tests: `python -m unittest -v`.

**Limits:** Best-fit decreasing heuristic for a single stock length, not a guaranteed mathematical optimum. Reserves one blade kerf per piece including final pieces, deliberately conservative when factory ends can be used. Dimensions support 0.001 mm precision. Does not model grain, defects, mitres, end trimming, clamps or cutting-order constraints. Check usable stock lengths and measure before cutting.

**Verification:** 10 automated tests passed locally 4 November 2026; no claim of field validation or external users.

MIT-licensed original TS69 workshop utility.