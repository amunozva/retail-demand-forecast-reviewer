"""Independent audit: no imports from engine, uses Decimal and week-keyed records."""
import csv
from decimal import Decimal
from pathlib import Path

def verify():
    path=Path(__file__).resolve().parents[1]/'knowledge'/'BIA674_Midterm_Munoz_OJ_Real_Data.csv'
    with path.open(newline='') as f:
        demand={int(r['Week']):Decimal(r['Units_Sold']) for r in csv.DictReader(f)}
    records=[]
    for week in range(145,161):
        forecast=sum(demand[week-lag] for lag in (1,2,3,4))/Decimal(4)
        error=forecast-demand[week]
        records.append({'week':week,'actual':float(demand[week]),'forecast':float(forecast),'error':float(error)})
    mad=sum(abs(Decimal(str(r['error']))) for r in records)/Decimal(len(records))
    forecast=sum(demand[w] for w in (157,158,159,160))/Decimal(4)
    return {'implementation':'Separate Decimal, week-keyed calculation; no engine imports',
            'window':'holdout weeks 145–160, 16 observations',
            'last_four_units':[int(demand[w]) for w in (157,158,159,160)],
            'forecast_units':float(forecast),'holdout_MA4_MAD_units':float(mad),'rows':records}
