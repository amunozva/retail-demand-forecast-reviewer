# BIA 674 — Retail Demand Forecast Reviewer (working calculation engine, not yet connected to ChatGPT)

**Project:** Individual Midterm, Option B candidate — Agentic prototype
**Scope:** One real historical retail orange juice SKU at one store, one-week-ahead demand recommendation
**Status:** Source and engine tests complete. Cloud MCP hosting, ChatGPT plugin connection, agent UI testing, narrated demonstration and professor approval remain pending. **This archive is not an installable functioning ChatGPT plugin.**

## What's in this package
- `knowledge/`: Real 121-week demand CSV, original demand-planning policy and method SOP (3 documented items)
- `forecast_tool/engine.py`: Pure Python data retrieval, input validation, forecasting and decision tool; no paid services or model training
- `tests/test_engine.py`: Six local tests, covering the five rubric categories and leakage check
- `evidence/`: Baseline independent validation script, local execution trace, original five-test prompt plan (NOT evidence of plugin execution)
- `docs/architecture.md`: Proposed agentic control flow and human authority boundary
- `docs/PLUGIN_CREATOR_PROMPT.md`: Handoff instructions to generate and connect a private plugin with an actual MCP tool
- `docs/tool_contract.json`: Computation tool request/response interface for implementation

## Run the engine immediately
Python 3.9+ required; no third-party dependencies.

From the project folder:

```bash
python forecast_tool/engine.py
python forecast_tool/engine.py --request '{"scenario_last_week_units": 6000}'
python forecast_tool/engine.py --request '{"missing_last_week": true}'
python forecast_tool/engine.py --request '{"claimed_last_week_units": 9000}'
python forecast_tool/engine.py --request '{"intent": "place_order"}'
python -m unittest discover -s tests -v
```

The baseline expected output is MA4 / 3408 units in week 161 / holdout MAD 588 units. Tests T1–T5 run the deterministic tool behavior. You must repeat them **in ChatGPT after plugin hosting and installation**, recording actual ChatGPT prompt, tool call, response and result for academic evidence. No live supplier/ERP action is available.

## Connect this to a plugin
1. Open ChatGPT Plugins and invoke the installed **Plugin Creator** (or use `@plugin-creator` in a new chat).
2. Attach this ZIP (or its content) and send the prompt from `docs/PLUGIN_CREATOR_PROMPT.md`.
3. Ask Plugin Creator to make the Python computation into a real callable hosted MCP tool, not just a skill. Provide the public/private host configuration only through the platform's supported deployment workflow; no verified remote MCP URL is included or implied in this ZIP.
4. Install the private plugin, select it in a new ChatGPT chat using @ mention, and test the five prompts. Save exact input, actual output, source/tool trace, pass/fail, then improve one observed problem and rerun. Only then claim full implementation.
5. Record the professor's answer about Option B/plugin acceptance. Keep all sources attributed and share only privately or within the assignment.

## Why not use the full dataset?
There are 106,139 original raw observations. This reproducible scope selects Store 54/Brand 6 with 121 consecutive weeks; the selection rule was based on completeness and training-period stability, not observed holdout accuracy. The models are small, deterministic, and closely aligned to Chopra Chapter 7.

## Statistical controls
- Chronological train/validation/test; rolling one-step-ahead forecasts, no lookahead.
- Validation MAD selects model. Final test metrics reported only after model selection.
- Forecast E=F-D; units and percent errors labeled clearly.
- Sales dataset week IDs have no verified calendar-date mapping in this case.
- Promotions and inventory/lead-time data are not modeled.
- The next-week forecast is NOT a procurement order recommendation.

## Academic integrity
This source bundle was developed with AI assistance. Recheck models, sources, and implementation yourself before submission. Keep human signoff. Do not invent plugin traces, source records, task results, or performance claims.
