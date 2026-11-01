"""Local HTTP checks: no installed ChatGPT plugin or LLM exercised."""
import sys,json,threading,urllib.request
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from forecast_tool.mcp_server import Handler,ThreadingHTTPServer
from forecast_tool.independent import verify
plan=json.loads((ROOT/'evidence/BIA674_Midterm_Munoz_Live_Test_Plan.json').read_text())
server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
threading.Thread(target=server.serve_forever,daemon=True).start()
def post(body):
 req=urllib.request.Request('http://127.0.0.1:%s/mcp'%server.server_port,data=json.dumps(body).encode(),headers={'Content-Type':'application/json'})
 with urllib.request.urlopen(req,timeout=5) as r:return json.load(r)
results=[]
try:
 protocol=[]
 for method,params in [('server/discover',{}),('initialize',{'protocolVersion':'2025-03-26'}),('tools/list',{}),('ping',{})]:
  call={'jsonrpc':'2.0','id':method,'method':method,'params':params}
  out=post(call);assert 'result' in out
  protocol.append({'request':call,'response':out})
 assert protocol[2]['response']['result']['tools'][0]['name']=='analyze_orange_juice_demand'
 for index,test in enumerate(plan):
  call={'jsonrpc':'2.0','id':test['test_id'],'method':'tools/call','params':{'name':'analyze_orange_juice_demand','arguments':test['tool_arguments']}}
  raw=post(call);out=json.loads(raw['result']['content'][0]['text'])
  checks={'expected_status':out['status']==['OK','SIMULATED','NEEDS_INPUT','NEEDS_RECONCILIATION','BLOCKED'][index],'not_tool_error':raw['result']['isError'] is False,'source_unchanged':out['source_unchanged']}
  if index==0:
   checks.update(selected_MA4=out['selected_model']=='MA4',forecast_3408=out['forecast_units']==3408,holdout_MAD_588=out['holdout_test_metrics']['MA4']['MAD_units']==588,naive_MAD_768=out['holdout_test_metrics']['Naive']['MAD_units']==768,independent_MAD=out['independent_verification']['holdout_MA4_MAD_units']==588,human_review=out['human_approval_required'])
  elif index==1:checks.update(scenario_4284=out['forecast_units']==4284,original_2496=out['actual_week_160_units']==2496,baseline_3408=out['baseline_week_161_forecast_units']==3408)
  else:checks['forecast_withheld']='forecast_units' not in out
  results.append({'test_id':test['test_id'],'timestamp_utc':datetime.now(timezone.utc).isoformat(),'evidence_type':'LOCAL_HTTP_ONLY','exact_planned_prompt_not_sent_to_LLM':test['prompt'],'expected_behavior':test['expected_behavior'],'request':call,'response':raw,'checks':checks,'local_adapter_pass':all(checks.values()),'live_agent_pass_fail':'NOT RUN','actual_agent_response':None,'discrepancy':'No installed ChatGPT plugin or LLM interpretation exercised.'})
 malformed={'jsonrpc':'2.0','id':'invalid','method':'tools/call','params':{'name':'analyze_orange_juice_demand','arguments':{'missing_last_week':'false'}}}
 invalid=post(malformed);assert invalid['result']['isError']
 evidence={'scope':'Local HTTP MCP adapter only; NOT live ChatGPT tests','protocol_checks':protocol,'tests':results,'invalid_input_check':{'request':malformed,'response':invalid},'independent_audit':verify()}
 (ROOT/'evidence/BIA674_Midterm_Munoz_Local_HTTP_Evidence.json').write_text(json.dumps(evidence,indent=2))
 assert all(x['local_adapter_pass'] for x in results)
 print('PASS: discovery, initialize, tools/list, ping, five LOCAL HTTP cases, strict boolean rejection, separate forecast/MAD verification. LIVE CHATGPT TESTS: NOT RUN.')
finally:
 server.shutdown();server.server_close()
