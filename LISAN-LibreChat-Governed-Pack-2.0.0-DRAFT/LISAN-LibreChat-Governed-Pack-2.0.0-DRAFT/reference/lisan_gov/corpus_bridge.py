"""Read-only transport adapter for preserved Lisan candidate MCP stdio server.

This adapter NEVER interprets corpus provenance as formal source release approval.
It is optional; it is not an implementation of a root/lemma semantic census.
"""
from __future__ import annotations
import json, subprocess, queue, threading, itertools
from pathlib import Path
from .core import GateFailure, canon, digest

class ExistingMCPReadonlyCorpus:
    def __init__(self, script: str, node='node', timeout=75):
        if not Path(script).is_file(): raise GateFailure('STDIO_SCRIPT_NOT_FOUND')
        self.proc=subprocess.Popen([node,str(Path(script).resolve())],stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,
                                   bufsize=1,text=True,encoding='utf-8')
        self.pending=queue.Queue()
        self.timeout=timeout
        self.ids=itertools.count(1)
        self.thread=threading.Thread(target=self._reader,daemon=True)
        self.thread.start()
        self._request('initialize',{'protocolVersion':'2025-11-25','clientInfo':{'name':'lisan-governance-readonly-adapter','version':'0.1'},'capabilities':{}})
        self._send({'jsonrpc':'2.0','method':'notifications/initialized'})
        self.status=self.call('lisan_status',{})
        if not self.status.get('ready') or self.status.get('status')!='READY_FOR_CORPUS_OPERATIONS':
            raise GateFailure('CORPUS_NOT_READY')
        self.corpus_id=self.status['provenance']['corpus_id']
        self.corpus_sha256=self.status['provenance']['corpus_sha256']
    def _reader(self):
        while True:
            line=self.proc.stdout.readline()
            if not line: break
            try:self.pending.put(json.loads(line))
            except json.JSONDecodeError: self.pending.put({'error':{'message':'MALFORMED_MCP_RESPONSE'}})
    def _send(self,obj):
        if self.proc.poll() is not None: raise GateFailure('MCP_PROCESS_EXITED')
        self.proc.stdin.write(canon(obj)+'\n')
        self.proc.stdin.flush()
    def _request(self,method,params):
        n=next(self.ids)
        self._send({'jsonrpc':'2.0','id':n,'method':method,'params':params})
        try:r=self.pending.get(timeout=self.timeout)
        except queue.Empty:raise GateFailure('MCP_TIMEOUT')
        if r.get('id')!=n: raise GateFailure('MCP_RESPONSE_ID_MISMATCH')
        if 'error' in r: raise GateFailure('MCP_ERROR_'+str(r['error'].get('message','ERROR')))
        return r['result']
    def call(self,tool,args):
        result=self._request('tools/call',{'name':tool,'arguments':args})
        structured=result.get('structuredContent')
        if not isinstance(structured,dict): raise GateFailure('STRUCTURED_RESPONSE_REQUIRED')
        if result.get('isError'): raise GateFailure('CORPUS_TOOL_'+str(structured.get('status','FAILED')))
        return structured
    def scope(self,selector):
        if set(selector)!={'kind','query'} or selector['kind']!='FORMS':
            raise GateFailure('SELECTOR_UNSUPPORTED')
        q=selector['query']
        if set(q)!={'forms','match','normalization'} or not isinstance(q['forms'],list) or not q['forms']:
            raise GateFailure('INVALID_QUERY')
        offset=0;found=[];fingerprint=None;first=None
        while True:
            r=self.call('lisan_search',{'query':q,'offset':offset,'limit':50})
            if r.get('scan')!='COMPLETE_FOR_DECLARED_QUERY' or r.get('status')!='OK':
                raise GateFailure('DECLARED_SEARCH_NOT_COMPLETE')
            if r['provenance']['corpus_sha256']!=self.corpus_sha256:
                raise GateFailure('CORPUS_PIN_CHANGED')
            if first is None: first=r
            if fingerprint is None: fingerprint=r['query_fingerprint']
            if fingerprint!=r['query_fingerprint']: raise GateFailure('QUERY_FINGERPRINT_CHANGED')
            found.extend(x['ref'] for x in r['occurrences'])
            if r['page']['next_offset'] is None:break
            offset=r['page']['next_offset']
            if offset>6236: raise GateFailure('PAGINATION_BUDGET')
        if len(set(found))!=len(found) or len(found)!=first['matched_verses']:
            raise GateFailure('CORPUS_PAGINATION_INCONSISTENT')
        return {'refs':found,'corpus_id':self.corpus_id,'corpus_sha256':self.corpus_sha256,
                'selector_digest':fingerprint,'exhaustive_for_selector':True,
                'semantic_exhaustive':False,
                'source_authenticity':self.status['provenance'].get('original_source_authenticity','NOT_VERIFIED'),
                'count_unit':'VERSES','matched_verses':first['matched_verses'],
                'match_events':first['match_events']}
    def verify_quote(self,ref,text,kind):
        try:
            r=self.call('lisan_verify_quote',{'ref':ref,'text':text,'kind':kind})
            return r.get('matched') is True and r.get('status')=='QUOTE_EXACT_MATCH' and r['provenance']['corpus_sha256']==self.corpus_sha256
        except GateFailure as e:
            if 'QUOTE_NOT_VERIFIED' in e.code:return False
            raise
    def close(self):
        if self.proc.poll() is None:
            try:self.proc.stdin.close()
            except Exception:pass
            self.proc.terminate()
            try:self.proc.wait(timeout=3)
            except subprocess.TimeoutExpired:self.proc.kill()
    def __enter__(self):return self
    def __exit__(self,*a):self.close()
