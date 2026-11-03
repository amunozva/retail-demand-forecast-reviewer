"""Stateless MCP HTTP adapter. LOCAL verification does not prove ChatGPT connection.
Loopback by default. Remote use requires an authenticated TLS gateway; this adapter
checks a server-side bearer secret but does not implement ChatGPT OAuth discovery.
"""
import hmac,json,os,hashlib,math
from urllib.parse import urlsplit
from forecast_tool import oauth_auth
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from forecast_tool.engine import run,InputError,DATA
from forecast_tool.independent import verify
ROOT=Path(__file__).resolve().parents[1]
CONTRACT=json.loads((ROOT/'docs'/'tool_contract.json').read_text())
VERSIONS=['2026-07-28','2025-11-25','2025-06-18','2025-03-26']

def analyze(args):
    if not isinstance(args,dict) or set(args)-set(CONTRACT['input_schema']['properties']):
        raise ValueError('Arguments must be an object containing only documented fields.')
    if 'intent' in args and args['intent'] not in ('forecast','place_order'):
        raise ValueError('Unsupported intent.')
    if 'missing_last_week' in args and type(args['missing_last_week']) is not bool:
        raise ValueError('missing_last_week must be boolean.')
    for key in ('scenario_last_week_units','claimed_last_week_units'):
        if key in args and (type(args[key]) is not int or args[key]<0):
            raise ValueError(key+' must be a nonnegative integer.')
    before=hashlib.sha256(DATA.read_bytes()).hexdigest()
    result=run(args)
    if result['status'] in ('OK','SIMULATED'):
        # Original engine computes MA4 next-week output even if another model wins.
        # Fixed approved source selects MA4; withhold output if this ceases to hold.
        if result['selected_model']!='MA4':
            raise ValueError('Approved-case model changed. Engine next-week output needs review.')
        audit=verify()
        if not math.isclose(audit['forecast_units'],result['baseline_week_161_forecast_units'],abs_tol=1e-9) or not math.isclose(audit['holdout_MA4_MAD_units'],result['holdout_test_metrics']['MA4']['MAD_units'],abs_tol=1e-9):
            raise ValueError('Independent verification failed.')
        if result['status']=='SIMULATED':
            check=(sum(audit['last_four_units'][:3])+args['scenario_last_week_units'])/4
            if not math.isclose(check,result['forecast_units'],abs_tol=1e-9):
                raise ValueError('Scenario verification failed.')
            audit['scenario_forecast_units']=check
        result['independent_verification']=audit
        result['data_check']={'row_count':121,'store':54,'brand':6,'weeks':'40–160','units':'retail units/week','validated_by':'engine.load_sales; week sequence, IDs, positive units, log conversion and chronological splits'}
    after=hashlib.sha256(DATA.read_bytes()).hexdigest()
    if after!=before:
        raise ValueError('Source file changed during execution.')
    result['source_sha256']=before
    result['source_unchanged']=True
    result['citations']=[x.name for x in sorted((ROOT/'knowledge').iterdir()) if x.is_file()]
    return result

def dispatch(msg):
    ident=msg.get('id');method=msg.get('method');params=msg.get('params',{})
    if msg.get('jsonrpc')!='2.0':
        return {'jsonrpc':'2.0','id':ident,'error':{'code':-32600,'message':'Invalid JSON-RPC request'}}
    if 'id' not in msg:
        return None
    result=None
    if method=='server/discover':
        result={'supportedVersions':VERSIONS,'capabilities':{'tools':{}}}
    elif method=='initialize':
        requested=params.get('protocolVersion')
        result={'protocolVersion':requested if requested in VERSIONS else VERSIONS[0],'capabilities':{'tools':{}},'serverInfo':{'name':'Retail Demand Forecast Reviewer','version':'1.0.0'}}
    elif method=='ping': result={}
    elif method=='tools/list':
        result={'tools':[{'name':CONTRACT['tool_name'],'description':CONTRACT['description'],'inputSchema':CONTRACT['input_schema'],'annotations':{'readOnlyHint':True,'destructiveHint':False,'idempotentHint':True,'openWorldHint':False}}]}
    elif method=='tools/call':
        if params.get('name')!=CONTRACT['tool_name']:
            return {'jsonrpc':'2.0','id':ident,'error':{'code':-32602,'message':'Unknown tool'}}
        try:
            out=analyze(params.get('arguments',{}));failed=False
        except (InputError,ValueError,KeyError,TypeError,OSError,OverflowError) as exc:
            out={'status':'NEEDS_REVIEW','code':getattr(exc,'code','TOOL_FAILURE'),'message':str(exc),'next_step':'Correct inputs or reconcile source with the planner; no forecast is authorized.'};failed=True
        result={'content':[{'type':'text','text':json.dumps(out,allow_nan=False)}],'isError':failed}
    else:
        return {'jsonrpc':'2.0','id':ident,'error':{'code':-32601,'message':'Method not found'}}
    return {'jsonrpc':'2.0','id':ident,'result':result}

class Handler(BaseHTTPRequestHandler):
    def log_message(self,*args): pass
    def respond(self,status,data=None,headers=None):
        body=b'' if data is None else json.dumps(data).encode()
        self.send_response(status)
        self.send_header('Content-Type','application/json')
        self.send_header('Content-Length',str(len(body)))
        for key,value in (headers or {}).items():self.send_header(key,value)
        self.end_headers();self.wfile.write(body)
    def do_GET(self):
        path=urlsplit(self.path).path
        if os.getenv('MCP_AUTH_MODE')=='oauth' and path in (oauth_auth.METADATA_PATH,'/.well-known/oauth-protected-resource'):
            return self.respond(200,oauth_auth.metadata())
        if path=='/mcp':return self.respond(405,{'error':'Use POST /mcp'},{'Allow':'POST'})
        return self.respond(404)
    def do_POST(self):
        if urlsplit(self.path).path!='/mcp': return self.respond(404)
        # Browser-origin requests are unnecessary for this server-to-server tool.
        if self.headers.get('Origin'): return self.respond(403)
        if os.getenv('MCP_AUTH_MODE')=='oauth':
            if not oauth_auth.verify(self.headers.get('Authorization','')):
                return self.respond(401,{'error':'Authentication required'},
                                    {'WWW-Authenticate':oauth_auth.challenge()})
        else:
            secret=os.environ.get('MCP_BEARER_TOKEN')
            if secret and not hmac.compare_digest(self.headers.get('Authorization',''),'Bearer '+secret):
                return self.respond(401,{'error':'Authentication required'})
        try:
            length=int(self.headers.get('Content-Length','0'))
            if not 0<length<=65536: return self.respond(413)
            msg=json.loads(self.rfile.read(length))
            if not isinstance(msg,dict): return self.respond(400)
            result=dispatch(msg)
            self.respond(202 if result is None else 200,result)
        except (ValueError,TypeError,AttributeError):
            self.respond(400,{'error':'Malformed request'})

if __name__=='__main__':
    host=os.environ.get('MCP_HOST','127.0.0.1')
    if os.getenv('MCP_AUTH_MODE')=='oauth':oauth_auth.validate_config()
    elif host not in ('127.0.0.1','localhost','::1') and not os.environ.get('MCP_BEARER_TOKEN'):
        raise SystemExit('Non-loopback binding requires MCP_BEARER_TOKEN from environment.')
    ThreadingHTTPServer((host,int(os.environ.get('PORT','8080'))),Handler).serve_forever()
