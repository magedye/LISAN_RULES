import unittest, tempfile, json
from pathlib import Path
from lisan_gov import GateFailure, Principal, Policy, Registry, SyntheticCorpus
from lisan_gov.core import digest

A=Principal('author',frozenset({'researcher'}))
B=Principal('reviewer',frozenset({'reviewer'}))
C=Principal('approver',frozenset({'approver'}))
D=Principal('publisher',frozenset({'publisher'}))
I=Principal('intruder',frozenset())
S=Principal('same_person',frozenset({'researcher','reviewer','approver','publisher'}))

def F(refs=None):
    return {'kind':'EXPLICIT_REFS','refs':refs or ['X:1','X:2']}
class GovernanceTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.corpus=SyntheticCorpus({'X:1':'نص تجريبي ألف','X:2':'نص تجريبي باء','X:3':'نص تجريبي جيم'})
        self.r=Registry(Path(self.tmp.name)/'q.db', self.corpus)
    def tearDown(self):
        self.r.close();self.tmp.cleanup()
    def fails(self,code,func,*args,**kwargs):
        with self.assertRaises(GateFailure) as e:func(*args,**kwargs)
        self.assertEqual(e.exception.code,code)
    def create(self,id='s1',principal=A,refs=None,mode='NEW_CORPUS_STUDY',exposure=None):
        return self.r.create(id,principal,F(refs),mode,exposure)
    def draft(self,id='s1',principal=A,refs=None):
        self.create(id,principal,refs)
        refs=refs or ['X:1','X:2']
        for ref in refs:
            self.r.observe(id,1,principal,ref,self.corpus.verses[ref],kind='FULL')
        self.r.hypothesize(id,1,principal,'فرضية تجريبية محددة','تسقط عند ظهور قرينة مخالفة','فرضية أخرى محتملة','وجه استدلال تجريبي لا يثبت معنى')
        self.r.countersearch(id,1,principal,refs,'NOT_FOUND_IN_EXAMINED_SCOPE','اختبار بحث موثق داخل العينة المحددة','لم يظهر شاهد مقاوم داخل نطاق العينة')
        return self.r.seal(id,1,principal,claim_full=True)
    def qualified(self,id='s1',fixture_release=True):
        self.r.allow_fixture_release=fixture_release
        self.draft(id)
        self.r.review(id,1,B,'SUPPORTED','مراجعة تجريبية فقط لا تعني قبولًا دلاليًا')
        self.r.approve(id,1,C,'قبول fixture حصري في الاختبار')
        return self.r.release(id,1,D,'نشر fixture حصري')

    def test_01_source_identity_is_synthetic(self):
        self.assertEqual(self.corpus.corpus_id,'SYNTHETIC_NON_QURANIC_TEST')
    def test_02_default_tool_deny(self):
        self.assertFalse(Policy.tool_allowed('NEW_CORPUS_STUDY','publish'))
    def test_03_allowed_read_only(self):
        self.assertTrue(Policy.tool_allowed('NEW_CORPUS_STUDY','lisan_verify_quote'))
    def test_04_external_blocked_internal(self):
        self.assertFalse(Policy.tool_allowed('INDEPENDENT_DIAGNOSTIC','external_compare'))
    def test_05_external_available_after_lock_mode(self):
        self.assertTrue(Policy.tool_allowed('POST_LOCK_EXTERNAL_COMPARISON','external_compare'))
    def test_06_external_requires_lock(self):
        self.fails('POST_LOCK_ONLY',Policy.choose_route,explicit_external=True)
    def test_07_independence_forces_diagnostic(self):
        self.assertEqual(Policy.choose_route(explicit_independence=True,finding_accepted=True,covers_question=True),'INDEPENDENT_DIAGNOSTIC')
    def test_08_qualified_reuse(self):
        self.assertEqual(Policy.choose_route(finding_accepted=True,active_compatible=True,covers_question=True),'REUSE_QUALIFIED')
    def test_09_partial_scope_extends(self):
        self.assertEqual(Policy.choose_route(finding_accepted=True,active_compatible=True,covers_question=False),'CUMULATIVE_EXTENSION')
    def test_10_no_acceptance_routes_new(self):
        self.assertEqual(Policy.choose_route(finding_accepted=False),'NEW_CORPUS_STUDY')
    def test_11_unauthenticated_create_denied(self):
        self.fails('ROLE_OR_AUTH_REQUIRED',self.r.create,'x',I,F())
    def test_12_duplicate_study_denied(self):
        self.create();self.fails('STUDY_EXISTS',self.r.create,'s1',A,F())
    def test_13_invalid_scope(self):
        self.fails('SCOPE_INVALID',self.r.create,'s1',A,F(['X:9']))
    def test_14_blind_previous_exposure_denied(self):
        self.fails('BLIND_EXPOSURE_FORBIDDEN',self.r.create,'s1',A,F(),'INDEPENDENT_DIAGNOSTIC',[{'finding':'old'}])
    def test_15_non_quran_evidence_denied(self):
        self.create();self.fails('NON_QURAN_AS_PRIMARY',self.r.observe,'s1',1,A,'X:1','نص تجريبي ألف','FULL',source_label='TAFSIR')
    def test_16_wrong_quote_denied(self):
        self.create();self.fails('QUOTE_NOT_VERIFIED',self.r.observe,'s1',1,A,'X:1','تم تحريف النص','FULL')
    def test_17_out_of_scope_denied(self):
        self.create();self.fails('OUT_OF_SCOPE',self.r.observe,'s1',1,A,'X:3','نص تجريبي جيم','FULL')
    def test_18_annotation_is_candidate_not_direct_semantics(self):
        self.create();d=self.r.observe('s1',1,A,'X:1','نص تجريبي ألف','FULL','فاعل مفترض','STRUCTURAL_CANDIDATE')
        self.assertEqual(d['observations'][0]['annotation_type'],'STRUCTURAL_CANDIDATE')
    def test_19_author_must_match(self):
        self.create();self.fails('ROLE_OR_AUTH_REQUIRED',self.r.observe,'s1',1,B,'X:1','نص تجريبي ألف','FULL')
    def test_20_no_hypothesis_before_observation(self):
        self.create();self.fails('OBSERVATIONS_REQUIRED',self.r.hypothesize,'s1',1,A,'فرضية محددة','شرط رفض كاف','فرضية بديلة','تعليل مطول')
    def test_21_no_empty_warrant(self):
        self.create();self.r.observe('s1',1,A,'X:1','نص تجريبي ألف','FULL')
        self.fails('HYPOTHESIS_INCOMPLETE',self.r.hypothesize,'s1',1,A,'فرضية طويلة كفاية','شرط رفض مفصل','بديل معقول','')
    def test_22_countersearch_cannot_be_skipped(self):
        self.create();self.r.observe('s1',1,A,'X:1','نص تجريبي ألف','FULL')
        self.r.hypothesize('s1',1,A,'فرضية طويلة كفاية','شرط رفض مفصل','بديل معقول','تعليل طويل كفاية')
        self.fails('STAGE_DENIED',self.r.seal,'s1',1,A)
    def test_23_counter_outcome_not_found_is_legal(self):
        self.draft();self.assertEqual(self.r.inspect('s1')['study']['countersearch']['outcome'],'NOT_FOUND_IN_EXAMINED_SCOPE')
    def test_24_full_declared_not_root_semantics(self):
        self.draft();v=self.r.inspect('s1')['study']['coverage']
        self.assertEqual(v['scope'],'DECLARED_SELECTOR_ONLY');self.assertEqual(v['status'],'FULL_DECLARED')
    def test_25_partial_cannot_claim_full(self):
        self.create();self.r.observe('s1',1,A,'X:1','نص تجريبي ألف','FULL')
        self.r.hypothesize('s1',1,A,'فرضية طويلة كفاية','شرط رفض مفصل','بديل معقول','تعليل طويل كفاية')
        self.r.countersearch('s1',1,A,['X:1'],'UNRESOLVED','استقراء جزئي فعلي','التجربة لم تشمل كل المواضع')
        self.fails('FULL_COVERAGE_NOT_PROVEN',self.r.seal,'s1',1,A,True)
        self.assertEqual(self.r.seal('s1',1,A)['coverage']['status'],'PARTIAL')
    def test_26_seal_is_immutable(self):
        self.draft();self.fails('STAGE_DENIED',self.r.observe,'s1',1,A,'X:3','نص تجريبي جيم','FULL')
    def test_27_review_separation(self):
        self.draft('s1',principal=S)
        self.fails('INDEPENDENCE_REQUIRED',self.r.review,'s1',1,S,'SUPPORTED','سبب')
    def test_28_cannot_approve_unreviewed(self):
        self.draft();self.fails('SUPPORTED_REVIEW_REQUIRED',self.r.approve,'s1',1,C,'سبب')
    def test_29_same_approver_as_reviewer_forbidden(self):
        self.draft();self.r.review('s1',1,B,'SUPPORTED','سبب')
        self.fails('ROLE_OR_AUTH_REQUIRED',self.r.approve,'s1',1,B,'سبب')
    def test_30_synthetic_source_never_approved_by_default(self):
        self.draft();self.r.review('s1',1,B,'SUPPORTED','سبب')
        self.fails('SYNTHETIC_SOURCE_CANNOT_APPROVE',self.r.approve,'s1',1,C,'سبب')
    def test_31_publishing_without_approval_blocked(self):
        self.draft();self.fails('NOT_APPROVED',self.r.release,'s1',1,D,'سبب')
    def test_32_unreleased_card_hidden(self):
        self.draft();self.fails('OUTPUT_WITHHELD',self.r.public_card,'s1')
    def test_33_fixture_end_to_end(self):
        c=self.qualified();self.assertEqual(c['status'],'RELEASED');self.assertEqual(c['scope']['corpus_id'],'SYNTHETIC_NON_QURANIC_TEST')
    def test_34_cannot_release_twice(self):
        self.qualified();self.fails('ALREADY_RELEASED',self.r.release,'s1',1,D,'سبب')
    def test_35_stale_version_rejected(self):
        self.qualified();self.r.reopen('s1',1,B,'ظهور دليل للمراجعة')
        self.fails('REVISION_CONFLICT',self.r.review,'s1',1,B,'SUPPORTED','سبب')
    def test_36_reopen_blocks_prior_publication(self):
        self.qualified();self.r.reopen('s1',1,B,'ظهور دليل للمراجعة')
        self.fails('OUTPUT_WITHHELD',self.r.public_card,'s1')
    def test_37_cannot_tamper_sealed_data(self):
        self.qualified()
        self.r.conn.execute("UPDATE revisions SET data=? WHERE id='s1' AND rev=1",('{}',))
        self.fails('LOCK_TAMPER_DETECTED',self.r.public_card,'s1')
    def test_38_event_chain_verifies(self):
        self.draft();self.assertTrue(self.r.verify_audit_chain())
    def test_39_event_chain_detects_change(self):
        self.draft();self.r.conn.execute("UPDATE events SET event='TAMPER' WHERE n=1")
        self.assertFalse(self.r.verify_audit_chain())
    def test_40_dependency_invalidation(self):
        self.qualified('parent');self.qualified('child')
        self.r.add_dependency('child','parent',1,A)
        self.r.reopen('parent',1,B,'دليل مؤثر')
        self.fails('NEEDS_REVALIDATION',self.r.public_card,'child')
    def test_41_dependency_cycle_rejected(self):
        self.create('a');self.create('b')
        self.r.add_dependency('b','a',1,A)
        self.fails('DEPENDENCY_CYCLE',self.r.add_dependency,'a','b',1,A)
    def test_42_no_release_to_same_author(self):
        self.r.allow_fixture_release=True;self.draft('s1',principal=S)
        self.r.review('s1',1,B,'SUPPORTED','سبب')
        self.r.approve('s1',1,C,'سبب')
        self.fails('PUBLISHER_INDEPENDENCE_REQUIRED',self.r.release,'s1',1,S,'سبب')
    def test_43_semantic_review_unsupported_cannot_approve(self):
        self.draft();self.r.review('s1',1,B,'UNRESOLVED','سبب')
        self.fails('SUPPORTED_REVIEW_REQUIRED',self.r.approve,'s1',1,C,'سبب')
    def test_44_partial_never_formal_accepted_even_in_fixture(self):
        self.r.allow_fixture_release=True;self.create();self.r.observe('s1',1,A,'X:1','نص تجريبي ألف','FULL')
        self.r.hypothesize('s1',1,A,'فرضية طويلة كفاية','شرط رفض مفصل','بديل معقول','تعليل طويل كفاية')
        self.r.countersearch('s1',1,A,['X:1'],'UNRESOLVED','بحث جزئي موثق','التحليل يغطي شاهدًا واحدًا')
        self.r.seal('s1',1,A)
        self.r.review('s1',1,B,'SUPPORTED','مراجعة المثال')
        self.fails('COVERAGE_LIMITED_NO_FORMAL_ACCEPTANCE',self.r.approve,'s1',1,C,'سبب')
    def test_45_external_route_after_lock_only(self):
        self.assertEqual(Policy.choose_route(explicit_external=True,locked_internal=True),'POST_LOCK_EXTERNAL_COMPARISON')
    def test_46_scope_provenance_has_no_semantic_exhaustive(self):
        self.create();self.assertFalse(self.r.inspect('s1')['study']['scope']['semantic_exhaustive'])
    def test_47_locked_hash_is_bound_to_exact_snapshot(self):
        lock=self.draft();self.assertEqual(lock['sealed_digest'],digest(self.r.inspect('s1')['study']))
    def test_48_inactive_prior_revision_cannot_be_published(self):
        self.qualified();self.r.reopen('s1',1,B,'دليل مؤثر')
        self.fails('REVISION_CONFLICT',self.r.release,'s1',1,D,'سبب')

    def test_55_policy_version_change_blocks_published_card(self):
        self.qualified();self.r.policy_version='LISAN-POLICY-3.0'
        self.fails('REQUALIFICATION_REQUIRED',self.r.public_card,'s1')
    def test_56_corpus_pin_change_blocks_published_card(self):
        self.qualified();self.r.corpus.corpus_sha256='f'*64
        self.fails('CORPUS_PIN_CHANGED',self.r.public_card,'s1')
    def test_57_audit_change_blocks_publication(self):
        self.qualified();self.r.conn.execute("UPDATE events SET actor='tampered' WHERE n=1")
        self.fails('AUDIT_CHAIN_CHANGED',self.r.public_card,'s1')

if __name__=='__main__': unittest.main()
