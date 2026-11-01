# Retail Demand Forecast Reviewer — executable source, not a connected plugin

## Current boundary
The supplied Python engine and three knowledge files are retained unchanged. Added: a stateless HTTP MCP adapter importing engine.run, strict contract validation, independent Decimal forecast/MAD verification, source hashes, Version 1 instructions and exact live-test plan. No private ChatGPT plugin has been created; no cloud URL or installation exists.

Available supported hosting documentation specifies a JavaScript Cloudflare Worker entry point. It does not supply a verified Python runtime/deployment workflow for this engine. No alternative Python host or credentials were provided. We did not replace the Python engine with a JavaScript reimplementation or create a skills-only plugin.

## Reproduce locally
From the extracted project directory with Python 3.9+:
```
python -m unittest discover -s tests -v
python -m forecast_tool.mcp_server
```
Server binds 127.0.0.1:8080; POST JSON-RPC to /mcp. Example:
```
curl http://127.0.0.1:8080/mcp -H 'Content-Type: application/json' -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"analyze_orange_juice_demand","arguments":{}}}'
```
Run `python tests/run_adapter_checks.py` separately: it starts its own ephemeral local server, records five real HTTP tool responses plus independent audit, and marks all evidence LOCAL_HTTP_ONLY. It does not exercise an LLM or prove the plugin is selectable in ChatGPT.

## Deployment preparation, not deployment
Dockerfile is provided for a future approved Python host. Docker image build has not been tested here. Set MCP_BEARER_TOKEN only through the host's secret manager, never archive it. Non-loopback binding fails without that secret. Put this development HTTP adapter behind a production authenticated TLS gateway with timeouts and request limits. Its bearer check is not a complete OAuth implementation. Verify the chosen ChatGPT connector's supported authentication and MCP transport before connecting. Do not publish an unauthenticated endpoint.

Host must execute `python -m forecast_tool.mcp_server` with bundled knowledge and docs/tool_contract.json, and expose HTTPS /mcp to the authorized owner. Then create one PRIVATE plugin connected to that verified endpoint, install it, and invoke the actual tool in ChatGPT. No MCP URL is asserted in this package. Local protocol coverage includes discovery, initialization, tool list/call and ping; full hosted interoperability is unverified.

## Known source issues preserved transparently
- engine.run always produces MA4's next forecast even if another candidate were selected. The adapter withholds output if selection ceases to be MA4; approved data selects MA4.
- Original `independent_check` only repeats the mean. New `independent_verification` independently recomputes the forecast and holdout MAD using week-keyed Decimal data without engine imports.
- Engine computes holdout metric objects before executing its validation-only selection statement. Holdout is not an input to selection, but literal execution order differs from the requested select-then-evaluate sequence. Preserved source is not claimed to meet that procedural requirement; reorder only in a reviewed engine revision before final live acceptance.
- Supplied independent script expects a same-folder CSV, includes the seasonal diagnostic in its selection set, and references an absent workbook. It is retained as supplied historical evidence, not used by the adapter. New audit is separate.

## Gates and next steps
1. Hosted selectable tool: NOT MET.
2. Observed ChatGPT analytical invocation: NOT MET. Local HTTP invocation is separate evidence.
3. Five live agent tests: NOT RUN; use exact saved test plan.
4. Evidence-based Version 2 and affected live rerun: NOT DONE. Do not manufacture a revision before live results.
5. Source reproduction: local instructions, code, hashes and test evidence supplied; hosted reproduction and supporting workbook remain pending.
6. Instructor Option B approval: PENDING; only instructor can grant it.

No report or demo is represented as submission-ready. Use the preparation outline, then fill genuine live evidence and instructor decision.
