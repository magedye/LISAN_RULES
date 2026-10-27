from pathlib import Path
import csv,collections,re
from artifact_tool import Blob, SpreadsheetFile
B=Path('/mnt/data/LISAN_Rules_Operational_20261028')
SRC=Path('/mnt/data/LISAN_GOVERNING_RULES_190_EXPANDED.xlsx')
DEST=Path('/mnt/data/LISAN_GOVERNANCE_OPERATIONAL_REGISTER_230_v2.xlsx')

def read(name):
 with (B/name).open(encoding='utf-8-sig',newline='') as f:
  return list(csv.DictReader(f))

def addr(n):
 s=''
 while n:
  n,r=divmod(n-1,26);s=chr(65+r)+s
 return s

wb=SpreadsheetFile.import_xlsx(Blob.load(str(SRC)))
primary=read('LISAN_GOVERNANCE_MASTER_230.csv')
new=read('LISAN_NEW_40_CANDIDATES.csv')
ops=read('LISAN_RULE_EXECUTION_PROFILES_230.csv')
traces=read('LISAN_NEW_RULES_TRACEABILITY.csv')
metrics=read('LISAN_METRIC_CATALOG.csv')
imp=read('LISAN_RULE_IMPACT_EXPERIMENTS_230.csv')
sources=read('LISAN_SOURCE_MANIFEST.csv')
assert len(primary)==len(ops)==len(imp)==230 and len(new)==40

DARK='#173F3C';DEEP='#0C2C2A';GOLD='#D1B17A';IVORY='#FBF8F1';PALE='#EAF2EF';INK='#20322F';MUTED='#4F605C';ACCENT='#2F6E69'

def sheet_with_data(title,headers,rows,wide_cols=(),right_cols=(),row_h=27,table=True):
 sh=wb.worksheets.add(title)
 n=len(headers); endrow=len(rows)+1; endcol=addr(n)
 sh.get_range(f'A1:{endcol}{endrow}').values=[headers]+rows
 # Style all row heights and header, but do not make 230-row output excessively tall.
 sh.get_range(f'A1:{endcol}{endrow}').format.row_height=row_h
 sh.get_range(f'A1:{endcol}{endrow}').format.font.name='Arial'
 sh.get_range(f'A1:{endcol}{endrow}').format.font.size=10
 sh.get_range(f'A1:{endcol}{endrow}').format.font.color=INK
 sh.get_range(f'A1:{endcol}{endrow}').format.vertical_alignment='center'
 sh.get_range(f'A1:{endcol}1').format={'fill':DARK,'font':{'bold':True,'color':'#FFFFFF','size':10},'row_height':34,'vertical_alignment':'center'}
 try: sh.freeze_panes.freeze_rows(1);sh.freeze_panes.freeze_columns(1)
 except Exception: pass
 for j in range(1,n+1):
  col=addr(j)
  w=16
  if j==1:w=18
  if j in wide_cols:w=54
  elif j in right_cols:w=39
  elif j==n:w=26
  sh.get_range(f'{col}:{col}').format.column_width=w
  if j in wide_cols or j in right_cols:sh.get_range(f'{col}2:{col}{endrow}').format.wrap_text=True
 if table and len(rows)>0:
  try: sh.tables.add(f'A1:{endcol}{endrow}',True,f'Table_{re.sub("[^a-zA-Z0-9]","",title)}')
  except Exception as e:print('table skipped',title,str(e)[:100])
 return sh

heads=list(primary[0].keys())+['rule_status','authority_level','profile_origin','impact_metric_id','measurement_status']
opsd={p['id']:p for p in ops}
rows=[]
for r in primary:
 p=opsd[r['id']]
 rows.append([r[k] for k in primary[0].keys()]+['PROPOSED','PENDING_AUTHORITY_REVIEW',p['profile_origin'],p['impact_metric_id'],'NOT_MEASURED'])
