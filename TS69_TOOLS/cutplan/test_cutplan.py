import tempfile
import unittest
from pathlib import Path
from cutplan import mm, plan, load_csv, report


class CutPlanTests(unittest.TestCase):
    def test_basic(self):
        boards = plan(mm('2400'), mm('3'), [mm('1000'), mm('1000'), mm('390')])
        self.assertEqual(len(boards), 1)
        self.assertEqual(sum(b['remaining'] for b in boards), mm('2400') - mm('2390') - mm('9'))

    def test_exact_consumption(self):
        b = plan(mm('1000'), mm('3'), [mm('997')])
        self.assertEqual(b[0]['remaining'], 0)

    def test_reject_overlength(self):
        with self.assertRaisesRegex(ValueError, 'exceeds stock'):
            plan(mm('1000'), mm('3'), [mm('998')])

    def test_reject_empty(self):
        with self.assertRaises(ValueError):
            plan(mm('1000'), mm('3'), [])

    def test_decimal_precision(self):
        self.assertEqual(mm('3.175'), 3175)
        with self.assertRaises(ValueError):
            mm('3.1759')

    def test_nonfinite_and_negative(self):
        for value in ('NaN', 'Infinity', '-1'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                mm(value)

    def test_csv_and_quantities(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/'cuts.csv'
            p.write_text('length_mm,quantity\n1200,2\n350,3\n', encoding='utf8')
            self.assertEqual(len(load_csv(p)), 5)

    def test_invalid_quantity(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/'cuts.csv'
            p.write_text('length_mm,quantity\n1200,0\n', encoding='utf8')
            with self.assertRaisesRegex(ValueError, 'quantity'):
                load_csv(p)

    def test_conservation_property(self):
        for stock in (1000, 1200, 2400):
            for kerf in (0, 3, 5):
                pieces = [101, 203, 307, 19, 49, 73, 100] * 2
                boards = plan(stock, kerf, pieces)
                self.assertEqual(len(pieces), sum(len(b['pieces']) for b in boards))
                for b in boards:
                    self.assertGreaterEqual(b['remaining'], 0)
                    self.assertEqual(stock, sum(b['pieces']) + len(b['pieces'])*kerf + b['remaining'])

    def test_report(self):
        data = report(mm("1000"), mm("3"), plan(mm("1000"), mm("3"), [mm("400"), mm("400")]))
        self.assertEqual(data['boards_required'], 1)
        self.assertEqual(data['offcut_total_mm'], '194')


if __name__ == '__main__':
    unittest.main()
