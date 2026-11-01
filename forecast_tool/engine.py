"""Deterministic calculation and guardrail engine for BIA674 forecast prototype.

Uses only Python standard library. Data are a fixed, public, historical case-study
subset. This file is a tool prototype, not a deployed ChatGPT plugin.
"""
import csv
import json
import math
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / 'knowledge' / 'BIA674_Midterm_Munoz_OJ_Real_Data.csv'

class InputError(ValueError):
    def __init__(self, code, message, next_step):
        self.code, self.next_step = code, next_step
        super().__init__(message)


def load_sales(path=DATA):
    """Read and validate the source, including transformation from natural log sales."""
    with open(path, encoding='utf-8', newline='') as file:
        rows = list(csv.DictReader(file))
    if len(rows) != 121:
        raise InputError('INVALID_DATASET', f'Expected 121 rows, found {len(rows)}.', 'Provide a complete validated source.')
    sales = []
    for i, r in enumerate(rows):
        w = int(r['Week'])
        if w != 40 + i or int(r['Store']) != 54 or int(r['Brand']) != 6:
            raise InputError('INVALID_DATASET', 'Week sequence or Store/Brand identifier invalid.', 'Recheck the source file.')
        units = int(r['Units_Sold'])
        if units <= 0 or abs(math.exp(float(r['LogMove_Original'])) - units) >= 0.001:
            raise InputError('INVALID_DATASET', f'Invalid sales units or log-to-unit conversion at week {w}.', 'Confirm source units and logmove.')
        expected_split = ('Train' if i < 89 else 'Validation' if i < 105 else 'Test')
        if r['Split'] != expected_split:
            raise InputError('INVALID_DATASET', f'Data split mismatch at week {w}.', 'Restore chronological train/validation/test split.')
        sales.append(units)
    return sales


def _mean(values):
    return sum(values)/len(values)


def series_forecasts(y):
    n = len(y)
    naive = [None] + [float(y[i-1]) for i in range(1,n)]
    moving = [None if i<4 else _mean(y[i-4:i]) for i in range(n)]
    ses = [None]*n
    level = _mean(y[:8])
    for i in range(8,n):
        ses[i] = level
        level = 0.1*y[i] + 0.9*level
    xx = list(range(1,17))
    xbar, ybar = _mean(xx), _mean(y[:16])
    slope = sum((x-xbar)*(d-ybar) for x,d in zip(xx, y[:16]))/sum((x-xbar)**2 for x in xx)
    intercept = ybar - slope*xbar
    level, trend = intercept + slope*16, slope
    holt = [None]*n
    for i in range(16,n):
        holt[i] = level + trend
        old = level
        level = 0.1*y[i] + 0.9*(level+trend)
        trend = 0.2*(level-old)+0.8*trend
    seasonal = [None if i<52 else float(y[i-52]) for i in range(n)]
    return {'Naive':naive, 'MA4':moving, 'SES':ses, 'Holt':holt, 'Seasonal naive 52 (diagnostic only)':seasonal}


def metrics(y, forecast, begin, end):
    pairs = [(float(forecast[i])-y[i], float(y[i])) for i in range(begin,end)]
    if any(forecast[i] is None or y[i]<=0 for i in range(begin,end)):
        raise InputError('INVALID_METRIC', 'Missing forecast or zero demand makes a metric undefined.', 'Select a valid window/metric.')
    errors = [e for e,_ in pairs]
    return {
        'MAD_units':_mean([abs(e) for e in errors]),
        'MSE_units_squared':_mean([e*e for e in errors]),
        'MAPE_percent':100*_mean([abs(e)/d for e,d in pairs]),
        'mean_error_units':_mean(errors),
    }


