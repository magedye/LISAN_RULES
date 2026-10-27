# Quran Lisan Candidate — complete delivery package

Created 2026-10-14 from the owner-private Site and plugin state verified for this delivery.

## Contents

- `Site/Source_Snapshot/`: complete tracked source tree at commit `e3a8d156c1b60cb0b50d9a0834688fb0d856eafa`, including corpus, manifests, trust anchors, UI, worker sources, tests, docs, migrations, and build outputs.
- `Site/Source_History.bundle`: Git history and refs for the source repository.
- `Site/Published_Version_7/`: the exact qualified Worker artifact and native Sites deployment archive for the live version 7.
- `Site/Rollback_Version_6/`: the qualified rollback bundle for version 6.
- `Plugin/Complete_Live_Plugin_1.1.0-cumulative.2/`: all 31 files from the current private connected plugin, reconstructed from the retained original plus the qualified overlay.
- `Plugin/*.zip`: original plugin archive and the qualified cumulative overlay, retained as provenance.
- `Qualification_Evidence/`: release qualification, UAT delta, deployment, migration, access, persistence, MCP, plugin, and blocker evidence.
- `SITE_CONFIGURATION_SAFE.json`: Site IDs, private ACL, database binding, deployment identity, migration hashes, plugin identity, and environment-variable names.

## Important limits

- No secret values, bearer tokens, CSRF secret, repository credentials, or browser session material are included. Runtime values are redacted by Sites; only environment-variable names and the last qualified feature-flag states are recorded.
- A full D1 backup is not included. Sites tools did not provide a full export or isolated restore target. The blocker evidence is included; study-level JSON exports are not equivalent to a database backup.
- Version 12 is the newest saved version record but is historical temporary admin-job evidence. It is not live and is not included as a deployable artifact. Version 7 is the verified live deployment; version 6 is the rollback reference.
- The package does not confer `RELEASE_ACCEPTED` or semantic approval. The recorded decision permits only the previously scoped conditional private experiment; continuous use remains unqualified.

## Integrity

`SHA256SUMS.txt` lists hashes for the packaged files. Verify hashes before use. The source Worker SHA-256 is `168015c6e47a1ba86a8a391d071abbf272a31da64f907bb02f3ce5db880e4068`.
