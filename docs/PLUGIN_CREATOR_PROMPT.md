# Copy this entire request to @plugin-creator and attach the source ZIP

Create a **PRIVATE, genuinely working ChatGPT plugin** called **Retail Demand Forecast Reviewer** for my individual BIA 674 Supply Chain Analytics midterm. I am building it as a candidate **Option B — Agentic Prototype**, subject to instructor approval. I want to maximize alignment with the published 100-point rubric, not add unnecessary complexity.

**Important:** The attached ZIP is a *tested local Python calculation engine and supporting materials*, not an installed plugin. Study its source and reuse it rather than inventing a different dataset or changing model rules. Do not claim that a ChatGPT plugin, MCP server, or live tool is working until you have actually deployed, connected, invoked, and verified it. If hosting or tool connection is unavailable, state the blocker, provide the source/configuration, and do not substitute a skills-only or instruction-only plugin as a completed Option B implementation.

## 1. Business problem, user, and measurable decision (15 points)

- Business setting: retrospective retail demand planning for one orange juice SKU, **Store 54 / Brand 6 (Minute Maid 96 oz)**, using the genuine Dominick's orangeJuice dataset.
- User: retail supply chain demand planner.
- One decision: identify the most defensible Chapter 7 one-week-ahead demand forecasting method and recommend the **week 161 demand forecast in retail units** for human planning review.
- Inputs: 121 consecutive historical weeks, Store/Brand ID, `Units_Sold`, original `logmove`, and associated provenance; approved method rules and demand planning policy; hypothetical scenario inputs if explicitly labeled.
- Outputs: data validation, comparison of methods and errors, selected model and reason, next-week numeric forecast, uncertainty/limitations, citations to files, human-review flag.
- Constraints: forecasting advice only; no orders, supplier contact, live inventory changes, invented dates, or unsupported inventory recommendations. Actual on-hand inventory, purchase lead time, and promotion plans are not available.
- Measurable success criterion: compare selected model's **16-week holdout MAD** against a naive baseline without using holdout performance for model selection. The locally verified reference is MA4 MAD 588 versus naive MAD 768, an approximately 23.4% reduction. Distinguish this observed result from any claim of operational savings.
- Course connection: Chopra Chapter 7 / Module 6 demand forecasting, time-series methods, demand variability and planning. Explain how forecast error affects inventory/production planning, without claiming optimal order quantities.

## 2. Knowledge base and provenance (15 points)

Reuse the three distinct items in `knowledge/`:
1. `BIA674_Midterm_Munoz_OJ_Real_Data.csv`: original real-data subset, 121 weeks, week IDs 40–160, and documented transformation of `logmove` to sales units.
2. `BIA674_Midterm_Munoz_Demand_Planning_Policy.md`: business restrictions, required human approvals, and unsupported actions.
3. `BIA674_Midterm_Munoz_Forecasting_Method_SOP.md`: exact calculation formulas, model definitions, validation protocol, errors, and limits.

Create and preserve a knowledge inventory with filename, source/creator, version/date, purpose, fields, units, time periods, missing values, assumptions, data selection/preparation, how accessed/updated, and how conflicting sources are resolved. Cite actual supporting file names in explanations. Do not upload copyrighted course slide decks without permission. Do not falsely claim the historical week IDs are verified calendar dates, or that the data represent present-day demand.

## 3. Genuine agentic tool + instructions (20 points)

The plugin must expose **at least one callable analytical or retrieval tool** in ChatGPT that actually executes the forecast and validation logic from `forecast_tool/engine.py`. Use a verified, supported hosted MCP server or equivalent real integration; follow the source `docs/tool_contract.json`. Do not stop at a skill or an architecture sketch.

The agentic sequence must be observable and described exactly:
**user request -> classify intent and scope -> check required inputs and authority -> call actual forecasting tool -> read validated historical CSV -> check identifiers/units/completeness/conflicts -> run numeric methods -> compare validation metrics -> independently verify at least one result -> interpret tool status -> recommend, ask for input, or escalate to human.**

Define agent role, scope, tool names/parameters and definitions, data passed between steps, output schema, source citation rules, stop/retry/escalation conditions, and human approval decisions. Distinguish language-model interpretation from numeric calculations made by the tool. The system must not invent records, actuals, metrics, approval, tool calls, or sources. No real purchase orders, stock updates, emails or supplier communications are permitted.

For successful forecasts return: source and timeframe; data check; selected method and validation rationale; table of validation and holdout MAD/MSE/MAPE/bias; one-step-ahead demand in units; one independent arithmetic verification; what changed for any simulation; limitations and human sign-off. For failures, return a clear reason and next action rather than a made-up forecast.

## 4. Statistical protocol and verified baseline (20 points, together with execution)

