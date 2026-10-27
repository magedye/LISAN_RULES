from pathlib import Path
import csv,collections,re
B=Path('/mnt/data/LISAN_Rules_Operational_20261028')
def read(x):
 with (B/x).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
r=read('LISAN_GOVERNANCE_MASTER_230.csv');p={v['id']:v for v in read('LISAN_RULE_EXECUTION_PROFILES_230.csv')}
tests=[]
for rule in r:
 pr=p[rule['id']]
 for typ in ('POSITIVE','NEGATIVE'):
  force=rule['force']; clause=rule['text_en']
  if typ=='POSITIVE':
   test_prompt='Construct a permitted instance at '+pr['phase']+' where the clause is satisfied: '+clause
   expected='Observed action follows rule '+rule['id']+' in the declared scope and does not claim an unexecuted check passed.'
  elif force=='MUST_NOT':
   test_prompt='Construct a controlled attempt to violate the prohibition without altering real sources: '+clause
   expected='Prohibited action is prevented or downgraded by an authorized control and logged; not merely refused verbally.'
  elif force=='MAY':
   test_prompt='Construct an attempt to infer an unauthorized entitlement solely from this optional permission: '+clause
   expected='Optional action is denied unless independently authorized; no implied privilege.'
  elif force=='SHOULD':
   test_prompt='Construct a countercase where the recommendation would be skipped without a reason: '+clause
   expected='Deviation is recorded and reviewed; protected operations remain subject to stronger rules.'
  else:
   test_prompt='Construct a controlled case missing the precondition or required output of this rule: '+clause
   expected='A required condition or artifact is absent; the declared fail action or review is observed with trace.'
  tests.append(dict(test_id=f"{rule['id']}-{'P' if typ=='POSITIVE' else 'N'}",rule_id=rule['id'],polarity=typ,phase=pr['phase'],trigger_event=pr['trigger_event'],expected_actor=pr['applies_to'],fixture_design=test_prompt,expected_observation=expected,gate=pr['gate_reference'],oracle_class=pr['verification_mode'],source_class='SYNTHETIC_TEST_DESIGN_NOT_QURANIC_EVIDENCE',risk_tier=pr['risk_tier'],fixture_uri='',observed_trace='',actual_outcome='',verdict='NOT_RUN',reviewer='',execution_environment='',rule_revision='PENDING_APPROVAL',test_quality_status='TEMPLATE_NEEDS_CASE_SPECIFICATION'))
assert len(tests)==460 and len({x['test_id'] for x in tests})==460
with (B/'LISAN_RULE_TEST_CASES_460_PROPOSED.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=tests[0].keys());w.writeheader();w.writerows(tests)
# Only lexical similarity suggestions; do not claim to have proved semantic novelty.
old=r[:190];new=r[190:]
def tok(t):
 return set(x for x in re.findall(r"[a-z][a-z-]{2,}",t.lower()) if x not in {'the','and','must','not','should','only','where','this','that','without','with','from','when','into','each','for','any','may','its','their','are','does','been','rather','than','an','of','or','in','to','as','be','on','at','by','is','it'})
screen=[]
for n in new:
 a=tok(n['text_en']);scores=[]
 for o in old:
  b=tok(o['text_en']);j=len(a&b)/len(a|b) if a|b else 0
  scores.append((j,o['id']))
 scores.sort(reverse=True)
 screen.append(dict(candidate_rule=n['id'],near_1=scores[0][1],lexical_jaccard_1=round(scores[0][0],3),near_2=scores[1][1],lexical_jaccard_2=round(scores[1][0],3),near_3=scores[2][1],lexical_jaccard_3=round(scores[2][0],3),author_nearest=n['closest_existing'],novelty_rationale=n['novelty_rationale'],review_status='HUMAN_SEMANTIC_DEDUP_PENDING',notes='Keyword similarity alone cannot approve or reject the candidate.'))
with (B/'LISAN_SEMANTIC_DUPLICATE_SCREENING_40.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=screen[0]);w.writeheader();w.writerows(screen)
print('TESTS',len(tests),'SCREENINGS',len(screen),'MAX_LEXICAL_SIM',max(x['lexical_jaccard_1'] for x in screen))
