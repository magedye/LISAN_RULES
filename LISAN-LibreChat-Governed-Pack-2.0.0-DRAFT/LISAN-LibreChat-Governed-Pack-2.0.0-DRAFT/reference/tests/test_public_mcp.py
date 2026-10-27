import tempfile, unittest
from pathlib import Path
from lisan_gov import Registry,SyntheticCorpus,Principal,GateFailure
from lisan_gov.public_mcp import fetch_public

class PublicTests(unittest.TestCase):
 def setUp(self):
  self.t=tempfile.TemporaryDirectory()
  self.db=str(Path(self.t.name)/'fixture.db')
  self.c=SyntheticCorpus({'X:1':'نص مصطنع تجريبي'})
  self.r=Registry(self.db,self.c,allow_fixture_release=True)
  a=Principal('a',frozenset({'researcher'}));b=Principal('b',frozenset({'reviewer'}))
  c=Principal('c',frozenset({'approver'}));d=Principal('d',frozenset({'publisher'}))
  self.r.create('fixture',a,{'kind':'EXPLICIT_REFS','refs':['X:1']})
  self.r.observe('fixture',1,a,'X:1','نص مصطنع تجريبي','FULL')
  self.r.hypothesize('fixture',1,a,'فرضية تجربة طويلة','شرط قابل للتكذيب','تفسير آخر محتمل','وجه استدلال تجريبي فقط')
  self.r.countersearch('fixture',1,a,['X:1'],'UNRESOLVED','تم الفحص محليًا','بحث مصطنع لا يحتج به')
  self.r.seal('fixture',1,a,True)
  self.r.review('fixture',1,b,'SUPPORTED','مراجعة مثال')
  self.r.approve('fixture',1,c,'قبول مثال')
  self.r.release('fixture',1,d,'نشر مثال محلي')
 def tearDown(self):self.r.close();self.t.cleanup()
 def test_readonly_mcp_denies_without_source_attestation(self):
  with self.assertRaises(GateFailure) as e:fetch_public(self.db,'fixture',False)
  self.assertEqual(e.exception.code,'SOURCE_RELEASE_NOT_ATTESTED')
 def test_readonly_mcp_never_serves_synthetic_even_if_accepted(self):
  with self.assertRaises(GateFailure) as e:fetch_public(self.db,'fixture',True,self.c.corpus_sha256)
  self.assertEqual(e.exception.code,'SYNTHETIC_SOURCE_NEVER_PUBLIC')
 def test_bad_id_rejected(self):
  with self.assertRaises(GateFailure) as e:fetch_public(self.db,'../../passwd',True,self.c.corpus_sha256)
  self.assertEqual(e.exception.code,'INVALID_STUDY_ID')

