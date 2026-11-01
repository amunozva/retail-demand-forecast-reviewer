#!/usr/bin/env python3
"""Independent, standard-library verification of BIA 674 orange-juice forecasting.
Usage: python BIA674_Midterm_Munoz_Verify_Forecast.py
Requires the same-directory real-data CSV. Recomputes formulas independently from the Excel workbook.
"""
from pathlib import Path
import csv,math,statistics
p=Path(__file__).with_name('BIA674_Midterm_Munoz_OJ_Real_Data.csv')
rows=list(csv.DictReader(p.open()))
assert len(rows)==121
weeks=[int(r['Week']) for r in rows]
assert weeks==list(range(40,161)) and all(int(r['Store'])==54 and int(r['Brand'])==6 for r in rows)
y=[int(r['Units_Sold']) for r in rows]
assert all(v>0 for v in y)
assert all(abs(math.exp(float(r['LogMove_Original']))-int(r['Units_Sold']))<0.001 for r in rows)
assert all(r['Split']==('Train' if i<89 else 'Validation' if i<105 else 'Test') for i,r in enumerate(rows))
n=len(y)
naive=[None]+[float(a) for a in y[:-1]]
ma4=[None if i<4 else sum(y[i-4:i])/4 for i in range(n)]
ses=[None]*n
level=statistics.mean(y[:8])
for i in range(8,n):
 ses[i]=level
 level=.1*y[i]+.9*level
# Initial ordinary least squares for t = 1,...,16
k=16; xx=list(range(1,k+1)); xbar=statistics.mean(xx);ybar=statistics.mean(y[:k]);
slope=sum((x-xbar)*(v-ybar) for x,v in zip(xx,y[:k]))/sum((x-xbar)**2 for x in xx)
intercept=ybar-slope*xbar
level=intercept+slope*k;trend=slope
holt=[None]*n
for i in range(k,n):
 holt[i]=level+trend
 previous=level
 level=.1*y[i]+.9*(level+trend)
 trend=.2*(level-previous)+.8*trend
season52=[None if i<52 else float(y[i-52]) for i in range(n)]
series={'Naive':naive,'MA4':ma4,'SES':ses,'Holt':holt,'Seasonal naive 52':season52}
def metrics(f,lo,hi):
 z=[(f[i]-y[i],float(y[i])) for i in range(lo,hi)]
 assert all(f[i] is not None and y[i]>0 for i in range(lo,hi))
 return {'MAD':sum(abs(e) for e,d in z)/len(z),'MAPE_pct':100*sum(abs(e)/d for e,d in z)/len(z),
 'MSE':sum(e*e for e,d in z)/len(z),'mean_bias':sum(e for e,d in z)/len(z)}
print('Original dataset sales units | Store 54 | Brand 6 | Week 40-160')
print('Method                     Validation MAD     Test MAD      Test MAPE')
for name,f in series.items():
 v=metrics(f,89,105); t=metrics(f,105,121)
 print(f'{name:<24} {v["MAD"]:>13.2f} {t["MAD"]:>12.2f} {t["MAPE_pct"]:>13.2f}%')
selection=min(series,key=lambda name:metrics(series[name],89,105)['MAD'])
assert selection=='MA4'
assert abs(metrics(ma4,105,121)['MAD']-588)<1e-9
assert abs(metrics(naive,105,121)['MAD']-768)<1e-9
next_ma4=sum(y[-4:])/4
assert next_ma4==3408
scenario=sum(y[-4:-1])/4+6000/4
assert scenario==4284
print('Selected by validation MAD:',selection)
print('Week 161 one-week forecast:',next_ma4,'units')
print('Test MAD reduction vs naive:',round(100*(768-588)/768,4),'%')
print('Synthetic what-if: week 160=6000 => week 161 MA4',scenario,'units')
print('PASS: conversion, chronology, formula results, model selection and scenario checked.')
