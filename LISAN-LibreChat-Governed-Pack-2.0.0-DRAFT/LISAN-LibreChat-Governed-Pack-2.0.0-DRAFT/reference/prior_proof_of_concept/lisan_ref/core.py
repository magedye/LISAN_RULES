"""Pure-python reference of LISAN boundaries and phase control.

NO semantic authority, networking, authentication provider, DB or LibreChat integration.
All callers must authenticate before creating trusted Principal instances.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from copy import deepcopy
from hashlib import sha256
from threading import RLock
import json

class GateError(Exception):
    def __init__(self, code: str):
        self.code = code
        super().__init__(code)

@dataclass(frozen=True)
class Principal:
    subject: str
    roles: frozenset[str]   # MUST be supplied by trusted server-side identity middleware

@dataclass
class Study:
    study_id: str
    revision: int
    author_id: str
    corpus_digest: str
    selector: str
    expected_refs: frozenset[str]
    method_revision: str = 'method-demo-v1'
    policy_revision: str = 'policy-demo-v1'
    stage: str = 'SCOPED'
    observations: dict[str, str] = field(default_factory=dict)
    hypothesis: str | None = None
    falsification_condition: str | None = None
    countersearch_outcome: str | None = None
    countersearch_refs: frozenset[str] = frozenset()
    limitations: list[str] = field(default_factory=list)
    locked_digest: str | None = None
    semantic_review: str = 'NOT_REVIEWED'
    reviewer_id: str | None = None
    approval: str = 'NOT_GRANTED'
    approver_id: str | None = None
    release: str = 'NOT_RELEASED'

@dataclass(frozen=True)
class ToolRequest:
    tool_name: str
    mode: str
    phase: str
    study_locked: bool
    external_requested: bool = False

_READ_ONLY = frozenset({'get_verse', 'search', 'count', 'verify_quote', 'get_study'})


def allow_tool(request: ToolRequest, principal: Principal) -> bool:
    """Small example of default deny, NOT a LibreChat callback signature."""
    if not principal.subject:
        return False
    if request.tool_name in _READ_ONLY:
        if request.tool_name == 'get_study' and request.mode == 'INDEPENDENT_DIAGNOSTIC':
            return False
        return True
    if request.tool_name == 'external_compare':
        return (request.mode == 'POST_LOCK_EXTERNAL_COMPARISON'
                and request.study_locked and request.external_requested)
    if request.tool_name == 'submit_draft':
        return request.mode in {'NEW_CORPUS_STUDY', 'CUMULATIVE_EXTENSION', 'INDEPENDENT_DIAGNOSTIC'}
    if request.tool_name == 'review':
        return 'reviewer' in principal.roles and request.study_locked
    if request.tool_name == 'approve':
        return 'approver' in principal.roles and request.study_locked
    if request.tool_name == 'release':
        return 'publisher' in principal.roles and request.study_locked
    return False


class FrozenCorpus:
    """Synthetic fixture: strings are not Quranic text. Replace with qualified corpus adapter."""
    def __init__(self, verses: dict[str, str], corpus_digest: str):
        if not verses or not corpus_digest:
            raise ValueError('CORPUS_IDENTITY_REQUIRED')
        self.verses = dict(verses)
        self.digest = corpus_digest

    def verify(self, ref: str, exact_excerpt: str) -> None:
        original = self.verses.get(ref)
        if original is None or not exact_excerpt or exact_excerpt not in original:
            raise GateError('CITATION_MISMATCH')


class Engine:
    def __init__(self, corpus: FrozenCorpus):
        self.corpus = corpus
        self._studies: dict[str, Study] = {}
        self._lock = RLock()
        self.events: list[dict] = []

    def _record(self, code: str, study: Study, principal: Principal):
        self.events.append({'event': code, 'study_id': study.study_id,
                            'revision': study.revision, 'actor': principal.subject})

    def _get(self, study_id: str, expected_revision: int) -> Study:
        s = self._studies.get(study_id)
        if s is None: raise GateError('STUDY_NOT_FOUND')
        if s.revision != expected_revision: raise GateError('REVISION_CONFLICT')
        if s.corpus_digest != self.corpus.digest: raise GateError('CORPUS_CHANGED')
        return s

    def create(self, study_id: str, principal: Principal, selector: str,
               expected_refs: set[str]) -> Study:
        with self._lock:
            if not principal.subject: raise GateError('UNAUTHENTICATED')
            if study_id in self._studies: raise GateError('ALREADY_EXISTS')
            if not selector or not expected_refs or not expected_refs <= self.corpus.verses.keys():
                raise GateError('INVALID_SCOPE')
            s = Study(study_id, 1, principal.subject, self.corpus.digest,
                      selector, frozenset(expected_refs))
            self._studies[study_id] = s
            self._record('G0_SCOPED', s, principal)
            return deepcopy(s)

    def observe(self, study_id: str, revision: int, principal: Principal,
                ref: str, exact_excerpt: str) -> Study:
        with self._lock:
            s = self._get(study_id, revision)
            if principal.subject != s.author_id: raise GateError('AUTHOR_REQUIRED')
            if s.stage not in {'SCOPED','OBSERVED'}: raise GateError('STAGE_DENIED')
            if ref not in s.expected_refs: raise GateError('OUT_OF_SCOPE')
            self.corpus.verify(ref, exact_excerpt)
            s.observations[ref] = exact_excerpt
            s.stage = 'OBSERVED'
            self._record('G3_OBSERVED', s, principal)
            return deepcopy(s)

    def hypothesize(self, study_id: str, revision: int, principal: Principal,
                    statement: str, reject_if: str) -> Study:
        with self._lock:
            s = self._get(study_id, revision)
            if principal.subject != s.author_id: raise GateError('AUTHOR_REQUIRED')
            if s.stage != 'OBSERVED' or not statement.strip() or not reject_if.strip():
                raise GateError('HYPOTHESIS_INCOMPLETE')
            s.hypothesis, s.falsification_condition = statement, reject_if
            s.stage = 'HYPOTHESIZED'
            self._record('G4_HYPOTHESIZED', s, principal)
            return deepcopy(s)

    def record_countersearch(self, study_id: str, revision: int, principal: Principal,
                             searched_refs: set[str], outcome: str) -> Study:
        with self._lock:
            s = self._get(study_id, revision)
            if principal.subject != s.author_id: raise GateError('AUTHOR_REQUIRED')
            if s.stage != 'HYPOTHESIZED': raise GateError('COUNTERSEARCH_NOT_RUN')
            if not searched_refs or not searched_refs <= s.expected_refs:
                raise GateError('COUNTERSEARCH_SCOPE_INVALID')
            if outcome not in {'COUNTERS', 'SUPPORTS', 'UNRESOLVED', 'NOT_FOUND_IN_EXAMINED_SCOPE'}:
                raise GateError('COUNTERSEARCH_OUTCOME_INVALID')
            s.countersearch_refs = frozenset(searched_refs)
            s.countersearch_outcome = outcome
            s.stage = 'COUNTER_CHECKED'
            self._record('G5_COUNTER_CHECKED', s, principal)
            return deepcopy(s)

    def lock_internal(self, study_id: str, revision: int, principal: Principal,
                      claim_full: bool = False) -> Study:
        with self._lock:
            s = self._get(study_id, revision)
            if principal.subject != s.author_id: raise GateError('AUTHOR_REQUIRED')
            if s.stage != 'COUNTER_CHECKED': raise GateError('STAGE_DENIED')
            complete = (set(s.observations) == set(s.expected_refs)
                        and set(s.countersearch_refs) == set(s.expected_refs))
            if claim_full and not complete: raise GateError('COVERAGE_UNVERIFIED')
            if not complete: s.limitations.append('PARTIAL_SCOPE')
            semantic = {'study_id': s.study_id, 'revision': s.revision,
                        'corpus_digest': s.corpus_digest, 'selector': s.selector,
                        'expected_refs': sorted(s.expected_refs),
                        'observations': dict(sorted(s.observations.items())),
                        'hypothesis': s.hypothesis,
                        'falsification_condition': s.falsification_condition,
                        'countersearch_refs': sorted(s.countersearch_refs),
                        'countersearch_outcome': s.countersearch_outcome,
                        'limitations': s.limitations}
            canonical = json.dumps(semantic, ensure_ascii=False, sort_keys=True,
                                   separators=(',', ':')).encode('utf-8')
            s.locked_digest = sha256(canonical).hexdigest()
            s.stage = 'LOCKED'
            self._record('G7_INTERNAL_LOCKED', s, principal)
            return deepcopy(s)

    def review(self, study_id: str, revision: int, principal: Principal,
               assessment: str) -> Study:
        with self._lock:
            s = self._get(study_id, revision)
            if 'reviewer' not in principal.roles or principal.subject == s.author_id:
                raise GateError('INDEPENDENT_REVIEWER_REQUIRED')
            if s.stage != 'LOCKED': raise GateError('REVIEW_REQUIRES_LOCK')
            if s.semantic_review != 'NOT_REVIEWED': raise GateError('REVIEW_ALREADY_RECORDED')
            if assessment not in {'SUPPORTED', 'UNRESOLVED', 'REJECTED'}:
                raise GateError('INVALID_REVIEW')
            s.semantic_review, s.reviewer_id = assessment, principal.subject
            self._record('G8_REVIEWED', s, principal)
            return deepcopy(s)

    def approve(self, study_id: str, revision: int, principal: Principal) -> Study:
        with self._lock:
            s = self._get(study_id, revision)
            if 'approver' not in principal.roles or principal.subject in {s.author_id, s.reviewer_id}:
                raise GateError('APPROVAL_AUTHORIZATION_DENIED')
            if s.stage != 'LOCKED' or s.semantic_review != 'SUPPORTED':
                raise GateError('REVIEW_NOT_SUPPORTED')
            if s.approval != 'NOT_GRANTED': raise GateError('APPROVAL_ALREADY_DECIDED')
            if 'PARTIAL_SCOPE' in s.limitations:
                raise GateError('PARTIAL_SCOPE_NOT_APPROVABLE_IN_DEMO')
            s.approval, s.approver_id = 'ACCEPTED', principal.subject
            self._record('G9_ACCEPTED', s, principal)
            return deepcopy(s)

    def release(self, study_id: str, revision: int, principal: Principal) -> str:
        with self._lock:
            s = self._get(study_id, revision)
            if 'publisher' not in principal.roles: raise GateError('PUBLISHER_REQUIRED')
            if s.approval != 'ACCEPTED': raise GateError('NOT_GRANTED')
            s.release = 'RELEASED'
            self._record('G12_RELEASED', s, principal)
            return self.get_published(study_id, revision)

    def get_published(self, study_id: str, revision: int) -> str:
        with self._lock:
            s = self._get(study_id, revision)
            if s.release != 'RELEASED' or s.approval != 'ACCEPTED' or s.semantic_review != 'SUPPORTED':
                raise GateError('OUTPUT_WITHHELD')
            return ('نتيجة مؤهلة للنطاق المحدد فقط | دراسة: ' + s.study_id
                    + ' | نسخة: ' + str(s.revision)
                    + ' | بصمة القفل: ' + s.locked_digest
                    + '\nالفرضية المراجعة: ' + (s.hypothesis or '')
                    + '\nقيد: الاعتماد لا يمنح يقيناً دلالياً مطلقاً.')

    def reopen(self, study_id: str, revision: int, principal: Principal) -> Study:
        with self._lock:
            s = self._get(study_id, revision)
            if 'reviewer' not in principal.roles and 'approver' not in principal.roles:
                raise GateError('REOPEN_AUTHORIZATION_DENIED')
            if s.stage != 'LOCKED': raise GateError('REOPEN_REQUIRES_LOCK')
            new = Study(study_id, s.revision + 1, s.author_id, s.corpus_digest,
                        s.selector, s.expected_refs, s.method_revision, s.policy_revision)
            new.limitations = ['PREVIOUS_REVISION_REOPENED']
            self._studies[study_id] = new
            self._record('REOPENED_NEW_REVISION', new, principal)
            return deepcopy(new)
