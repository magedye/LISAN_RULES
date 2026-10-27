"""Offline integrity and completeness audit. No mutations of owner projects."""
from pathlib import Path
import csv,zipfile,json,hashlib,sys,importlib.util
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'baseline/Lisan-LibreChat-Pack-1.0.0'
ZIP=ROOT/'baseline/_original_archive/Lisan-LibreChat-Pack-1.0.0.zip'
CHECKS=[]
def run(label,ok,notes=''):
 CHECKS.append({'name':label,'result':'PASS' if ok else 'FAIL','detail':notes})
 print(('PASS ' if ok else 'FAIL ')+label+((' :: '+notes) if notes else ''))

def csv_count(name,n):
 p=ROOT/'governance/catalogs'/name
 try:
  with p.open(encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
  run('CATALOG '+name,len(rows)==n, str(len(rows))+'/'+str(n))
 except Exception as ex:run('CATALOG '+name,False,type(ex).__name__)

def main():
 manifest=json.loads((ROOT/'governance/BASELINE_IDENTITY.json').read_text('utf-8'))
 raw=ZIP.read_bytes()
 run('BASELINE ORIGINAL SHA256',hashlib.sha256(raw).hexdigest()==manifest['original_archive_sha256'])
 with zipfile.ZipFile(ZIP) as z:
  names=z.namelist(); valid=True;cnt=0
  for n in names:
   parts=Path(n).parts
   if n.startswith('/') or '..' in parts or '\\' in n:
    valid=False;continue
   if n.endswith('/'):continue
   cnt+=1
   rel='/'.join(parts[1:])
   f=BASE/rel
   if not f.is_file() or f.read_bytes()!=z.read(n):valid=False
  run('PRESERVED BASELINE CONTENT',valid,f'{cnt} files byte-identical to ZIP')
 for file,count in [('AGENTS_10.csv',10),('SKILLS_19.csv',19),('FUNCTIONS_37.csv',37),('LAYERS_30.csv',30),('AI_CAPABILITIES_38.csv',38),('GATES_13.csv',13),('ACCEPTANCE_AT_38.csv',38),('AI_EVALS_EC_42.csv',42)]:
  csv_count(file,count)
 root=ROOT/'governance/docs'
 need=['01_ARCHITECTURE_DECISION_AR.md','02_SOURCE_RECONCILIATION_AR.md',
       '03_CAPABILITIES_AND_ROLES_AR.md','04_GATES_POLICIES_AND_CONTRACTS_AR.md',
       '05_SETUP_DEPLOYMENT_AND_ROLLBACK_AR.md','06_ACCEPTANCE_AND_EVALUATION_AR.md',
       '07_WORK_PACKAGES_AND_AGENT_DIRECTIVE_AR.md','08_SECURITY_OPEN_GAPS_AR.md']
 run('REQUIRED EXECUTIVE DOCS',all((root/p).is_file() for p in need))
 skills=list((BASE/'skills').glob('*/SKILL.md'))
 run('BASELINE 19 SKILL FILES',len(skills)==19)
 yamlfile=ROOT/'governance/config/librechat.research-trial.reference.yaml'
 y=yamlfile.read_text('utf-8')
 run('RESTRICTIVE APPROVAL DEFAULT',('mode: dontAsk' in y and 'mode: default' not in y))
 run('PUBLISHER DEFAULT CLOSED',('SOURCE_RELEASE_NOT_ATTESTED' in (ROOT/'reference/lisan_gov/public_mcp.py').read_text('utf-8')))
 bad=[x for x in CHECKS if x['result']!='PASS']
 print(json.dumps({'status':'PASS' if not bad else 'FAIL','checks':len(CHECKS),'failed':len(bad)},ensure_ascii=False))
 return 1 if bad else 0
if __name__=='__main__':sys.exit(main())
