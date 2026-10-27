"""Read-only MCP publication adapter (illustrative, NOT a production auth boundary).

Only returns a RELEASED current revision whose immutable record and approvals match.
Disabled by default. Do not load as a public MCP server until source authority,
principal isolation, storage and release authentication have been independently tested.
"""
from __future__ import annotations
import json, os, re, sqlite3, sys
from .core import digest, GateFailure

TOOLS=[
 {'name':'lisan_publication_status','description':'Read-only governance status; not semantic acceptance.',
  'inputSchema':{'type':'object','properties':{},'additionalProperties':False}},
 {'name':'lisan_get_released_finding','description':'Read only a formally released current finding by ID. Cannot approve or edit.',
  'inputSchema':{'type':'object','properties':{'study_id':{'type':'string','minLength':1,'maxLength':128}},
                 'required':['study_id'],'additionalProperties':False}}
]

def fetch_public(dbpath: str, study_id: str, source_accepted: bool, expected_corpus_sha256: str=''):
    if not source_accepted: raise GateFailure('SOURCE_RELEASE_NOT_ATTESTED')
    if not re.fullmatch(r'[a-f0-9]{64}',expected_corpus_sha256):
        raise GateFailure('PINNED_CORPUS_IDENTITY_REQUIRED')
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]{0,127}',study_id):
        raise GateFailure('INVALID_STUDY_ID')
    con=sqlite3.connect('file:'+os.path.abspath(dbpath)+'?mode=ro',uri=True)
    con.row_factory=sqlite3.Row
    try:
        st=con.execute('SELECT active_rev FROM studies WHERE id=?',(study_id,)).fetchone()
        if not st:raise GateFailure('STUDY_NOT_FOUND')
        rev=st['active_rev']
        blocked=con.execute('SELECT 1 FROM invalidations WHERE id=?',(study_id,)).fetchone()
        if blocked:raise GateFailure('NEEDS_REVALIDATION')
        r=con.execute('SELECT * FROM revisions WHERE id=? AND rev=?',(study_id,rev)).fetchone()
        if not r or r['phase']!='SEALED' or not r['sealed_digest']:raise GateFailure('OUTPUT_WITHHELD')
        d=json.loads(r['data'])
        if digest(d)!=r['sealed_digest']:raise GateFailure('LOCK_TAMPER_DETECTED')
        if d['scope']['corpus_sha256']!=expected_corpus_sha256:
            raise GateFailure('CORPUS_PIN_CHANGED')
        v={row['kind']:row for row in con.execute('SELECT * FROM decisions WHERE id=? AND rev=?',(study_id,rev))}
        for name,expected in [('review','SUPPORTED'),('approval','ACCEPTED'),('release','RELEASED')]:
            if name not in v or v[name]['decision']!=expected or v[name]['snapshot_digest']!=r['sealed_digest']:
                raise GateFailure('OUTPUT_WITHHELD')
        if d['scope']['source_authenticity']=='SYNTHETIC_TEST_ONLY':
            raise GateFailure('SYNTHETIC_SOURCE_NEVER_PUBLIC')
        return {'study_id':study_id,'revision':rev,'status':'RELEASED',
                'hypothesis':d['hypothesis']['statement'],
                'scope':d['scope'],'countersearch':d['countersearch'],
                'limitations':d.get('limitations',[]),'sealed_digest':r['sealed_digest'],
                'notice':'نتيجة مراجعة معتمدة في نطاقها؛ لا تثبت يقينًا دلاليًا مطلقًا.'}
    finally:con.close()

def serve(dbpath,source_accepted=False,expected_corpus_sha256=''):
    initialized=False
    for line in sys.stdin:
        mid=None
        try:
            req=json.loads(line)
            if not isinstance(req,dict) or req.get('jsonrpc')!='2.0':
                raise GateFailure('INVALID_REQUEST')
            mid=req.get('id')
            method=req.get('method')
            if mid is None:
                if method=='notifications/initialized' and initialized:continue
                continue
            args=req.get('params') or {}
            if method=='initialize':
                if args.get('protocolVersion') not in {'2025-11-25','2025-06-18'}:
                    raise GateFailure('UNSUPPORTED_PROTOCOL_VERSION')
                initialized=True
                result={'protocolVersion':args['protocolVersion'],'capabilities':{'tools':{}},
                        'serverInfo':{'name':'lisan-publication-readonly-reference','version':'0.1'},
                        'instructions':'Publication is not available unless source and governance have been approved outside the model.'}
            elif not initialized:raise GateFailure('NOT_INITIALIZED')
            elif method=='tools/list':result={'tools':TOOLS}
            elif method=='tools/call':
                name=args.get('name');kwargs=args.get('arguments') or {}
                if name=='lisan_publication_status' and not kwargs:
                    value={'ready':bool(dbpath and os.path.isfile(dbpath)),'source_release_attested':source_accepted,
                           'note':'Read only; no approval tools. Not a semantic oracle.'}
                elif name=='lisan_get_released_finding' and set(kwargs)=={'study_id'}:
                    value=fetch_public(dbpath,kwargs['study_id'],source_accepted,expected_corpus_sha256)
                else:raise GateFailure('UNKNOWN_TOOL_OR_ARGUMENTS')
                result={'content':[{'type':'text','text':json.dumps(value,ensure_ascii=False)}],
                        'structuredContent':value,'isError':False}
            elif method=='ping':result={}
            else:raise GateFailure('METHOD_NOT_FOUND')
            response={'jsonrpc':'2.0','id':mid,'result':result}
        except (GateFailure,ValueError,sqlite3.Error,TypeError,KeyError) as e:
            # No raw SQL error/arguments/paths in tool output.
            code=e.code if isinstance(e,GateFailure) else 'READONLY_SERVICE_ERROR'
            response={'jsonrpc':'2.0','id':locals().get('mid',None),'result':{'content':[{'type':'text','text':code}],
                'structuredContent':{'status':code},'isError':True}}
        print(json.dumps(response,ensure_ascii=False,separators=(',',':')),flush=True)

if __name__=='__main__':
    p=os.getenv('LISAN_GOV_DB','')
    # Environment variables represent operator-controlled config, not identity proof.
    accepted=os.getenv('LISAN_PUBLICATION_SOURCE_ACCEPTED')=='1'
    pinned=os.getenv('LISAN_PUBLISHED_CORPUS_SHA256','')
    serve(p,accepted,pinned)
