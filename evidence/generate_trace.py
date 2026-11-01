"""Generate truthfully labeled LOCAL ENGINE traces; NOT ChatGPT agent traces."""
from pathlib import Path
import json, sys, datetime
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from forecast_tool.engine import run
cases={
 'T1_typical':{},
 'T2_changed_conditions':{'scenario_last_week_units':6000},
 'T3_missing_info':{'missing_last_week':True},
 'T4_conflict':{'claimed_last_week_units':9000},
 'T5_unsupported':{'intent':'place_order'}
}
results={k:{'request':v,'actual_engine_output':run(v)} for k,v in cases.items()}
path=Path(__file__).with_name('LOCAL_ENGINE_TRACE_NOT_PLUGIN.json')
path.write_text(json.dumps({'evidence_type':'local deterministic calculation tool execution only',
 'not_plugin_execution':True,'cases':results},indent=2))
print('Wrote', path.name, 'with',len(results),'genuine local engine test outcomes')
