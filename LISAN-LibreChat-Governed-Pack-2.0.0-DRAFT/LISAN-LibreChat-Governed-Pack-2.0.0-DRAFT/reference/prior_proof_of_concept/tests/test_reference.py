import unittest
from lisan_ref.core import Engine, FrozenCorpus, Principal, GateError, ToolRequest, allow_tool

A = Principal('researcher1', frozenset({'researcher'}))
V = Principal('reviewer1', frozenset({'reviewer'}))
P = Principal('owner1', frozenset({'approver'}))
PUB = Principal('publisher1', frozenset({'publisher'}))
# Synthetic content. It is NOT Quranic text and cannot qualify a corpus.
CORPUS = FrozenCorpus({'10:1': 'ALPHA BETA', '10:2': 'GAMMA DELTA'}, 'test-sha256-fixture')

class ReferenceTests(unittest.TestCase):
    def setUp(self):
        self.e = Engine(CORPUS)
        self.e.create('demo', A, 'SYNTHETIC_SET:10:1,10:2', {'10:1', '10:2'})

    def assertGate(self, code, callback):
        with self.assertRaises(GateError) as caught: callback()
        self.assertEqual(caught.exception.code, code)

    def seed(self, full=True):
        self.e.observe('demo',1,A,'10:1','ALPHA BETA')
        if full: self.e.observe('demo',1,A,'10:2','GAMMA DELTA')
        self.e.hypothesize('demo',1,A,'SPECULATIVE HYPOTHESIS','REFUTATION CRITERION')
        self.e.record_countersearch('demo',1,A,{'10:1','10:2'} if full else {'10:1'},
                                    'NOT_FOUND_IN_EXAMINED_SCOPE')
        return self.e.lock_internal('demo',1,A,claim_full=full)

    def test_out_of_scope(self):
        self.assertGate('OUT_OF_SCOPE',lambda:self.e.observe('demo',1,A,'10:3','X'))
    def test_wrong_quote(self):
        self.assertGate('CITATION_MISMATCH',lambda:self.e.observe('demo',1,A,'10:1','WRONG'))
    def test_hypothesis_without_evidence(self):
        self.assertGate('HYPOTHESIS_INCOMPLETE',lambda:self.e.hypothesize('demo',1,A,'X','Y'))
    def test_missing_countersearch(self):
        self.e.observe('demo',1,A,'10:1','ALPHA')
        self.e.hypothesize('demo',1,A,'X','Y')
        self.assertGate('STAGE_DENIED',lambda:self.e.lock_internal('demo',1,A))
    def test_dont_invent_counterevidence(self):
        self.assertEqual(self.seed().countersearch_outcome,'NOT_FOUND_IN_EXAMINED_SCOPE')
    def test_partial_full_denied(self):
        self.e.observe('demo',1,A,'10:1','ALPHA')
        self.e.hypothesize('demo',1,A,'X','Y')
        self.e.record_countersearch('demo',1,A,{'10:1'},'UNRESOLVED')
        self.assertGate('COVERAGE_UNVERIFIED',lambda:self.e.lock_internal('demo',1,A,claim_full=True))
    def test_partial_not_approved(self):
        self.seed(full=False)
        self.e.review('demo',1,V,'SUPPORTED')
        self.assertGate('PARTIAL_SCOPE_NOT_APPROVABLE_IN_DEMO',lambda:self.e.approve('demo',1,P))
    def test_cannot_rewrite_lock(self):
        self.seed()
        self.assertGate('STAGE_DENIED',lambda:self.e.observe('demo',1,A,'10:1','ALPHA'))
    def test_author_cannot_review(self):
        self.seed()
        self.assertGate('INDEPENDENT_REVIEWER_REQUIRED',lambda:self.e.review('demo',1,A,'SUPPORTED'))
    def test_author_cannot_approve(self):
        self.seed(); self.e.review('demo',1,V,'SUPPORTED')
        self.assertGate('APPROVAL_AUTHORIZATION_DENIED',lambda:self.e.approve('demo',1,A))
    def test_reviewer_cannot_approve(self):
        self.seed(); self.e.review('demo',1,V,'SUPPORTED')
        self.assertGate('APPROVAL_AUTHORIZATION_DENIED',lambda:self.e.approve('demo',1,Principal('reviewer1',frozenset({'approver'}))))
    def test_no_published_without_approval(self):
        self.seed()
        self.assertGate('OUTPUT_WITHHELD',lambda:self.e.get_published('demo',1))
    def test_release_end_to_end(self):
        s=self.seed(); self.assertEqual(len(s.locked_digest),64)
        self.e.review('demo',1,V,'SUPPORTED'); self.e.approve('demo',1,P)
        self.assertIn('نتيجة مؤهلة',self.e.release('demo',1,PUB))
    def test_stale_revision(self):
        self.seed(); self.e.reopen('demo',1,V)
        self.assertGate('REVISION_CONFLICT',lambda:self.e.observe('demo',1,A,'10:1','ALPHA'))
        self.assertGate('OUTPUT_WITHHELD',lambda:self.e.get_published('demo',2))
    def test_tool_default_deny(self):
        self.assertFalse(allow_tool(ToolRequest('delete_all','NEW_CORPUS_STUDY','OBSERVED',False),A))
    def test_tool_external_requires_locked_and_explicit(self):
        self.assertFalse(allow_tool(ToolRequest('external_compare','NEW_CORPUS_STUDY','OBSERVED',False),A))
        self.assertFalse(allow_tool(ToolRequest('external_compare','POST_LOCK_EXTERNAL_COMPARISON','LOCKED',True,False),A))
        self.assertTrue(allow_tool(ToolRequest('external_compare','POST_LOCK_EXTERNAL_COMPARISON','LOCKED',True,True),A))
    def test_approval_tool_requires_role(self):
        self.assertFalse(allow_tool(ToolRequest('approve','REUSE_QUALIFIED','LOCKED',True),A))
    def test_blind_mode_cannot_access_prior_study(self):
        self.assertFalse(allow_tool(ToolRequest('get_study','INDEPENDENT_DIAGNOSTIC','SCOPED',False),A))
    def test_reviewer_cannot_change_recorded_review_silently(self):
        self.seed(); self.e.review('demo',1,V,'SUPPORTED')
        self.assertGate('REVIEW_ALREADY_RECORDED',lambda:self.e.review('demo',1,V,'REJECTED'))
    def test_repeated_approval_denied(self):
        self.seed(); self.e.review('demo',1,V,'SUPPORTED'); self.e.approve('demo',1,P)
        self.assertGate('APPROVAL_ALREADY_DECIDED',lambda:self.e.approve('demo',1,P))
    def test_authority_not_from_model(self):
        self.assertGate('APPROVAL_AUTHORIZATION_DENIED',lambda:self.e.approve('demo',1,A))

if __name__ == '__main__': unittest.main()
