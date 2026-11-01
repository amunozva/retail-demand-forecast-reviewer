FROM python:3.12-slim
WORKDIR /app
COPY forecast_tool ./forecast_tool
COPY knowledge ./knowledge
COPY docs/tool_contract.json ./docs/tool_contract.json
USER 65534:65534
ENV PYTHONDONTWRITEBYTECODE=1 MCP_HOST=0.0.0.0 PORT=8080
EXPOSE 8080
CMD ["python", "-m", "forecast_tool.mcp_server"]
