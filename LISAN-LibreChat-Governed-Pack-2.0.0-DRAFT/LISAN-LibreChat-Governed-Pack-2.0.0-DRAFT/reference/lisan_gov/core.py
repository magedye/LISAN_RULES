"""LISAN governance reference: strict mechanical gates, not a semantic oracle.

Standard library only. Critical operations are invoked by a trusted host/operator,
NOT exposed as tools to a language model. Test fixtures are synthetic, not Quran.
"""
from __future__ import annotations
import hashlib, json, sqlite3, time
from dataclasses import dataclass
from contextlib import contextmanager
from typing import Protocol
from pathlib import Path

MODES = frozenset({'NEW_CORPUS_STUDY', 'CUMULATIVE_EXTENSION', 'INDEPENDENT_DIAGNOSTIC'})
EXTERNAL_MODE = 'POST_LOCK_EXTERNAL_COMPARISON'
COUNTER_OUTCOMES = frozenset({'COUNTERS','SUPPORTS','UNRESOLVED','NOT_FOUND_IN_EXAMINED_SCOPE','LIMITS'})

class GateFailure(Exception):
    def __init__(self, code):
        super().__init__(code)
        self.code = code


def canon(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))

def digest(value):
    return hashlib.sha256(canon(value).encode('utf-8')).hexdigest()

@dataclass(frozen=True)
class Principal:
    # IMPORTANT: created from trusted host authentication / operator session only.
    subject: str
    roles: frozenset[str]

    def require(self, role):
        if not self.subject or role not in self.roles:
            raise GateFailure('ROLE_OR_AUTH_REQUIRED')

class Corpus(Protocol):
    def scope(self, selector: dict) -> dict: ...
    def verify_quote(self, ref: str, text: str, kind: str) -> bool: ...

class SyntheticCorpus:
    """For test/demo only. Text is intentionally non-Quranic."""
    def __init__(self, verses: dict[str,str]):
        self.verses = dict(verses)
        self.corpus_sha256 = digest(self.verses)
        self.corpus_id = 'SYNTHETIC_NON_QURANIC_TEST'
    def scope(self, selector):
        if set(selector) != {'kind','refs'} or selector['kind']!='EXPLICIT_REFS':
            raise GateFailure('SELECTOR_UNSUPPORTED_IN_FIXTURE')
        refs=selector['refs']
        if not refs or len(refs)!=len(set(refs)) or not set(refs).issubset(self.verses):
            raise GateFailure('SCOPE_INVALID')
        # scope is explicit refs only. This never represents a whole root/lemma census.
        return {'refs':sorted(refs),'corpus_id':self.corpus_id,'corpus_sha256':self.corpus_sha256,
                'selector_digest':digest(selector),'exhaustive_for_selector':True,
                'semantic_exhaustive':False,'source_authenticity':'SYNTHETIC_TEST_ONLY'}
    def verify_quote(self,ref,text,kind):
        if kind not in {'FULL','EXCERPT'} or not isinstance(text,str) or not text:
            return False
        v=self.verses.get(ref)
        return v is not None and (v==text if kind=='FULL' else text in v)

class Policy:
    # Enforcement must take caller role/mode from server state, never model arguments.
    @staticmethod
    def tool_allowed(mode: str, tool: str) -> bool:
        read={'lisan_status','lisan_search','lisan_get_verses','lisan_verify_quote',
              'lisan_validate_analysis','lisan_prepare_research','lisan_check_study'}
        external={'external_compare'}
        if mode in MODES: return tool in read
        if mode==EXTERNAL_MODE: return tool in read|external
        return False
    @staticmethod
    def choose_route(*, explicit_independence=False, explicit_external=False,
                     locked_internal=False, finding_accepted=False,
                     active_compatible=False, covers_question=False):
        if explicit_independence: return 'INDEPENDENT_DIAGNOSTIC'
        if explicit_external:
            if not locked_internal: raise GateFailure('POST_LOCK_ONLY')
            return EXTERNAL_MODE
        if finding_accepted and active_compatible and covers_question:
            return 'REUSE_QUALIFIED'
        if finding_accepted and active_compatible:
            return 'CUMULATIVE_EXTENSION'
        return 'NEW_CORPUS_STUDY'

