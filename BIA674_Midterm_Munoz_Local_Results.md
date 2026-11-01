# Locally observed results — NOT ChatGPT plugin evidence

Local engine: 6/6 tests passed. Local HTTP MCP adapter: five scenario cases passed, plus discovery, initialization, tool list, ping and invalid-boolean rejection. No LLM test or private cloud deployment occurred.

| Method | Validation MAD | Holdout MAD | Holdout MSE | Holdout MAPE % | Holdout bias |
|---|---:|---:|---:|---:|---:|
| Naive | 1656.00 | 768.00 | 861696.00 | 27.12 | 108.00 |
| MA4 | 1141.50 | 588.00 | 492408.00 | 20.89 | 93.00 |
| SES | 1389.23 | 641.62 | 681904.74 | 24.38 | 481.25 |
| Holt | 1407.65 | 590.37 | 461381.11 | 19.45 | -168.27 |

Independent Decimal check: (3456 + 3552 + 4128 + 2496) / 4 = 3,408 retail units. Holdout MA4 absolute errors sum to 9,408; divide by 16 = 588 units.

Scenario week 160 = 6,000 gives 4,284 units, up 876. Original file SHA-256 remains unchanged. Holdout MA4 MAD reduction versus naive: (768 − 588) / 768 × 100 = 23.4375%. This is retrospective error reduction, not operational savings. Holt has lower holdout MAPE. Human review is required.

Full validation and holdout metrics, exact HTTP requests and responses, audit rows, and pass judgments are in evidence/BIA674_Midterm_Munoz_Local_HTTP_Evidence.json. All live ChatGPT results remain NOT RUN.