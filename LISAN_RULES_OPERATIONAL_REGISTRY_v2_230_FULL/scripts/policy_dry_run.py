#!/usr/bin/env python3
"""Safe, NON-AUTHORITATIVE demonstration: proposed rules are never selected as active."""
import csv, json, pathlib, sys
BASE=pathlib.Path(__file__).resolve().parent.parent
with (BASE/'LISAN_GOVERNANCE_MASTER_230.csv').open(encoding='utf-8-sig',newline='') as f:
 rules=list(csv.DictReader(f))
# The master CSV contains only proposals and does not include an owner-issued active version.
# This mock policy resolver defaults to DENY; never use it as a production authorization service.
active=[x for x in rules if x.get('admission_status')=='ACTIVE' and x.get('approved_by') and x.get('verified_predicate')]
print(json.dumps({'mode':'DRY_RUN_ONLY','candidate_count':len(rules),'selected_active_rules':len(active),'can_authorize_protected_action':False,'message':'No owner-authorized active rules are represented in this draft; trusted policy service is required.'},ensure_ascii=False,indent=2))
