"""Unit tests of standalone ENGINE (NOT actual ChatGPT plugin traces)."""
import json
import math
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from forecast_tool.engine import run, load_sales, series_forecasts, metrics

class ForecastTests(unittest.TestCase):
    def test_baseline(self):
        r=run()
        self.assertEqual(r['status'],'OK')
        self.assertEqual(r['selected_model'],'MA4')
        self.assertEqual(r['forecast_units'],3408)
        self.assertEqual(r['actual_week_160_units'],2496)
        self.assertEqual(r['holdout_test_metrics']['MA4']['MAD_units'],588)
        self.assertTrue(math.isclose(r['holdout_test_metrics']['MA4']['MAPE_percent'],20.89,abs_tol=0.01))
        self.assertTrue(r['independent_check'])
        self.assertLess(r['validation_metrics']['MA4']['MAD_units'],r['validation_metrics']['Holt']['MAD_units'])
    def test_scenario(self):
        r=run({'scenario_last_week_units':6000})
        self.assertEqual(r['status'],'SIMULATED')
        self.assertEqual(r['baseline_week_161_forecast_units'],3408)
        self.assertEqual(r['forecast_units'],4284)
        self.assertEqual(r['actual_week_160_units'],2496)
    def test_missing(self):
        r=run({'missing_last_week':True})
        self.assertEqual(r['code'],'MISSING_CRITICAL_DEMAND')
        self.assertNotIn('forecast_units',r)
    def test_conflict(self):
        r=run({'claimed_last_week_units':9000})
        self.assertEqual(r['code'],'SOURCE_CONFLICT')
        self.assertNotIn('forecast_units',r)
    def test_purchase(self):
        r=run({'intent':'place_order'})
        self.assertEqual(r['code'],'UNAUTHORIZED_ACTION')
        self.assertNotIn('forecast_units',r)
    def test_time_order_no_leakage(self):
        y=load_sales(); preds=series_forecasts(y)
        self.assertEqual(len(y),121)
        self.assertEqual(preds['MA4'][105],sum(y[101:105])/4)
        self.assertEqual(preds['Naive'][105],y[104])

if __name__=='__main__':
    unittest.main(verbosity=2)
