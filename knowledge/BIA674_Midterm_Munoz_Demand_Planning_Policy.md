# Knowledge item 2 — Demand planning decision policy
**Version:** 1.0 | **Created:** 2026-11-01 | **Creator:** Project author with AI assistance; review required

## Business setting
A retrospective retail-planning case study for Store 54, Minute Maid 96 oz (brand 6). The demand planner must select a forecasting method and obtain an auditable *one-week-ahead* demand forecast. The original source is the public `bayesm` orangeJuice dataset. The store identifier is anonymized; this is not a current live replenishment system.

## Scope and authorization
- Output: preferred forecasting method, forecast in **units sold per week**, model-comparison metrics, uncertainty/risks, and a next-step recommendation for the planner.
- Do not place orders, contact suppliers, alter enterprise systems, or imply that a forecast equals a purchase-order quantity.
- Ordering decisions require human review of on-hand inventory, inventory in transit, replenishment lead time, desired service level, review cycle, storage limitations, and known upcoming promotions. These inputs are **not** in the provided dataset.
- The week IDs (40–160) are dataset identifiers, not verified dates. Never invent calendar dates.

## Model governance
- Use only information known at the forecast origin. Historical one-week-ahead forecasting may update after each prior week's demand is observed.
- Select the model on **validation MAD**, using weeks 129–144. Keep weeks 145–160 isolated for final evaluation; do not reselect based on final test performance.
- Demonstrate the baseline (last observed week's demand), a 4-week moving average, simple exponential smoothing (alpha=0.1), and Holt's model (alpha=0.1, beta=0.2). A 52-week seasonal-naive model is diagnostic only, not proof of annual seasonality.
- Do not force Winter's method: it requires a supported seasonal pattern and adequate history for seasonal initialization. Document any omission.
- Calculate all quantitative results with a computational tool, check formula consistency, and report unrounded results internally. Display concise rounded results.
- Error sign convention from Chapter 7: **E_t = F_t - D_t** (positive = over-forecast).
- Report MAD (units), MSE (units squared), MAPE (percent), and signed mean error (units); compare test results only after selection.

## Missing, conflicting, and unusual inputs
- Ask the human to provide missing critical weekly demand and corresponding week IDs. Do not silently interpolate or invent values for operational decisions.
- If a scenario modifies an existing observation, identify it as a hypothetical scenario and preserve the untouched real dataset.
- If a user input conflicts with the validated source, disclose both values and request a source-of-truth decision; do not silently overwrite.
- If demand is zero, MAPE is undefined for that observation. State this and use MAD/MSE or a pre-agreed alternative rather than dividing by zero.
- If model predictions are negative, do not suggest a negative inventory order; flag for review and apply the agreed forecast policy only with an explanation.
- If the requested advice exceeds the file or the system's approval authority, state the limitation and escalate.

## Approvals
A retail demand planner must review weekly forecasts before converting them to inventory plans. A purchasing manager or authorized buyer must approve any actual order. This prototype makes **no external actions**.
