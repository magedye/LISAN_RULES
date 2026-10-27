import unittest, os, json, subprocess, sys, tempfile
from pathlib import Path

class PublicMCPProtocolTests(unittest.TestCase):
 def start(self,db=None):
  env=os.environ.copy();env.pop('LISAN_PUBLICATION_SOURCE_ACCEPTED',None)
  env['LISAN_GOV_DB']=db or '/DOES_NOT_EXIST_FOR_THIS_TEST.db'
  return subprocess.Popen([sys.executable,'-m','lisan_gov.public_mcp'],env=env,
                          stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                          text=True,bufsize=1)
 def request(self,p,x):
  p.stdin.write(json.dumps(x)+'\n');p.stdin.flush()
  return json.loads(p.stdout.readline())
 def test_52_publication_service_defaults_no_acceptance(self):
  p=self.start()
  try:
   a=self.request(p,{'jsonrpc':'2.0','id':1,'method':'initialize','params':{'protocolVersion':'2025-11-25'}})
   self.assertEqual(a['result']['serverInfo']['name'],'lisan-publication-readonly-reference')
   b=self.request(p,{'jsonrpc':'2.0','id':2,'method':'tools/call','params':{'name':'lisan_get_released_finding','arguments':{'study_id':'x'}}})
   self.assertTrue(b['result']['isError'])
   self.assertEqual(b['result']['structuredContent']['status'],'SOURCE_RELEASE_NOT_ATTESTED')
  finally:
   p.terminate();p.wait(timeout=5)
   for h in (p.stdin,p.stdout,p.stderr):h.close()
 def test_53_publication_tool_list_has_no_writes(self):
  p=self.start()
  try:
   self.request(p,{'jsonrpc':'2.0','id':1,'method':'initialize','params':{'protocolVersion':'2025-11-25'}})
   r=self.request(p,{'jsonrpc':'2.0','id':2,'method':'tools/list','params':{}})
   tools=[x['name'] for x in r['result']['tools']]
   self.assertEqual(set(tools),{'lisan_publication_status','lisan_get_released_finding'})
  finally:
   p.terminate();p.wait(timeout=5)
   for h in (p.stdin,p.stdout,p.stderr):h.close()
 def test_54_tool_without_initialization_rejected(self):
  p=self.start()
  try:
   r=self.request(p,{'jsonrpc':'2.0','id':1,'method':'tools/list','params':{}})
   self.assertTrue(r['result']['isError']);self.assertEqual(r['result']['structuredContent']['status'],'NOT_INITIALIZED')
  finally:
   p.terminate();p.wait(timeout=5)
   for h in (p.stdin,p.stdout,p.stderr):h.close()
