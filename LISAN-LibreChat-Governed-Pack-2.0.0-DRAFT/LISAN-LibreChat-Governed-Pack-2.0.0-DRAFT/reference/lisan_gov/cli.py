"""Read-only preflight and synthetic demonstration. No production mutation commands."""
import argparse, json, tempfile
from pathlib import Path
from .core import GateFailure,Principal,Registry,SyntheticCorpus
from .corpus_bridge import ExistingMCPReadonlyCorpus

def demo():
    researcher=Principal('demo-researcher',frozenset({'researcher'}))
    reviewer=Principal('demo-reviewer',frozenset({'reviewer'}))
    approver=Principal('demo-approver',frozenset({'approver'}))
    publisher=Principal('demo-publisher',frozenset({'publisher'}))
    with tempfile.TemporaryDirectory() as tmp:
        c=SyntheticCorpus({'DEMO:1':'مثال مصطنع أول لا ينتمي إلى القرآن',
                           'DEMO:2':'مثال مصطنع ثان لا ينتمي إلى القرآن'})
        g=Registry(Path(tmp)/'demo.db',c,allow_fixture_release=True)
        try:
            s=g.create('demo',researcher,{'kind':'EXPLICIT_REFS','refs':['DEMO:1','DEMO:2']})
            for ref,text in c.verses.items():g.observe('demo',1,researcher,ref,text,'FULL')
            g.hypothesize('demo',1,researcher,'فرضية تجريبية تخص النص المصطنع','لو وجد شاهد مضاد تسقط الفرضية','قد توجد فرضية بديلة محتملة','وجه استدلال تجريبي قابل للمراجعة')
            g.countersearch('demo',1,researcher,list(c.verses),'UNRESOLVED','فحص جميع المرجعيات المصطنعة','لا حكم دلالي خارجي من التجربة')
            g.seal('demo',1,researcher,True)
            g.review('demo',1,reviewer,'SUPPORTED','أمثلة اختبارية فقط، لا اختبار معاني قرآنية')
            g.approve('demo',1,approver,'قبول fixture اختبار حصري')
            v=g.release('demo',1,publisher,'نشر اختبار حصري')
            print(json.dumps({'demo':'SYNTHETIC_ONLY','result':v,'audit_chain_valid':g.verify_audit_chain()},ensure_ascii=False,indent=2))
        finally:g.close()

def smoke(path):
    with ExistingMCPReadonlyCorpus(path) as c:
        scope=c.scope({'kind':'FORMS','query':{'forms':['ٱللَّهُ'],'match':'TOKEN','normalization':'EXACT'}})
        verse=c.call('lisan_get_verses',{'refs':['2:157']})['verses'][0]
        assert c.verify_quote('2:157',verse['original_text'],'FULL')
        assert not c.verify_quote('2:157',verse['original_text']+' محرف','FULL')
        print(json.dumps({'status':'PASS_READONLY_BRIDGE_ONLY','corpus_id':c.corpus_id,
                          'corpus_sha256':c.corpus_sha256,'source_authenticity':c.status['provenance']['original_source_authenticity'],
                          'selector_matched_verses':scope['matched_verses'],
                          'selector_semantic_exhaustive':scope['semantic_exhaustive'],
                          'exact_quote_check':True,'tampered_quote_rejected':True,
                          'formal_semantic_acceptance':False},ensure_ascii=False,indent=2))

def main():
    ap=argparse.ArgumentParser(description='LISAN Governance reference: demo/smoke only')
    sub=ap.add_subparsers(dest='command',required=True)
    sub.add_parser('demo',help='Synthetic data isolated fixture')
    sub.add_parser('corpus-smoke',help='Read-only original MCP bridge').add_argument('--stdio',required=True)
    args=ap.parse_args()
    try:
        if args.command=='demo':demo()
        elif args.command=='corpus-smoke':smoke(args.stdio)
    except (GateFailure,AssertionError) as e:
        ap.exit(2, 'FAIL: '+str(e)+'\n')
if __name__=='__main__':main()