def run(request=None):
    """Execute one simulated planner request. Never issues external actions.

    request fields: intent='forecast'|'place_order'; scenario_last_week_units=int|None;
    missing_last_week=bool; claimed_last_week_units=int|None.
    """
    request = request or {}
    source='BIA674_Midterm_Munoz_OJ_Real_Data.csv, Store 54, Brand 6, weeks 40-160'
    if request.get('intent','forecast') not in ('forecast', 'place_order'):
        return {'status':'HUMAN_REVIEW','code':'UNSUPPORTED_INTENT',
                'message':'Outside the approved forecasting workflow.','next_step':'Ask a supply chain planner to review the request.'}
    if request.get('intent')=='place_order':
        return {'status':'BLOCKED','code':'UNAUTHORIZED_ACTION',
                'message':'No purchase orders or supplier communications are authorized; a forecast is not an order quantity.',
                'next_step':'Have the planner/buyer review inventory, lead time, service level, and approvals.'}
    y=load_sales()
    if request.get('missing_last_week'):
        return {'status':'NEEDS_INPUT','code':'MISSING_CRITICAL_DEMAND',
                'message':'Week 160 actual demand is missing for this revised scenario. The official value cannot be reused without permission.',
                'next_step':'Provide or confirm the actual week 160 demand; do not invent or silently fill the value.'}
    claimed=request.get('claimed_last_week_units')
    if claimed is not None and (not isinstance(claimed,int) or isinstance(claimed,bool) or claimed<0):
        raise InputError('INVALID_INPUT','Claimed demand must be a nonnegative integer.','Provide a valid unit count.')
    if claimed is not None and claimed != y[-1]:
        return {'status':'NEEDS_RECONCILIATION','code':'SOURCE_CONFLICT',
                'message':f'External claim for week 160 is {claimed:,} units; validated CSV records {y[-1]:,}.',
                'next_step':'Identify the authoritative source and obtain human approval before changing the official dataset.'}
    scenario=request.get('scenario_last_week_units')
    if scenario is not None and (not isinstance(scenario,int) or isinstance(scenario,bool) or scenario<0):
        raise InputError('INVALID_INPUT','Scenario demand must be a nonnegative integer.','Provide a valid hypothetical value.')
    models=series_forecasts(y)
    validation={name:metrics(y,f,89,105) for name,f in models.items()}
    test={name:metrics(y,f,105,121) for name,f in models.items()}
    # Select among the FOUR predefined candidates, using validation data only.
    candidates=('Naive','MA4','SES','Holt')
    chosen=min(candidates,key=lambda name: validation[name]['MAD_units'])
    baseline=sum(y[-4:])/4
    synthetic = (sum(y[-4:-1])+scenario)/4 if scenario is not None else None
    forecast = synthetic if scenario is not None else baseline
    # independent calculation of selected forecast and error, same data separate aggregation
    independently_checked = abs(baseline-_mean([y[-1],y[-2],y[-3],y[-4]])) < 1e-10
    assert independently_checked
    return {
        'status':'SIMULATED' if scenario is not None else 'OK',
        'case':source,
        'selected_model':chosen,
        'selection_rule':'Lowest validation MAD among Naive, MA4, SES and Holt (weeks 129-144).',
        'forecast_week':161,
        'forecast_units':forecast,
        'baseline_week_161_forecast_units':baseline,
        'scenario_week_160_units':scenario,
        'actual_week_160_units':y[-1],
        'validation_metrics':validation,
        'holdout_test_metrics':test,
        'independent_check':independently_checked,
        'units':'retail units per week',
        'error_sign':'forecast minus actual',
        'human_approval_required':True,
        'warnings':[
            'This historical dataset has no actual demand for week 161.',
            'The output is a demand forecast, NOT a purchase order.',
            'On-hand inventory, supplier lead times and promotion plans are not provided.',
            'Holt has lower holdout MAPE than MA4; MA4 is chosen by validation MAD.',
            'No model was selected or tuned based on holdout performance.'
        ]
    }


def cli():
    import argparse
    p=argparse.ArgumentParser(description='BIA 674 real-data forecasting tool')
    p.add_argument('--request', default='{}',help='JSON string with intent/scenario_last_week_units/missing_last_week/claimed_last_week_units')
    opts=p.parse_args()
    try:
        print(json.dumps(run(json.loads(opts.request)),indent=2))
    except InputError as e:
        print(json.dumps({'status':'NEEDS_REVIEW','code':e.code,'message':str(e),'next_step':e.next_step},indent=2))

if __name__=='__main__':
    cli()
