import unittest

from reporting import render_report


class RenderReportTests(unittest.TestCase):
    def test_sorts_entries_and_adds_total(self):
        entries = [{"name": "beta", "amount": 3}, {"name": "alpha", "amount": -1}]
        self.assertEqual(render_report(entries), "alpha: -1\nbeta: 3\nTOTAL: 2")

    def test_rejects_invalid_entries(self):
        with self.assertRaises(ValueError):
            render_report([{"name": "", "amount": 2}])
        with self.assertRaises(ValueError):
            render_report([{"name": "ok", "amount": "2"}])


if __name__ == "__main__":
    unittest.main()
