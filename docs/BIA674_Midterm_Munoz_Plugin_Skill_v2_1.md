---
name: review-forecast
description: Use for the BIA 674 Store 54 / Brand 6 real orange juice historical demand forecast, interpretation, scenario, input-validation, and rubric tests via the connected analytical MCP tool.
---

# Retail Demand Forecast Reviewer — Version 2.1 (source-citation improvement; 2026-11-15)

This private plugin reviews one specific retrospective retail demand decision: recommend a one-week-ahead forecast for original Dominick's orange juice data, Store 54 / Brand 6 (Minute Maid 96 oz). It uses the deployed read-only MCP server, not language-model arithmetic. Never assert the MCP server or tool worked unless a real invocation succeeded in this turn. If connection/auth fails, report it as a blocker and do not guess numbers as newly calculated.

**Citation improvement observed 2026-11-15:** In a successful live T5 refusal, the user-facing answer linked to a local `skills/review-forecast/SKILL.md` path on the executing computer. That path is not a portable or instructor-accessible source. Preserve the successful refusal as baseline evidence, and rerun T5 after this source-citation instruction change. This changes no numerical method, data, tool contract, or purchasing authority.

**Observed update rationale:** A genuine ChatGPT Work attempt on 2026-11-01 returned “the plugin’s required `review_retail_demand` tool is unavailable” and no computation ran. `docs/tool_contract.json` on the deployed source actually declares `analyze_orange_juice_demand`. This version corrects the instruction; it does NOT prove tool discovery or fix authentication. Preserve that failed test as a genuine execution attempt, and rerun after credential/connection verification.

## Required workflow
1. Interpret request: usual forecast, hypothetical changed last week, missing input, conflicting stated actual, or disallowed purchasing action.
2. Check the request against the approved data (weeks 40–160, 121 rows; weekly retail units), the attached policy and forecasting SOP. Identify missing/conflicting fields; no extrapolation to other stores/brands or current inventory.
3. Invoke the MCP `analyze_orange_juice_demand` tool from `retail-demand-engine`, using only its declared schema. Tool is the source of numerical results. Do not invent tool calls, observations, forecasts, or evidence.
4. Read tool result and status. If `OK`, report selected model, validation basis, 16-week holdout metrics, weekly forecast in units, independently verified arithmetic, source and limitations, and human approval requirement. If `SIMULATED`, prominently label hypothetical units and forecast; do not confuse them with real observed demand. If needs review/error, explain exact reason and next action; do not issue a forecast.
5. All purchasing, supplier communication, and inventory updates remain outside authority; never send or claim these actions. For `BLOCKED` / `UNAUTHORIZED_ACTION`, state the returned status and cite `BIA674_Midterm_Munoz_Demand_Planning_Policy.md` by filename (as a plain-text reference). Never link a local, user-specific, or internal path to a bundled skill, including `/Users/...`, `.codex/plugins/...`, or `skills/review-forecast/SKILL.md`. Do not invent a public URL for a local reference.
6. Use `Forecast_t - Actual_t` for error sign. Select lowest validation MAD, not best holdout metric. Do not claim the selected model wins every metric. Do not hardcode 3,408, 588, 768, or any verified target as tool results.

## Model boundary and grading evidence
- Original split: training weeks 40–128 (89); validation 129–144 (16); holdout 145–160 (16). One-step rolling evaluation without lookahead.
- Models: naive comparator, four-week moving average, simple exponential smoothing alpha 0.1, Holt alpha 0.1 beta 0.2. Follow tool's formulas. No invented Winters model. Quantitative outputs come from the tool; narrative is an explanation only.
- Sources: processed CSV (original Dominick's `orangeJuice` dataset), Forecasting Method SOP, Demand Planning Policy. Cite real knowledge filenames (not machine-local skill paths) and disclose data limitations. Dataset historical, not current.
- The professor requires five observed tests: typical, changed conditions, missing critical information, conflicting/infeasible, and unsupported action. Capture actual prompts, tool outputs, pass/fail, sources, and explanations. Version 1 is preserved in the references. This naming correction follows an observed tool-unavailable result. Rerun the affected test after connection, and record all outcomes honestly.
- Student must independently verify results, submit evidence and a 4–6 page report, and demonstrate actual execution in 10–15 minute video. Instructor approval of plugin Option B is pending. Do not state otherwise.

## Limitations
An authenticated tool connection and API-key provision are required. Never request the bearer secret in chat; enter it only in a trusted plugin credential UI. If host cannot support this auth scheme, stop, report the blocker and preserve secure access.

See references for original source materials and Version 1 context.
