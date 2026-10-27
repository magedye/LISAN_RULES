#!/usr/bin/env python3
"""Offline verification of the *draft* LISAN rule register; makes no authority claims."""
import csv, json, pathlib, collections, hashlib, re, sys
BASE=pathlib.Path(__file__).resolve().parent.parent
PREV=pathlib.Path('/mnt/data/LISAN_Governance_Register_Expanded_20261027/LISAN_GOVERNING_RULES_190_BILINGUAL.csv')
def read(p):
 with p.open(encoding='utf-8-sig',newline='') as fh:return list(csv.DictReader(fh))
def check(cond,msg):
 if not cond:raise AssertionError(msg)
old=read(PREV);new=read(BASE/'LISAN_GOVERNANCE_MASTER_230.csv')
candidates=read(BASE/'LISAN_NEW_40_CANDIDATES.csv');profiles=read(BASE/'LISAN_RULE_EXECUTION_PROFILES_230.csv')
impact=read(BASE/'LISAN_RULE_IMPACT_EXPERIMENTS_230.csv'); metrics=read(BASE/'LISAN_METRIC_CATALOG.csv')
check((len(old),len(new),len(candidates),len(profiles),len(impact))==(190,230,40,230,230),'Counts incorrect')
keys=list(old[0]);check(all(all(old[i][k]==new[i][k] for k in keys) for i in range(190)),'Baseline changed')
check(all(new[i]['id']==f'LISAN-GOV-{i+1:03}' for i in range(230)),'IDs not sequential')
check(len({r['text_en'].casefold().strip() for r in new})==230,'Exact English duplicate')
check(all(r['text_en'].strip() and r['text_ar'].strip() for r in new),'Empty bilingual rule')
check(all(m['measurement_status']=='NOT_MEASURED' and m['measured_value']=='' for m in metrics),'bad measurement status')
check(all(r['evaluation_status']=='NOT_RUN' and r['baseline_metric']=='' and r['treatment_metric']=='' for r in impact),'Impact values invented')
check(all(p['enforcement_status']=='NOT_VERIFIED' for p in profiles),'Unproven enforcement reported')
check(all(p['review_status']=='PENDING_INDEPENDENT_REVIEW' for p in profiles),'Unreviewed profiles reported reviewed')
check(set(r['impact_metric_id'] for r in profiles).issubset(set(m['metric_id'] for m in metrics)),'Unknown metric')
check(collections.Counter(r['source_status'] for r in candidates)=={'SOURCE_DERIVED_PROPOSAL':26,'DESIGN_PROPOSAL_NOT_SOURCE_REQUIREMENT':14},'Wrong candidate origin counts')
# Schema in exported text is a design aid, not registered host schema.
check(json.loads((BASE/'schemas/lisan_rule_record_v2_PROPOSED.schema.json').read_text(encoding='utf8'))['additionalProperties'] is False,'Expected closed schema')
print(json.dumps({'status':'LOCAL_ARTIFACT_VALIDATION_PASSED','baseline':190,'candidate_additions':40,'total':230,'metrics':len(metrics),'impact_tests_executed':0,'source_derived_candidates':26,'design_proposals':14,'key_limit':'No human semantic dedup/authority approval or live Site/Plugin compliance test conducted'},ensure_ascii=False,indent=2))
