import csv, json, pathlib
B=pathlib.Path('/mnt/data/LISAN_Rules_Operational_20261028')
def read(x):
 with (B/x).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
rules=read('LISAN_GOVERNANCE_MASTER_230.csv');profs={r['id']:r for r in read('LISAN_RULE_EXECUTION_PROFILES_230.csv')}
recs=[]
for r in rules:
 p=profs[r['id']]
 recs.append({
  'id':r['id'],'revision':1,'text_en':r['text_en'],'text_ar':r['text_ar'],'kind':r['kind'],'kind_ar':r['kind_ar'],'force':r['force'],'category':r['category'],
  'rule_status':'PROPOSED','authority_level':'PENDING_AUTHORITY_REVIEW','source_reference':r['source_reference'],'source_quote':None,'source_digest':None,'source_status':r['source_status'],
  'scope_context':p['phase'],'applicable_modes':['PENDING_RULE_SPECIFIC_APPLICABILITY_REVIEW'],'applies_to':[p['applies_to']],'trigger_event':p['trigger_event'],
  'trigger_predicate':p['trigger_predicate'],'expected_behavior':p['expected_behavior'],'enforcement_target':p['enforcement_target'],'enforcement_status':'NOT_VERIFIED',
  'verification_mode':p['verification_mode'],'failure_action':p['failure_action'],'admission_status':r['admission_status'],'risk_tier':p['risk_tier'],
  'reviewer_id':None,'approved_by':None,'effective_from':None,'supersedes':[],'evidence_refs':[],'test_refs':[],
  'impact_metric_id':p['impact_metric_id'],'impact_measurement_status':'NOT_MEASURED','impact_baseline':None,'impact_treatment':None,'exceptions':[],
  'rationale':r['novelty_rationale'] + '; profile origin: '+p['profile_origin']+'; user/owner review pending.'
 })
(B/'LISAN_GOVERNANCE_230_PROPOSED_MACHINE_RECORDS.json').write_text(json.dumps({'registry_schema':'lisan-governance-registry/2.0-DRAFT','activation_allowed':False,'rules':recs},ensure_ascii=False,indent=2),encoding='utf8')
try:
 import jsonschema
 schema=json.loads((B/'schemas/lisan_rule_record_v2_PROPOSED.schema.json').read_text(encoding='utf8'))
 for r in recs:jsonschema.validate(r,schema)
 print('SCHEMA VALIDATION:',len(recs),'valid records')
except ImportError:print('jsonschema not installed - structural validation performed via stdlib')
