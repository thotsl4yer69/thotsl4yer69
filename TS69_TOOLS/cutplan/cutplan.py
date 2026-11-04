#!/usr/bin/env python3
"""TS69 CutPlan: reproducible one-dimensional workshop cut plans, no dependencies.

This is a best-fit decreasing heuristic, NOT a guaranteed globally optimal solution.
Each requested piece reserves one full kerf, including the final piece on a board.
That conservative convention avoids understating material requirements.
"""
import argparse
import csv
import json
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path


def mm(value):
    try:
        d = Decimal(str(value))
    except (InvalidOperation, ValueError):
        raise ValueError(f"Invalid dimension: {value!r}") from None
    if not d.is_finite() or d < 0:
        raise ValueError(f"Dimensions must be finite and nonnegative: {value!r}")
    if d.as_tuple().exponent < -3:
        raise ValueError("Dimensions support at most 3 decimal places (0.001 mm)")
    return int(d * 1000)


def pretty(v):
    return format(Decimal(v) / 1000, "f").rstrip("0").rstrip(".") if v % 1000 else str(v // 1000)


def plan(stock_mm, kerf_mm, pieces):
    if stock_mm <= 0:
        raise ValueError("Stock length must be greater than zero")
    if kerf_mm < 0:
        raise ValueError("Kerf must be nonnegative")
    if not pieces:
        raise ValueError("At least one cut is required")
    for piece in pieces:
        if piece <= 0:
            raise ValueError("Piece lengths must be greater than zero")
        if piece + kerf_mm > stock_mm:
            raise ValueError(f"Piece {pretty(piece)} mm plus kerf {pretty(kerf_mm)} mm exceeds stock")
    boards = []
    for piece in sorted(pieces, reverse=True):
        cost = piece + kerf_mm
        candidates = [(b['remaining'] - cost, i) for i, b in enumerate(boards) if b['remaining'] >= cost]
        if candidates:
            _, index = min(candidates)
            b = boards[index]
        else:
            b = {'pieces': [], 'remaining': stock_mm}
            boards.append(b)
        b['pieces'].append(piece)
        b['remaining'] -= cost
    return boards


def load_csv(path):
    pieces = []
    with open(path, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or not {'length_mm', 'quantity'} <= set(reader.fieldnames):
            raise ValueError("CSV must have length_mm,quantity columns")
        for n, row in enumerate(reader, 2):
            length = mm(row['length_mm'])
            try:
                quantity = int(row['quantity'])
            except (TypeError, ValueError):
                raise ValueError(f"Line {n}: quantity must be an integer") from None
            if quantity <= 0 or quantity > 10000:
                raise ValueError(f"Line {n}: quantity must be 1..10000")
            if length == 0:
                raise ValueError(f"Line {n}: length must be positive")
            pieces.extend([length] * quantity)
            if len(pieces) > 10000:
                raise ValueError("Maximum 10000 total pieces")
    return pieces


def report(stock, kerf, boards):
    used = sum(sum(b['pieces']) for b in boards)
    sawdust = sum(len(b['pieces']) for b in boards) * kerf
    waste = sum(b['remaining'] for b in boards)
    return {'stock_length_mm': pretty(stock), 'kerf_mm': pretty(kerf),
            'boards_required': len(boards), 'pieces': sum(len(b['pieces']) for b in boards),
            'finished_length_mm': pretty(used), 'reserved_kerf_mm': pretty(sawdust),
            'offcut_total_mm': pretty(waste),
            'boards': [{'board': i, 'cuts_mm': [pretty(p) for p in b['pieces']],
                        'offcut_mm': pretty(b['remaining'])} for i, b in enumerate(boards, 1)]}


def main(argv=None):
    parser = argparse.ArgumentParser(description='Best-fit cut list for one stock length (all units millimetres).')
    parser.add_argument('--stock', required=True, help='Usable stock length in mm')
    parser.add_argument('--kerf', default='3.2', help='Blade kerf in mm (default: 3.2)')
    parser.add_argument('--csv', required=True, type=Path, help='CSV with length_mm,quantity headers')
    parser.add_argument('--json', action='store_true', help='Machine-readable JSON output')
    args = parser.parse_args(argv)
    try:
        stock, kerf = mm(args.stock), mm(args.kerf)
        boards = plan(stock, kerf, load_csv(args.csv))
    except (ValueError, OSError) as e:
        parser.error(str(e))
    data = report(stock, kerf, boards)
    if args.json:
        print(json.dumps(data, indent=2))
    else:
        print(f"TS69 CutPlan | {data['pieces']} pieces | {data['boards_required']} boards of {pretty(stock)} mm | kerf {pretty(kerf)} mm")
        for b in data['boards']:
            print(f"Board {b['board']:>2}: " + ' + '.join(b['cuts_mm']) + f" | offcut {b['offcut_mm']} mm")
        print(f"Total offcuts {data['offcut_total_mm']} mm; reserved kerf {data['reserved_kerf_mm']} mm")
    return 0


if __name__ == '__main__':
    sys.exit(main())