s=sheet_with_data('V2 Rules',heads,rows,wide_cols=(2,3,10,12),right_cols=(7,8,9,11,13),row_h=39)
s.get_range('C2:C231').format.horizontal_alignment='right'
# Drop-downs represent future editable reviewed states, no row is auto-promoted.
try:
 s.get_range('N2:N231').data_validation={'rule':{'type':'list','values':['PROPOSED','UNDER_REVIEW','APPROVED_INACTIVE','ACTIVE','SUSPENDED','SUPERSEDED','REJECTED']}}
 s.get_range('R2:R231').data_validation={'rule':{'type':'list','values':['NOT_MEASURED','EXPERIMENT_PLANNED','EXECUTED_UNREVIEWED','REVIEWED','INCONCLUSIVE']}}
except Exception as e:print('validation warning',str(e)[:100])

nh=['id','text_en','text_ar','kind','force','category','source_reference','closest_existing','novelty_rationale','risk_tier','phase','trigger_event','source_status','admission_status']
newrows=[[r.get(k,'') for k in nh] for r in new]
sn=sheet_with_data('V2 New 40',nh,newrows,wide_cols=(2,3,7,9),right_cols=(6,8),row_h=48)
sn.get_range('C2:C41').format.horizontal_alignment='right'

opheads=['id','rule_kind','force','category','phase','applies_to','trigger_event','trigger_predicate','expected_behavior','enforcement_target','verification_mode','failure_action','gate_reference','required_evidence','proposed_test','impact_metric_id','risk_tier','applicability_status','enforcement_status','profile_origin','review_status']
sops=sheet_with_data('V2 Rule Operations',opheads,[[r[k] for k in opheads] for r in ops],wide_cols=(8,9,14,15),right_cols=(4,18,20),row_h=40)

mheads=['metric_id','name_en','name_ar','formula_text','direction','evidence_source','dimension','qualification_note','measured_value','measurement_status','benchmark_revision','owner_approved_threshold']
sm=sheet_with_data('V2 Metrics',mheads,[[r[k] for k in mheads] for r in metrics],wide_cols=(4,8),right_cols=(2,3,6),row_h=42)
sm.get_range('C2:C14').format.horizontal_alignment='right'

# Impact run sheet has explicit blank observed values and formulas that remain blank until evidence is supplied.
metrics_map={r['metric_id']:r for r in metrics}
impact_headers=['rule_id','metric_id','risk_tier','baseline_events','baseline_total','baseline_rate','treatment_events','treatment_total','treatment_rate','desired_direction','improvement_delta','evaluation_status','evidence_receipt','independent_reviewer','uncertainty_note','experiment_design','audit_note']
impact_rows=[]
for r in imp:
 mt=metrics_map[r['metric_id']]
 impact_rows.append([r['rule_id'],r['metric_id'],r['risk_tier'],'','','','','','',mt['direction'],'',r['evaluation_status'],'','','',r['experiment_design'],r['notes']])
si=sheet_with_data('V2 Rule Impact',impact_headers,impact_rows,wide_cols=(16,17),right_cols=(15,),row_h=26)
# Body formulas refer only to user-entered observed rates, and show blank if no evidence.
si.get_range('F2').formulas=[['=IF(OR(D2="",E2="",E2=0),"",D2/E2)']]
si.get_range('F2:F231').fill_down()
si.get_range('I2').formulas=[['=IF(OR(G2="",H2="",H2=0),"",G2/H2)']]
si.get_range('I2:I231').fill_down()
si.get_range('K2').formulas=[['=IF(OR(F2="",I2=""),"",IF(J2="MAX",I2-F2,F2-I2))']]
si.get_range('K2:K231').fill_down()
for col in ('F','I','K'):
 si.get_range(f'{col}2:{col}231').set_number_format('0.0%')
try:
 si.get_range('L2:L231').data_validation={'rule':{'type':'list','values':['NOT_RUN','BLOCKED','FAIL','PASS_IN_SCOPE','INCONCLUSIVE']}}
