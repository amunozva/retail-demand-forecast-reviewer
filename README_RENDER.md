# Retail Demand Forecast Reviewer — Render deployment kit (PRE-DEPLOYMENT)

This repository preserves the executable original Python MCP adapter, independent audit,
three knowledge files, six local unit tests, and five local HTTP checks.
It has **not** been deployed or connected to ChatGPT. It is not a finished Option B submission.

## 1. Verify first

From the repository root using Python 3.9+:

```bash
python -m unittest discover -s tests -v
python tests/run_adapter_checks.py
```

Expected local numeric checks: MA4 next-week forecast 3,408 units; 16-week test
MAD 588 units versus naive 768 units. These numbers are NOT hardcoded as outputs.

## 2. Host via Render (repo required)

1. Put the CONTENTS of this directory (Dockerfile and render.yaml at repository root)
   in a new **private GitHub repository**. Never commit .env or secrets.
2. Grant Render access to this private repository if required.
3. In Render create a new Web Service using that repository (Docker runtime),
   or create a Blueprint from render.yaml. Select a suitable plan and review any costs.
4. Set MCP_BEARER_TOKEN to a strong unique secret through Render's secret/environment
   settings, not via source code. The adapter refuses to start on 0.0.0.0 without it.
5. Confirm deploy succeeds and service HTTPS address is provided by Render.
6. Test authentication from an authorized environment. A missing or bad token must
   return 401; a valid token should return MCP initialize and tools/list results.
7. Save the genuine hosted tool responses and source version as evidence.

Note: Render's Create Web Service connection requires a deployable Git URL; this ZIP
is NOT directly deployed through the ChatGPT Render connector.

## 3. IMPORTANT ChatGPT connection blocker

The adapter supports a fixed `Authorization: Bearer ...` server-side secret but
**does not implement OAuth 2.1**. ChatGPT's plugin connection form may not support
entering a fixed bearer/API key. Hosting does NOT automatically make the tool
selectable in ChatGPT. Verify a supported authentication/connection route **before**
representing the plugin as finished. Possible documented alternatives include an
approved Secure MCP Tunnel, or a correctly implemented OAuth 2.1 gateway.
Do NOT disable authentication solely to make the connection succeed: the requested
project is private. If public anonymous read-only hosting is ever considered,
obtain the user's explicit approval and check redistribution requirements first.

### MCP tool contract

POST /mcp, JSON-RPC 2.0; tool: analyze_orange_juice_demand.
The server is read-only; it never orders stock or communicates with suppliers.
The server has no exposed GET /mcp SSE endpoint; MCP client interoperability
needs testing against the exact ChatGPT connection method.

## 4. Completion requirements (not yet achieved)

- A live connected tool actually invoked by ChatGPT.
- Five live agent tests with input/expected/actual/evidence/pass or fail.
- Evidence-based Version 2 change and affected test rerun.
- Independent numerical verification; reproducible submission package.
- Instructor approval for Option B plugin form, report, 10–15 minute demo.

Retain Version 1 documentation before any changes; do not fabricate traces.