class Registry:
    """Durable SQLite reference. Not a production identity/tenant boundary."""
    def __init__(self, dbpath, corpus: Corpus, policy_version='LISAN-POLICY-2.0.0',
                 allow_fixture_release=False, source_qualification=False,
                 method_version='LISAN-METHOD-1.0'):
        self.dbpath=str(dbpath)
        self.corpus=corpus
        self.policy_version=policy_version
        self.method_version=method_version
        self.allow_fixture_release=allow_fixture_release
        self.source_qualification=source_qualification
        Path(self.dbpath).parent.mkdir(parents=True, exist_ok=True)
        self.conn=sqlite3.connect(self.dbpath, isolation_level=None, timeout=10)
        self.conn.row_factory=sqlite3.Row
        self.conn.execute('PRAGMA foreign_keys=ON')
        self.conn.execute('PRAGMA journal_mode=WAL')
        self.conn.executescript('''
        CREATE TABLE IF NOT EXISTS studies(
            id TEXT PRIMARY KEY, active_rev INTEGER NOT NULL,
            created_by TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS revisions(
            id TEXT NOT NULL, rev INTEGER NOT NULL,
            phase TEXT NOT NULL, data TEXT NOT NULL, sealed_digest TEXT,
            PRIMARY KEY(id,rev), FOREIGN KEY(id) REFERENCES studies(id));
        CREATE TABLE IF NOT EXISTS decisions(
            id TEXT NOT NULL, rev INTEGER NOT NULL,
            kind TEXT NOT NULL, actor TEXT NOT NULL, decision TEXT NOT NULL,
            reason TEXT NOT NULL, snapshot_digest TEXT NOT NULL,
            PRIMARY KEY(id,rev,kind));
        CREATE TABLE IF NOT EXISTS dependencies(
            child TEXT NOT NULL, parent TEXT NOT NULL, parent_rev INTEGER NOT NULL,
            PRIMARY KEY(child,parent), FOREIGN KEY(child) REFERENCES studies(id));
        CREATE TABLE IF NOT EXISTS invalidations(
            id TEXT PRIMARY KEY, reason TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS events(
            n INTEGER PRIMARY KEY AUTOINCREMENT, id TEXT NOT NULL, rev INTEGER NOT NULL,
            event TEXT NOT NULL, actor TEXT NOT NULL, payload_digest TEXT NOT NULL,
            previous_hash TEXT NOT NULL, event_hash TEXT NOT NULL);
        ''')

    def close(self): self.conn.close()
    @contextmanager
    def transaction(self):
        self.conn.execute('BEGIN IMMEDIATE')
        try:
            yield
            self.conn.execute('COMMIT')
        except BaseException:
            self.conn.execute('ROLLBACK')
            raise

    def _event(self, sid, rev, event, subject, payload):
        row=self.conn.execute('SELECT event_hash FROM events ORDER BY n DESC LIMIT 1').fetchone()
        prev=row['event_hash'] if row else '0'*64
        pay=digest(payload)
        record={'id':sid,'rev':rev,'event':event,'actor':subject,
                'payload_digest':pay,'previous_hash':prev}
        eh=digest(record)
        self.conn.execute('INSERT INTO events(id,rev,event,actor,payload_digest,previous_hash,event_hash) VALUES(?,?,?,?,?,?,?)',
                          (sid,rev,event,subject,pay,prev,eh))

    def verify_audit_chain(self):
        prev='0'*64
        for row in self.conn.execute('SELECT * FROM events ORDER BY n'):
            record={k:row[k] for k in ('id','rev','event','actor','payload_digest','previous_hash')}
            if row['previous_hash']!=prev or digest(record)!=row['event_hash']: return False
            prev=row['event_hash']
        return True

    def _load(self,sid,rev):
        st=self.conn.execute('SELECT active_rev FROM studies WHERE id=?',(sid,)).fetchone()
        if not st: raise GateFailure('STUDY_NOT_FOUND')
        if rev!=st['active_rev']: raise GateFailure('REVISION_CONFLICT')
        r=self.conn.execute('SELECT * FROM revisions WHERE id=? AND rev=?',(sid,rev)).fetchone()
        if not r: raise GateFailure('REVISION_NOT_FOUND')
        return dict(r),json.loads(r['data'])

    def _persist(self,sid,rev,phase,data):
        x=self.conn.execute('UPDATE revisions SET phase=?, data=? WHERE id=? AND rev=? AND sealed_digest IS NULL',
                            (phase,canon(data),sid,rev))
        if x.rowcount!=1: raise GateFailure('SEALED_IMMUTABLE')

    def create(self,sid:str,actor:Principal,selector:dict,mode='NEW_CORPUS_STUDY',
               exposure=None,method_version=None):
        actor.require('researcher')
        if mode not in MODES: raise GateFailure('INVALID_MODE')
        if not sid or len(sid)>128 or not sid.replace('-','').replace('_','').replace('.','').isalnum():
            raise GateFailure('INVALID_STUDY_ID')
        if mode=='INDEPENDENT_DIAGNOSTIC' and exposure:
            raise GateFailure('BLIND_EXPOSURE_FORBIDDEN')
        scope=self.corpus.scope(selector)
        if not scope.get('refs') or not scope.get('exhaustive_for_selector'):
            raise GateFailure('SCOPE_NOT_ATTESTED')
        obj={'id':sid,'revision':1,'mode':mode,'author':actor.subject,
             'scope':scope,'selector':selector,'policy_version':self.policy_version,
             'method_version':method_version or self.method_version,'exposure':exposure or [],'observations':[],
             'hypothesis':None,'countersearch':None,'limitations':[],
             'epistemic_status':'HYPOTHESIS','semantic_review':'NOT_REVIEWED',
             'approval_status':'NOT_GRANTED','release_status':'NOT_RELEASED'}
        with self.transaction():
            if self.conn.execute('SELECT 1 FROM studies WHERE id=?',(sid,)).fetchone():
                raise GateFailure('STUDY_EXISTS')
            self.conn.execute('INSERT INTO studies VALUES (?,?,?)',(sid,1,actor.subject))
            self.conn.execute('INSERT INTO revisions(id,rev,phase,data) VALUES(?,?,?,?)',
                              (sid,1,'SCOPED',canon(obj)))
            self._event(sid,1,'G0_SCOPE_CREATED',actor.subject,{'selector':scope['selector_digest']})
        return obj

    def observe(self,sid,rev,actor:Principal,ref,text,kind='EXCERPT',
                annotation='',annotation_type='TEXT_EXCERPT',source_label='QURAN'):
        actor.require('researcher')
        with self.transaction():
            row,d=self._load(sid,rev)
            if d['author']!=actor.subject: raise GateFailure('AUTHOR_REQUIRED')
            if row['phase'] not in {'SCOPED','OBSERVING'}: raise GateFailure('STAGE_DENIED')
            if ref not in d['scope']['refs']: raise GateFailure('OUT_OF_SCOPE')
            if source_label!='QURAN': raise GateFailure('NON_QURAN_AS_PRIMARY')
            if annotation_type not in {'TEXT_EXCERPT','STRUCTURAL_CANDIDATE'}:
                raise GateFailure('INVALID_ANNOTATION_TYPE')
            if not self.corpus.verify_quote(ref,text,kind): raise GateFailure('QUOTE_NOT_VERIFIED')
            if any(o['ref']==ref for o in d['observations']): raise GateFailure('DUPLICATE_OBSERVATION')
            d['observations'].append({'ref':ref,'text':text,'kind':kind,'annotation':annotation,
                                      'annotation_type':annotation_type,'source_label':source_label})
            self._persist(sid,rev,'OBSERVING',d)
            self._event(sid,rev,'G3_OBSERVED',actor.subject,{'ref':ref,'kind':kind})
            return d

    def hypothesize(self,sid,rev,actor:Principal,statement:str,falsification_condition:str,
                    rival:str,reasoning:str):
        actor.require('researcher')
        with self.transaction():
            row,d=self._load(sid,rev)
            if d['author']!=actor.subject: raise GateFailure('AUTHOR_REQUIRED')
            if row['phase']!='OBSERVING' or not d['observations']:
                raise GateFailure('OBSERVATIONS_REQUIRED')
            if any(not isinstance(v,str) or len(v.strip())<8 for v in
                   (statement,falsification_condition,rival,reasoning)):
                raise GateFailure('HYPOTHESIS_INCOMPLETE')
            d['hypothesis']={'statement':statement,'falsification_condition':falsification_condition,
                             'rival':rival,'warrant':reasoning}
            self._persist(sid,rev,'HYPOTHESIZED',d)
            self._event(sid,rev,'G4_HYPOTHESIZED',actor.subject,{'hypothesis':d['hypothesis']})
            return d

    def countersearch(self,sid,rev,actor:Principal,refs:list[str],outcome:str,method:str,reason:str):
        actor.require('researcher')
        with self.transaction():
            row,d=self._load(sid,rev)
            if d['author']!=actor.subject: raise GateFailure('AUTHOR_REQUIRED')
            if row['phase']!='HYPOTHESIZED': raise GateFailure('STAGE_DENIED')
            if outcome not in COUNTER_OUTCOMES or not refs or not set(refs).issubset(d['scope']['refs']):
                raise GateFailure('COUNTERSEARCH_INVALID')
            if not method.strip() or not reason.strip(): raise GateFailure('COUNTERSEARCH_NOT_EXPLAINED')
            d['countersearch']={'inspected_refs':sorted(set(refs)),'outcome':outcome,
                                'method':method,'reason':reason,
                                'evidence_level':'RESEARCHER_DECLARATION_NEEDS_REVIEW'}
            self._persist(sid,rev,'COUNTERCHECKED',d)
            self._event(sid,rev,'G5_COUNTERSEARCH_RECORDED',actor.subject,{'refs':sorted(set(refs)),'outcome':outcome})
            return d

    def seal(self,sid,rev,actor:Principal,claim_full=False):
        actor.require('researcher')
        with self.transaction():
            row,d=self._load(sid,rev)
            if d['author']!=actor.subject: raise GateFailure('AUTHOR_REQUIRED')
            if row['phase']!='COUNTERCHECKED': raise GateFailure('STAGE_DENIED')
            observed={o['ref'] for o in d['observations']}
            expected=set(d['scope']['refs'])
            countered=set(d['countersearch']['inspected_refs'])
            # This only proves enumerated coverage of DECLARED selector; not semantic validity.
            full=expected==observed and expected==countered
            if claim_full and not full: raise GateFailure('FULL_COVERAGE_NOT_PROVEN')
            d['coverage']={'expected':len(expected),'observed':len(observed),
                           'counter_inspected':len(countered),
                           'scope':'DECLARED_SELECTOR_ONLY','status':'FULL_DECLARED' if full else 'PARTIAL'}
            if not full: d['limitations'].append('PARTIAL_DECLARED_SCOPE')
            lock=digest(d)
            x=self.conn.execute('UPDATE revisions SET phase=?,data=?,sealed_digest=? '
                                'WHERE id=? AND rev=? AND sealed_digest IS NULL',
                                ('SEALED',canon(d),lock,sid,rev))
            if x.rowcount!=1: raise GateFailure('LOCK_CONFLICT')
            self._event(sid,rev,'G7_SEALED',actor.subject,{'digest':lock})
            return {'study_id':sid,'revision':rev,'sealed_digest':lock,'coverage':d['coverage'],
                    'epistemic_status':'HYPOTHESIS','semantic_review':'NOT_REVIEWED',
                    'approval_status':'NOT_GRANTED'}

    def review(self,sid,rev,actor:Principal,verdict:str,reason:str):
        actor.require('reviewer')
        if verdict not in {'SUPPORTED','UNRESOLVED','REJECTED'} or not reason.strip():
            raise GateFailure('REVIEW_INVALID')
        with self.transaction():
            row,d=self._load(sid,rev)
            if row['phase']!='SEALED': raise GateFailure('LOCK_REQUIRED')
            if actor.subject==d['author']: raise GateFailure('INDEPENDENCE_REQUIRED')
            if self._decision(sid,rev,'review'): raise GateFailure('REVIEW_ALREADY_EXISTS')
            self._save_decision(sid,rev,'review',actor.subject,verdict,reason,row['sealed_digest'])
            self._event(sid,rev,'G8_REVIEWED',actor.subject,{'verdict':verdict})
            return {'review_status':verdict,'snapshot':row['sealed_digest']}

    def _decision(self,sid,rev,kind):
        r=self.conn.execute('SELECT * FROM decisions WHERE id=? AND rev=? AND kind=?',(sid,rev,kind)).fetchone()
        return dict(r) if r else None

    def _save_decision(self,sid,rev,kind,subject,decision,reason,snapshot):
        self.conn.execute('INSERT INTO decisions VALUES (?,?,?,?,?,?,?)',
                          (sid,rev,kind,subject,decision,reason,snapshot))

    def approve(self,sid,rev,actor:Principal,reason:str):
        actor.require('approver')
        if not reason.strip(): raise GateFailure('REASON_REQUIRED')
        with self.transaction():
            row,d=self._load(sid,rev)
            review=self._decision(sid,rev,'review')
            if d['scope']['corpus_sha256']!=self.corpus.corpus_sha256:
                raise GateFailure('CORPUS_PIN_CHANGED')
            if d['policy_version']!=self.policy_version or d['method_version']!=self.method_version:
                raise GateFailure('REQUALIFICATION_REQUIRED')
            if row['phase']!='SEALED' or not review or review['decision']!='SUPPORTED':
                raise GateFailure('SUPPORTED_REVIEW_REQUIRED')
            if actor.subject in {d['author'],review['actor']}:
                raise GateFailure('APPROVER_INDEPENDENCE_REQUIRED')
            if self._decision(sid,rev,'approval'): raise GateFailure('ALREADY_APPROVED')
            if d.get('coverage',{}).get('status')!='FULL_DECLARED':
                raise GateFailure('COVERAGE_LIMITED_NO_FORMAL_ACCEPTANCE')
            if d['scope']['source_authenticity']=='SYNTHETIC_TEST_ONLY':
                if not self.allow_fixture_release: raise GateFailure('SYNTHETIC_SOURCE_CANNOT_APPROVE')
            elif not self.source_qualification:
                raise GateFailure('SOURCE_QUALIFICATION_NOT_ATTESTED')
            self._save_decision(sid,rev,'approval',actor.subject,'ACCEPTED',reason,row['sealed_digest'])
            self._event(sid,rev,'G9_ACCEPTED',actor.subject,{'reason':reason})
            return {'approval_status':'ACCEPTED','scope':d['scope'],'digest':row['sealed_digest']}

    def release(self,sid,rev,actor:Principal,reason:str):
        actor.require('publisher')
        if not reason.strip(): raise GateFailure('REASON_REQUIRED')
        with self.transaction():
            row,d=self._load(sid,rev)
            if actor.subject==d['author']: raise GateFailure('PUBLISHER_INDEPENDENCE_REQUIRED')
            approval=self._decision(sid,rev,'approval')
            if not approval or approval['decision']!='ACCEPTED': raise GateFailure('NOT_APPROVED')
            if self._decision(sid,rev,'release'): raise GateFailure('ALREADY_RELEASED')
            if self.conn.execute('SELECT 1 FROM invalidations WHERE id=?',(sid,)).fetchone():
                raise GateFailure('NEEDS_REVALIDATION')
            self._save_decision(sid,rev,'release',actor.subject,'RELEASED',reason,row['sealed_digest'])
            self._event(sid,rev,'G12_RELEASED',actor.subject,{'reason':reason})
        return self.public_card(sid)

    def public_card(self,sid):
        st=self.conn.execute('SELECT active_rev FROM studies WHERE id=?',(sid,)).fetchone()
        if not st: raise GateFailure('STUDY_NOT_FOUND')
        rev=st['active_rev']
        row=self.conn.execute('SELECT * FROM revisions WHERE id=? AND rev=?',(sid,rev)).fetchone()
        if not row or row['phase']!='SEALED' or not row['sealed_digest']:
            raise GateFailure('OUTPUT_WITHHELD')
        d=json.loads(row['data'])
        if digest(d)!=row['sealed_digest']: raise GateFailure('LOCK_TAMPER_DETECTED')
        if d['scope']['corpus_sha256']!=self.corpus.corpus_sha256:
            raise GateFailure('CORPUS_PIN_CHANGED')
        if d['policy_version']!=self.policy_version or d['method_version']!=self.method_version:
            raise GateFailure('REQUALIFICATION_REQUIRED')
        if not self.verify_audit_chain(): raise GateFailure('AUDIT_CHAIN_CHANGED')
        if self.conn.execute('SELECT 1 FROM invalidations WHERE id=?',(sid,)).fetchone():
            raise GateFailure('NEEDS_REVALIDATION')
        approvals={k:self._decision(sid,rev,k) for k in ('review','approval','release')}
        if any(v is None or v['snapshot_digest']!=row['sealed_digest'] for v in approvals.values()):
            raise GateFailure('OUTPUT_WITHHELD')
        if approvals['review']['decision']!='SUPPORTED' or approvals['approval']['decision']!='ACCEPTED' or approvals['release']['decision']!='RELEASED':
            raise GateFailure('OUTPUT_WITHHELD')
        if d['scope']['source_authenticity']=='SYNTHETIC_TEST_ONLY' and not self.allow_fixture_release:
            raise GateFailure('SYNTHETIC_SOURCE_CANNOT_PUBLISH')
        if d['scope']['source_authenticity']!='SYNTHETIC_TEST_ONLY' and not self.source_qualification:
            raise GateFailure('SOURCE_QUALIFICATION_NOT_ATTESTED')
        return {'study_id':sid,'revision':rev,'status':'RELEASED',
                'scope':d['scope'],'sealed_digest':row['sealed_digest'],
                'claim':d['hypothesis']['statement'],
                'rival':d['hypothesis']['rival'],
                'limitations':d['limitations'],'countersearch':d['countersearch'],
                'epistemic_status':'SUPPORTED_BY_REVIEW_NOT_CANONICAL_TRUTH',
                'notice':'هذه نتيجة بحثية مؤهلة ضمن نطاقها، وليست يقينًا دلاليًا مطلقًا.'}

    def add_dependency(self,child,parent,parent_revision,actor:Principal):
        actor.require('researcher')
        with self.transaction():
            if not self.conn.execute('SELECT 1 FROM studies WHERE id=?',(child,)).fetchone():
                raise GateFailure('CHILD_NOT_FOUND')
            if not self.conn.execute('SELECT 1 FROM revisions WHERE id=? AND rev=?',(parent,parent_revision)).fetchone():
                raise GateFailure('PARENT_VERSION_NOT_FOUND')
            if child==parent: raise GateFailure('DEPENDENCY_CYCLE')
            # Reject cycles using current graph edges parent -> child.
            seen={child};queue=[parent]
            while queue:
                cur=queue.pop()
                if cur in seen: raise GateFailure('DEPENDENCY_CYCLE')
                seen.add(cur)
                queue.extend([r['parent'] for r in self.conn.execute('SELECT parent FROM dependencies WHERE child=?',(cur,))])
            self.conn.execute('INSERT OR REPLACE INTO dependencies VALUES(?,?,?)',(child,parent,parent_revision))
            self._event(child,self.conn.execute('SELECT active_rev FROM studies WHERE id=?',(child,)).fetchone()[0],
                        'H11_DEPENDENCY',actor.subject,{'parent':parent,'rev':parent_revision})

    def reopen(self,sid,rev,actor:Principal,reason:str):
        actor.require('reviewer')
        if not reason.strip(): raise GateFailure('REASON_REQUIRED')
        with self.transaction():
            row,d=self._load(sid,rev)
            if row['phase']!='SEALED': raise GateFailure('LOCK_REQUIRED')
            new_rev=rev+1
            nd={'id':sid,'revision':new_rev,'mode':d['mode'],'author':d['author'],
                'scope':d['scope'],'selector':d['selector'],'policy_version':d['policy_version'],
                'method_version':d['method_version'],'exposure':d['exposure'],
                'observations':[],'hypothesis':None,'countersearch':None,'limitations':['REOPENED_FROM_'+str(rev)],
                'epistemic_status':'HYPOTHESIS','semantic_review':'NOT_REVIEWED',
                'approval_status':'NOT_GRANTED','release_status':'NOT_RELEASED'}
            self.conn.execute('INSERT INTO revisions(id,rev,phase,data) VALUES(?,?,?,?)',
                              (sid,new_rev,'SCOPED',canon(nd)))
            self.conn.execute('UPDATE studies SET active_rev=? WHERE id=?',(new_rev,sid))
            # Find descendants (H11). Invalidate their current outputs pending replay.
            queue=[sid];seen={sid}
            while queue:
                parent=queue.pop(0)
                for rr in self.conn.execute('SELECT child FROM dependencies WHERE parent=?',(parent,)):
                    child=rr['child']
                    if child not in seen:
                        seen.add(child);queue.append(child)
                        self.conn.execute('INSERT OR REPLACE INTO invalidations(id,reason) VALUES(?,?)',
                                          (child,'DEPENDENCY_REOPENED:'+sid))
            self._event(sid,new_rev,'H11_REOPENED',actor.subject,{'previous_rev':rev,'reason':reason,'invalidated':sorted(seen-{sid})})
            return {'study_id':sid,'revision':new_rev,'affected':sorted(seen-{sid})}

    def inspect(self,sid):
        s=self.conn.execute('SELECT active_rev FROM studies WHERE id=?',(sid,)).fetchone()
        if not s: raise GateFailure('STUDY_NOT_FOUND')
        r=self.conn.execute('SELECT phase,data,sealed_digest FROM revisions WHERE id=? AND rev=?',(sid,s['active_rev'])).fetchone()
        d=json.loads(r['data'])
        decisions={k:self._decision(sid,s['active_rev'],k) for k in ('review','approval','release')}
        return {'phase':r['phase'],'study':d,'sealed_digest':r['sealed_digest'],'decisions':decisions}
