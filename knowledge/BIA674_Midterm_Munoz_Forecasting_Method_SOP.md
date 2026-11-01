# Knowledge item 3 — Forecasting methods and validation SOP
**Version:** 1.0 | **Created:** 2026-11-01 | **Creator:** Project author with AI assistance; aligned with Chopra Chapter 7

## Data and selection process
1. Read `BIA674_Midterm_Munoz_OJ_Real_Data.csv`. It contains exactly 121 original weekly observations for Store 54 / Brand 6, spanning week IDs 40 to 160 inclusive. The store has complete week coverage across all 11 brands, and Brand 6 has the lowest training-period coefficient of variation among that store's brands. Selection is based on completeness/stability rather than test error.
2. Source field: `logmove` is the natural log of sales units; recover weekly units as `ROUND(EXP(logmove), 0)`; double-check the exported numeric `Units_Sold`. `Deal_Indicator` and `Feature_Value` are descriptors, not predictors in these univariate forecasts.
3. Ensure each week occurs once, every week is present, and all unit quantities are positive. Week indexes are **not** converted into actual dates.
4. Partition chronologically: train weeks 40–128 (89 obs.), validation weeks 129–144 (16), test weeks 145–160 (16).

## Forecast calculations (one-step ahead, t predicted using t−1 and earlier)
- **Naive baseline:** F_t = D_(t−1).
- **Moving average (N=4):** F_t = [D_(t−4)+D_(t−3)+D_(t−2)+D_(t−1)] / 4.
- **Simple exponential smoothing:** Initialize level with mean of first 8 weeks. F_t=L_(t−1), L_t=0.1D_t+0.9L_(t−1). Initial forecasts start at the ninth observation.
- **Holt's trend-corrected smoothing:** Fit OLS line to first 16 periods; initialize level at t=16 and trend as OLS slope. F_t=L_(t−1)+T_(t−1), L_t=0.1D_t+0.9(L_(t−1)+T_(t−1)), T_t=0.2(L_t−L_(t−1))+0.8T_(t−1). Initial Holt forecast begins at observation 17.
- **52-week seasonal naive (diagnostic):** F_t=D_(t−52); this is not Winter's seasonal exponential smoothing.

## Model evaluation and governance
For each week with a forecast: E_t = F_t−D_t, AE_t=|E_t|, PE_t=|E_t|/D_t (when D_t>0), SE_t=E_t^2. MAD=mean(AE), MSE=mean(SE), MAPE=100*mean(PE), Bias=mean(E). These are calculated separately over equal 16-week validation and test periods. Tracking signal is cumulative signed error divided by running MAD; identify the window used when discussing it. Select smallest validation MAD, then inspect test results **once** for evidence; no retuning from test.

## Independent check
`BIA674_Midterm_Munoz_Verify_Forecast.py` recomputes these quantities directly from the CSV independently of the Excel formulas. Excel formulas are visible in `BIA674_Midterm_Munoz_Forecasting_Analysis.xlsx`.

## Expected example values (independently computed)
- Validation MAD: Naive 1,656.0; MA4 1,141.5; SES 1,389.23; Holt 1,407.65; seasonal naive 1,482.0 units.
- Holdout MAD: Naive 768.0; MA4 588.0; SES 641.62; Holt 590.37; seasonal naive 1,374.0 units.
- Holdout MAPE: MA4 20.89%; Holt 19.45%. **Holt beats MA4 on holdout MAPE, not MAD.**
- Recommendation: MA4 selected on validation MAD; forecast week 161 = 3,408 units; naive week 161 forecast = 2,496 units.

## Limitations
This is a historical, single-store/SKU study with promotions and large price changes; univariate models cannot explicitly anticipate advertised promotions. Forecasts are not orders, no inventory stock data is supplied, and the one-step error estimate is not a multi-week lead-time forecast error distribution. Actual week 161 demand is unknown in this dataset. A 52-week seasonal cycle is not proven by ~2.3 years of observations alone.
