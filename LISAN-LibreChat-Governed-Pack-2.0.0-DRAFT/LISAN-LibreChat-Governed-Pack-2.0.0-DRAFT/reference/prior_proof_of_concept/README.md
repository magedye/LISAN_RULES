# LISAN Enforcement — Reference Proof of Concept (Non-production)

Run: `python -m unittest discover -s tests -v` from the package directory (Python 3.11+).

This implements a small **executable illustration** of selected LISAN gates: a pinned synthetic corpus, exact quote checks, declared scope, epistemic stages, countersearch registration, content digest sealing, revision checks, separation of author/reviewer/approver/publisher, default-deny tool policy, and protected publication.

**Not implemented:** real Quran corpus adapter, authoritative authentication and role assignments, durable database transactions, tenant isolation, full router, actual native LibreChat hook API, async scheduling, signature key custody, policy distribution, full 30+ acceptance tests, semantic judgment, heritage detection, external-source validation, network control, real output-stream interception. Do not deploy as-is. In particular, the `Principal` must be created from server-verified credentials, not an LLM argument.

The `FrozenCorpus` in the tests contains **non-Quranic synthetic strings**. No semantic acceptance is asserted. The included 21-test unit suite was executed successfully during drafting. A green test suite is evidence only that these toy invariants hold under the included fixtures.
