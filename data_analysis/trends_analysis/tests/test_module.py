import unittest
import pandas as pd
from data_analysis.trends_analysis.analysis_trends_package.trend_analysis import TrendAnalyzer


class TestTrendAnalyzer(unittest.TestCase):

    def setUp(self):
        data = pd.Series([1, 2, 3, 4, 3, 2, 1, 2, 3, 4])
        self.analyzer = TrendAnalyzer(data)

    def test_moving_average(self):
        result = self.analyzer.moving_average(window=3)
        self.assertEqual(len(result), len(self.analyzer.data))
        self.assertAlmostEqual(result.iloc[3], 3.0, places=1)

    def test_difference(self):
        result = self.analyzer.difference()
        self.assertEqual(len(result), len(self.analyzer.data))
        self.assertEqual(result.iloc[5], -1)

    def test_autocorrelation(self):
        result = self.analyzer.autocorrelation(lag=1)
        self.assertIsInstance(result, float)
        self.assertTrue(-1 <= result <= 1)

    def test_find_extremium_points(self):
        result = self.analyzer.find_extremium_points()
        self.assertIn('Maximum', result.columns)
        self.assertIn('Minimum', result.columns)
        self.assertEqual(result['Maximum'].iloc[3], 4)
        self.assertEqual(result['Minimum'].iloc[6], 1)


if __name__ == '__main__':
    unittest.main()