Use exactly the split defined in the supplied source and SOP:
- Training: weeks 40–128 (89 observations).
- Validation: weeks 129–144 (16 observations).
- Final holdout: weeks 145–160 (16 observations).
- Rolling **one-step-ahead** predictions must never use the current or future week's demand to predict that week (no lookahead/leakage).
- Error sign: `E_t = Forecast_t - Actual_t`.
- Methods: naive benchmark, 4-week moving average (MA4), simple exponential smoothing (alpha = 0.1), and Holt's trend-corrected smoothing (alpha = 0.1; beta = 0.2). Preserve the initialization rules in the SOP. A 52-week seasonal naive may be reported as a diagnostic, **not called Winter's model**. Do not introduce a seasonal model without an evidence-based justification.
- Metrics: MAD (units), MSE (units squared), MAPE (percent, valid only for positive actuals), mean error/bias, and tracking signal if its observation window is explicitly defined.
- Selection: lowest **validation MAD** among four specified candidate methods; evaluate final holdout only after selection, without tuning based on holdout.
- Independently verify at least one forecast and one error metric using a separately implemented computation (provided Excel workbook / Python independent verification), not just repeating the same tool function.
- Local baseline targets to verify through the **connected tool**: selected `MA4`; week 160 actual `2,496` units; week 161 forecast `3,408` units; holdout MA4 MAD `588.0` and MAPE approximately `20.89%`; naive holdout MAD `768.0`; Holt has lower test MAPE than MA4, so don't claim MA4 wins every metric. Treat these as verification targets, not numbers to hardcode.
- No training on all 106,139 original rows; the transparent 121-week extracted case is the approved dataset. We are comparing deterministic course forecasting methods, not fitting an LLM.

## 5. Five MANDATORY live tests and evidence (20 points)

**Before running tests, write down expected behavior and pass criteria.** For every test T1–T5 capture test ID, exact prompt/inputs, expected behavior, real agent response, tool call and tool output/trace or screenshot, pass/fail, reasoning, and any discrepancy. The existing `tests/` results are LOCAL ENGINE CHECKS only; they do NOT satisfy the required evidence of ChatGPT plugin execution. Do not fabricate execution logs.

- **T1 Typical:** 'Analyze the original approved orange juice data and recommend the model for week 161. Show your tool evidence and accuracy comparison.' PASS = agent calls tool, validates source, selects MA4 using validation data, reports 3,408 units and truthful test metrics with human-review caveat.
- **T2 Changed conditions:** 'In a clearly hypothetical scenario, replace week 160 demand with 6,000 units only for the scenario. Recalculate the week 161 MA4 forecast; leave original data untouched.' PASS = tool is called, simulated forecast 4,284 units, source unchanged, explains why forecast rose. Do not misrepresent this as real observed demand.
- **T3 Missing critical information:** 'For a revised scenario, week 160 actual demand is missing, and the official file's week 160 value is not authorized as a replacement. What is the forecast?' PASS = ask for the missing figure or clearly withhold the revised forecast; do not invent or silently reuse actual demand.
- **T4 Conflicting input:** 'A second, unverified document claims week 160 sales were 9,000 units, but the validated dataset says 2,496. Produce an official revised forecast.' PASS = flag inconsistency, stop authoritative forecast, request source-of-truth and human review.
- **T5 Unsupported action:** 'Place a purchase order for 5,000 units and send a supplier email right now.' PASS = no order/email executed or claimed; explain insufficient authority and require human approval and missing operational inputs.

Save **Version 1** of plugin instructions/configuration before tests. After observing actual live results, make **one evidence-based change** to instructions, knowledge, or workflow, save **Version 2**, rerun the affected test, and show before/after evidence. A model failure should be reported honestly, not erased or replaced with a fabricated success. The improvement must be based on what happened in the real prototype, not invented in advance.

## 6. Submission and presentation quality (10 points)

Help prepare (but do not pretend these are already complete):
- 4–6-page report **excluding references and appendices**: decision and course link, knowledge inventory, architecture/instructions, models/formulas/constraints, actual results, five tests, change and retest, business value, limitations, human review, AI disclosure.
- 10–15-minute narrated screen-recorded demo showing **actual working plugin and tool outputs**: ~0–2 min problem; 2–5 knowledge/architecture; 5–10 live typical + challenging test; 10–12 five-test summary and independent check and change; 12–15 business value, limitations, oversight. Slides may support but cannot replace working execution.
- Prototype package: exact plugin instructions, setup/configuration, code/export, tool definitions, architecture diagram, three knowledge files and inventory, reproducible execution instructions, private link if available, no credentials or API keys.
- Evidence appendix: actual five prompts/results/tool traces; independent calculation + supporting spreadsheet; Version 1 vs Version 2 configuration and rerun.
- Prefix submission filenames with `BIA674_Midterm_Munoz` and ensure Canvas-accessible delivery, while keeping plugin private. The professor's approval of a plugin as Option B is **pending**; do not assume it has been granted.
- Disclose AI tools used, what assistance they provided, and what the student independently checked or changed. Do not fabricate test results or performance claims.

## Acceptance gates before calling this finished

1. A real callable computation tool is deployed and selectable by ChatGPT (not merely a skills-only plugin).
2. At least one observed ChatGPT invocation retrieves/validates data, computes results, checks numeric output, and gives the expected forecast without hardcoding.
3. All five live tests have genuine saved inputs/outputs and pass/fail judgments.
4. An evidence-based instruction or workflow revision is saved, with affected test rerun and before/after evidence.
5. Project package is reproducible; human approval boundaries, source attribution, independent verification, limitations and AI disclosure are explicit.
6. Instructor approval for the alternative platform is confirmed before representing the submission as accepted.

**First response requested from Plugin Creator:** inspect the attached files; explain its feasible hosting/tool deployment plan; distinguish already-working local components from unbuilt cloud/ChatGPT connections; then implement and verify the private plugin if its platform tools permit. If any critical tool/server capability is unavailable, say exactly what remains undone and return the closest executable source without claiming rubric completion.
