# BIA 674 Individual Midterm — Rubric acceptance checklist

This checklist is a project implementation aid, not instructor approval or an assessment grade. Original assignment is authoritative.

| Rubric criterion | Points | Evidence required | Current status |
|---|---:|---|---|
| Problem and course application | 15 | Named retail supply-chain planner, one-week demand decision, constraints, 16-week out-of-sample success criterion, Module 6/Ch7 connection | Scenario and local measures defined; final written evidence pending |
| Knowledge base and data quality | 15 | >=3 files including real structured CSV and policy/SOP; inventory with source/version/units/missing/updates/conflict handling | Files available locally; connected plugin ingestion pending |
| Instructions and system design | 20 | Exact instructions, tool definitions, agent step/order, actual validation/retry/stop/human-review rules, architecture | Source and architecture drafted; installed tool pending |
| Working prototype and analytics | 20 | ChatGPT-connected runnable tool, demonstrated forecast, accurate formulas, independent Excel/Python verification | Local tool tests pass; in-ChatGPT tool unverified |
| Testing and improvement | 20 | Five required live categories with expected vs actual, traces, pass/fail, initial version, justified change and rerun | Local unit tests exist; no live ChatGPT plugin evidence or before/after yet |
| Video and submission quality | 10 | Clear 10–15 minute narrated screen demo of actual execution, 4–6 page report, complete reproducible package, appendix and disclosure | Not yet complete |
| **Total** | **100** | Never promise perfect grading | |

## Core data and analysis evidence
- Dataset: selected 121 real weekly observations for Store 54, Brand 6, week IDs 40–160.
- Split: train 40–128; validation 129–144; holdout 145–160.
- Comparator: naive, MA4, SES (alpha .1), Holt (alpha .1, beta .2).
- Model selection: **validation MAD**, not lowest holdout metric.
- Confirm against independently produced artifacts: selected MA4; forecast week 161 = 3,408 units; holdout MAD MA4 588, naive 768; MAPE MA4 ~20.89%, Holt ~19.45%.
- Explicitly label simulations and unsupported assumptions.

## Required test evidence fields
Test ID; prompt; expected behavior and pass criteria defined before running; actual user-visible response; source/tool invocation trace; quantitative independent check when relevant; pass/fail; explanation; unresolved risks.

## Honest status note
A ZIP containing a working Python script is not by itself proof of a working ChatGPT-connected agentic prototype. Real invocation, five actual test runs, improvement/retest and a screen recording are still needed. Instructor approval of the plugin substitution is pending.
