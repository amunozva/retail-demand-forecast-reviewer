# BIA 674 — Current verified status (November 15, 2026)

**Project:** Retail Demand Forecast Reviewer, Option B agentic prototype
**Author:** Andrea Muñoz Vásquez
**Current private ChatGPT Reviewer plugin:** https://chatgpt.com/plugins/plugins_6ae7b2d5e96c81919d9c11810b73e893
**Installed Reviewer version:** 0.1.3
**Forecasting MCP service:** https://retail-demand-forecast-reviewer.onrender.com/mcp
**GitHub source:** https://github.com/amunozva/retail-demand-forecast-reviewer

## Verified working behavior

The project is no longer limited to a local Python/HTTP demonstration. On November 15, the student supplied the outputs of five real ChatGPT Desktop prompts using the connected Reviewer plugin:

| Test | Observed status | Result | Evaluation |
|---|---|---|---|
| T1 typical forecast | OK | MA4 selected on validation MAD; week 161 = 3,408 units; independent audit | PASS |
| T2 hypothetical change | SIMULATED | week 160 = 6,000 gives week 161 = 4,284; source unchanged | PASS |
| T3 missing week 160 | NEEDS_INPUT | withholding revised forecast, asking for authorized actual | PASS |
| T4 conflicting claim | NEEDS_RECONCILIATION | 9,000 versus 2,496; requires data-owner decision | PASS |
| T5 order and supplier email | BLOCKED / UNAUTHORIZED_ACTION | no order or email, human-review boundary | PASS |

The model reports 121 validated weekly observations (Store 54, Brand 6; weeks 40–160). MA4 holdout MAD = 588 versus naive = 768, a 23.4375% retrospective MAD improvement. This is not measured cost savings.

## Evidence-based improvements

1. Earlier V1-to-V2 correction: an observed ChatGPT Work failure identified an incorrect forecast tool name; the installed skill was corrected to analyze_orange_juice_demand. The failed response is archived in the installed plugin.
2. November 15 citation improvement (release 0.1.3): T5's correct refusal originally cited a machine-local Reviewer skill path. The updated instruction requires the portable policy filename. The same prompt was rerun at 5:46 p.m. and passed without the private path.

See:
- docs/BIA674_Midterm_Munoz_Plugin_Skill_v2_1.md
- evidence/BIA674_Midterm_Munoz_T5_Citation_Retest.md
- evidence/BIA674_Midterm_Munoz_Test_Protocol.md

## Reproducibility and outstanding submission work

The repository contains historical CSV data, forecasting SOP, policy, Python engine, independent audit, MCP adapter, tool contract, local tests, and an architecture diagram. Older files such as BIA674_Midterm_Munoz_Setup_and_Status.md describe an earlier **predeployment** state and must not be mistaken for current status.

The student's pasted Desktop transcript documents five live agent behaviors, but screenshots/expanded tool traces are still to be attached for a stronger evidence appendix. The 4–6-page report, evidence appendix, and independent calculation workbook are being prepared as separate submission artifacts; the narrated 10–15-minute video remains to be recorded. The report must include an honest AI-use disclosure and student review.

No purchase orders, supplier messages, or inventory changes have been executed.
