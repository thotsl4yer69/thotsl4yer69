# CutPlan — TS69 Workshop Tools

A working, dependency-free Python cut-list calculator for carpenters, workshop makers and anyone cutting repeat lengths from identical stock. It reads dimensions from a CSV and prints a board-by-board cutting plan, including blade kerf and offcuts. No signup, network access or paid service.

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