except Exception:pass

trh=list(traces[0].keys())
st=sheet_with_data('V2 Source Crosswalk',trh,[[r[k] for k in trh] for r in traces],wide_cols=(2,5,6),right_cols=(3,4),row_h=47)
sourceheads=list(sources[0].keys())
ss=sheet_with_data('V2 Source Manifest',sourceheads,[[r[k] for k in sourceheads] for r in sources],wide_cols=(2,3),right_cols=(4,5),row_h=38)

steps=[
 ('AD-01','صياغة محددة','Plain English/Arabic rule','Rule text + owner','RETURN_FOR_REWRITE'),
 ('AD-02','صلة بالمشروع','Exact LISAN task, phase, scope','Scope and applicability','REJECT_OUT_OF_SCOPE'),
 ('AD-03','إثبات المصدر','Source section, state and authority','Quote/digest/decision','QUARANTINE_SOURCE'),
 ('AD-04','عدم التكرار الدلالي','IDENTICAL/REFINE/CONFLICT/SUPERSEDE/NEW','Closest-existing and rationale','MERGE_OR_REFINE'),
 ('AD-05','حسم التعارض','Approved precedence and scoped overrides','Authority conflict disposition','OWNER_DECISION_REQUIRED'),
 ('AD-06','ضبط KIND/FORCE','Type and deontic force match actual language','Classification review','RETURN_FOR_CLASSIFICATION'),
 ('AD-07','شرط الانطباق','Typed event and predicate','Machine-checkable route + context','HOLD_APPLICABILITY'),
 ('AD-08','تحديد جهة التطبيق','Actor/role/effective tool grants','Host authorization evidence','HOLD_AUTHORIZATION'),
 ('AD-09','إنفاذ صحيح','Explicit target and no prompt-only enforcement claim','Code/config plus trace','NO_ENFORCED_CLAIM'),
 ('AD-10','تصرف الفشل','Deny/downgrade/flag/defer/log','Failure-action binding','HOLD_IMPLEMENTATION'),
 ('AD-11','اختبار إيجابي','Compliant case within scoped run','Actual trace and verdict','NOT_RUN'),
 ('AD-12','اختبار سلبي','Violation or adversarial prompt','Actual denial/limited outcome','NOT_RUN'),
 ('AD-13','خطة قياس أثر','Baseline, metric, direction and harms','Experiment manifest','IMPACT_NOT_MEASURED'),
 ('AD-14','تكافؤ عربي/إنجليزي','Same actor/force/scope/negation/exceptions','Bilingual independent review','RETURN_FOR_TRANSLATION'),
 ('AD-15','اعتماد مخوّل','Approval actor, timestamp, exact version','Signed review/decision event','PROPOSED_ONLY'),
 ('AD-16','توافق النسخة','Actual host/Plugin/Site contracts and permissions','Tested version and digest','DO_NOT_ACTIVATE'),
]
ad=sheet_with_data('V2 Admission Gates',['gate_id','المرحلة','Acceptance question','Required evidence','If missing'],[[*x] for x in steps],wide_cols=(3,4),right_cols=(2,5),row_h=34)
ad.get_range('B2:B17').format.horizontal_alignment='right'

review=[]
for r in primary[:190]:
 t=r['text_en'].lower()
 if r['force'] in ('SHOULD','MAY') and re.search(r'\b(must|never|may not|do not|require)\b',t):
  review.append([r['id'],r['force'],'STRONG_MODAL_IN_TEXT','Review whether MUST/MUST_NOT is needed; do not edit the original without authority.',r['text_en'],'PENDING_OWNER_REVIEW'])
assert len(review)==8
sr=sheet_with_data('V2 Classification QA',['id','current_force','flag','recommendation','text_en','review_status'],review,wide_cols=(4,5),row_h=45)

