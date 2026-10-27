/* Read-only MCP interoperability check using an existing MCP SDK installation. */
const path = require('node:path');
const fs = require('node:fs');
const assert = require('node:assert/strict');
const Module = require('node:module');
const [dependencyRoot, catalogPath] = process.argv.slice(2);
if (!dependencyRoot) throw new Error('Usage: node probe-sdk.cjs <node_modules> [catalog-output.json]');
process.env.NODE_PATH = dependencyRoot;
Module._initPaths();
const { Client } = require('@modelcontextprotocol/sdk/client/index.js');
const { StdioClientTransport } = require('@modelcontextprotocol/sdk/client/stdio.js');
const client = new Client({ name: 'lisan-package-sdk-probe', version: '1.0.0' }, { capabilities: {} });
const transport = new StdioClientTransport({
  command: process.execPath,
  args: [path.resolve(__dirname, '../runtime/tools/stdio.mjs')],
  stderr: 'pipe',
});
let stderr = '';
const timeout = setTimeout(() => { transport.close(); console.error('TIMEOUT'); process.exitCode = 1; }, 60000);
(async () => {
  try {
    await client.connect(transport);
    if (transport.stderr) transport.stderr.on('data', data => stderr += data.toString());
    const catalog = await client.listTools();
    assert.equal(catalog.tools.length, 7);
    assert.ok(catalog.tools.every(t => t.annotations?.readOnlyHint === true));
    if (catalogPath) fs.writeFileSync(catalogPath, JSON.stringify(catalog, null, 2) + '\n', 'utf8');
    const call = async (name, args) => {
      const result = await client.callTool({ name, arguments: args });
      assert.ok(!result.isError, `${name} failed`);
      assert.ok(result.structuredContent, `${name} has no structuredContent`);
      return result.structuredContent;
    };
    const status = await call('lisan_status', {});
    assert.equal(status.ready, true);
    const got = await call('lisan_get_verses', { refs: ['1:1'], context: 0 });
    const verse = got.verses.find(v => v.ref === '1:1');
    assert.ok(verse?.original_text);
    const exact = await call('lisan_verify_quote', { ref: verse.ref, text: verse.original_text, kind: 'FULL' });
    assert.equal(exact.matched, true);
    const badResult = await client.callTool({ name: 'lisan_verify_quote', arguments: { ref: verse.ref, text: verse.original_text + ' X', kind: 'FULL' } });
    assert.equal(badResult.isError, true);
    const bad = badResult.structuredContent;
    assert.equal(bad.matched, false);
    assert.equal(bad.status, 'QUOTE_NOT_VERIFIED');
    const search = await call('lisan_search', { query: { forms: [verse.original_text], match: 'SUBSTRING', normalization: 'EXACT' }, offset: 0, limit: 1 });
    assert.ok(search.matched_verses >= 1);
    assert.ok(search.match_events >= search.matched_verses);
    assert.equal(search.scan, 'COMPLETE_FOR_DECLARED_QUERY');
    assert.equal(search.semantic_coverage, 'NOT_ESTABLISHED');
    assert.ok(search.occurrences.some(v => v.ref === '1:1'));
    const method = await call('lisan_prepare_research', { question: 'شرح المنهج', mode: 'METHOD' });
    assert.equal(method.corpus_operations, 0);
    let invalidRejected = false;
    try {
      const invalid = await client.callTool({ name: 'lisan_check_study', arguments: {} });
      invalidRejected = invalid.isError === true;
    } catch { invalidRejected = true; }
    assert.ok(invalidRejected);
    console.log(JSON.stringify({ status: 'PASS', scope: 'LOCAL_MCP_SDK_READ_ONLY_INTEROPERABILITY', node: process.version,
      checks: ['sdk_initialize', 'seven_readonly_tools', 'status_ready', 'get_reference', 'exact_quote_accept', 'altered_quote_reject', 'literal_search_metadata', 'method_no_corpus_operations', 'invalid_study_reject'],
      corpus_sha256: status.provenance.corpus_sha256, tools: catalog.tools.map(t => t.name),
      semantic_analysis: 'NOT_PERFORMED', librechat_ui: 'NOT_RUN', cloud_model_calls: 0,
      note: 'A local SDK probe does not qualify the LibreChat host, model behavior, or semantic conclusions.' }, null, 2));
  } catch (error) {
    console.error(JSON.stringify({ status: 'FAIL', message: error.message, stderr }));
    process.exitCode = 1;
  } finally { clearTimeout(timeout); await client.close(); }
})();