fdef=[
 ('kind','Category of normative form','PRINCIPLE/POLICY/CONSTRAINT/CONTROL/REQUIREMENT/INSTRUCTION/GUIDELINE','NOT priority or authority'),
 ('force','Deontic requirement','MUST/MUST_NOT/SHOULD/MAY','Within applicable scope, not rule precedence'),
 ('authority_level','Where the rule obtains authority','FOUNDATIONAL_METHOD/.../PENDING_AUTHORITY_REVIEW','Explicitly reviewed, never inferred from wording'),
 ('rule_status','Whether a rule can run','PROPOSED/UNDER_REVIEW/APPROVED_INACTIVE/ACTIVE/SUSPENDED/SUPERSEDED/REJECTED','Draft records must not activate'),
 ('phase','Proposed applicable stage','EVIDENCE_COLLECTION/OUTPUT/RULE_GOVERNANCE...','Category-derived mappings require review'),
 ('trigger_event','Typed candidate event','CORPUS_QUERY/RUN_RESUME/PROTECTED_TRANSITION...','Not a full executable predicate'),
 ('trigger_predicate','Precise condition for applicability','Structured boolean rule after authorization','Current placeholder is NOT executable'),
 ('enforcement_target','Where policy should be enforced','SERVER_POLICY/OUTPUT_GUARD/HOST_CONTEXT/HUMAN_REVIEW','Target is not implementation evidence'),
 ('enforcement_status','Verified operational maturity','NOT_VERIFIED/PRESENT_UNTESTED/VERIFIED_IN_SCOPE','All profiles initially NOT_VERIFIED'),
 ('failure_action','What happens when a rule fails','DENY_PROTECTED_ACTION/HOLD_TRANSITION/RESTRICT_TO_DRAFT/FLAG_FOR_REVIEW/LOG_ONLY','Must fit severity and scope'),
 ('impact_metric_id','Relevant planned measurement','M01..M13','Not a measured result'),
 ('risk_tier','Pre-test priority assessment','CRITICAL/HIGH/MEDIUM/LOW','Not a probability or impact measurement'),
 ('measurement_status','Evidence of effect','NOT_MEASURED/.../REVIEWED','NOT_MEASURED until actual evaluation'),
 ('source_status','Provenance state of normative text','Existing draft/source-derived candidate/design proposal','Separate from authority'),
 ('profile_origin','How operational fields were populated','CATEGORY_BASED_INFERENCE/EXPLICIT_NEW_RULE_PROPOSAL','All require review before machine enforcement'),
 ('admission_status','Independent review and adoption workflow','PENDING/REJECTED/APPROVED...','Owner decision distinct from rule text'),
]
sd=sheet_with_data('V2 Field Dictionary',['field','purpose','values/examples','warning'],[[*x] for x in fdef],wide_cols=(2,3,4),row_h=39)

assets=[
 ('Rule Registry','RULE_ID','Policy Steward','Source/auth/status/English Arabic','Not identical to Study Registry'),
 ('Applicability Engine','RULE_ID + revision','Trusted Host','Run, phase, role, evidence scope, event predicate','No prompt-only rule selection'),
 ('Capability Grants','run_id','Trusted Host','Use/integrate/publish rights','No model-generated identity'),
 ('Rule and Gate Receipts','rule_id + execution','Validator/Gateway','Digest, observed outcome, rule revision','Model claim is not receipt'),
 ('Rule Evaluation','test_id','QA/Independent Reviewer','Positive/negative tests, trace, verdict','NOT_RUN stays NOT_RUN'),
 ('Impact Registry','experiment_id','QA/Owner','Baseline/intervention/false denial/cost','No causal claim before matched experiment'),
 ('Approval Ledger','decision_id','Owner/Authority','Authorized effective rule revision','No approval self-granted by AI'),
 ('Site Rule Studio','view_id','Frontend under AuthZ','Reviewable bilingual policy and effects','UI does not own policy authority'),
]
sa=sheet_with_data('V2 Architecture',['logical_component','primary_key','authority_owner','required_content','critical_boundary'],[[*x] for x in assets],wide_cols=(4,5),right_cols=(1,3),row_h=39)


# Proposed positive/negative tests for each rule. These are test DESIGN rows, not executed QA.
tcases=read('LISAN_RULE_TEST_CASES_460_PROPOSED.csv')
tcols=['test_id','rule_id','polarity','phase','trigger_event','expected_actor','fixture_design','expected_observation','gate','oracle_class','verdict','test_quality_status']
ste=sheet_with_data('V2 Proposed Tests',tcols,[[r[c] for c in tcols] for r in tcases],wide_cols=(7,8),right_cols=(6,),row_h=42)
# Similarity hints only; the rationale and semantic duplicate decision require a human.
dups=read('LISAN_SEMANTIC_DUPLICATE_SCREENING_40.csv')
dcols=list(dups[0].keys())
sdup=sheet_with_data('V2 Duplicate QA',dcols,[[r[c] for c in dcols] for r in dups],wide_cols=(9,11),right_cols=(8,10),row_h=42)

# Working dashboard with formulas, with no observed-effect values invented.
dash=wb.worksheets.add('V2 Summary')
dash.get_range('A1:F2').merge_cells if False else None
# no merge needed; avoid obscure appearance bugs
dash.get_range('A1').values=[['لسان القرآن | سجل البنود الحاكمة التشغيلي — مسودة V2']]
dash.get_range('A1:F1').format={'fill':DARK,'font':{'color':'#FFFFFF','bold':True,'size':15},'row_height':38}
dash.get_range('A3:B10').values=[
 ['المؤشر','القيمة'],['البنود السابقة',190],['الإضافات المرشحة',40],['الإجمالي',230],
 ['اختبارات أثر اجتازت ضمن نطاقها',None],['إصداراتها مثبتة بمراجعة مستقلة',None],['بقيت دون تعديل',190],['وضع النشر','DRAFT / NO ACTIVATION']
]
dash.get_range('B7').formulas=[['=COUNTIF(\'V2 Rule Impact\'!$L$2:$L$231,"PASS_IN_SCOPE")']]
dash.get_range('B8').values=[['لم يُتحقق من اعتماد أي بند جديد']]
dash.get_range('A3:B3').format={'fill':GOLD,'font':{'bold':True,'color':DEEP},'row_height':29}
dash.get_range('A4:B10').format.row_height=29
cats=collections.Counter(r['category'] for r in primary)
dash.get_range('A13:B13').values=[['المجال','عدد البنود']]
dash.get_range('A13:B13').format={'fill':DARK,'font':{'bold':True,'color':'#FFFFFF'},'row_height':29}
for i,cat in enumerate(sorted(cats),14):
 dash.get_range(f'A{i}').values=[[cat]]
 dash.get_range(f'B{i}').formulas=[[f'=COUNTIF(\'V2 Rules\'!$G$2:$G$231,A{i})']]
dash.get_range('A:A').format.column_width=44;dash.get_range('B:B').format.column_width=26
try:
 ch=dash.charts.add('bar',dash.get_range(f'A13:B{13+len(cats)}'))
 ch.title_text='Distribution of rule categories (proposed register)'
 ch.set_position('D4','N21')
except Exception as e:print('chart skip',str(e)[:170])
dash.get_range('A26').values=[['ملاحظة صلاحية: 190 بندًا أُبقيت، و40 إضافة جديدة مقترحة. جميع قيم الأثر الحقيقي فارغة، ولا توجد قاعدة جديدة مُفعّلة.']]
dash.get_range('A26').format.column_width=44

# Export final.
print('Workbook sheets after addition:',wb.inspect({'kind':'sheet','include':'id,name'}).ndjson[-2500:])
SpreadsheetFile.export_xlsx(wb).save(str(DEST))
print('EXPORTED',str(DEST),DEST.stat().st_size)
