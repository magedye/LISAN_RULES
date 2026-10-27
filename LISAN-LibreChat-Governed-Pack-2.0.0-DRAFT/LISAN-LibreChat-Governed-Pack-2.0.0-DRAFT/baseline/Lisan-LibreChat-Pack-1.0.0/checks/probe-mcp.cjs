/* Optional read-only protocol check. No LLM calls, database writes, or source edits. */
const { spawn } = require('node:child_process');
const path = require('node:path');
const assert = require('node:assert/strict');
const entry = path.resolve(__dirname, '../runtime/tools/stdio.mjs');
const child = spawn(process.execPath, [entry], { stdio: ['pipe', 'pipe', 'pipe'], windowsHide: true });
let stdout = '', stderr = '';
child.stdout.setEncoding('utf8'); child.stderr.setEncoding('utf8');
child.stdout.on('data', s => stdout += s); child.stderr.on('data', s => stderr += s);
const requests = [
  { jsonrpc: '2.0', id: 1, method: 'initialize', params: { protocolVersion: '2025-11-25', capabilities: {}, clientInfo: { name: 'lisan-package-probe', version: '1.0.0' } } },
  { jsonrpc: '2.0', method: 'notifications/initialized', params: {} },
  { jsonrpc: '2.0', id: 2, method: 'tools/list', params: {} },
  { jsonrpc: '2.0', id: 3, method: 'tools/call', params: { name: 'lisan_status', arguments: {} } },
  { jsonrpc: '2.0', id: 4, method: 'tools/call', params: { name: 'lisan_prepare_research', arguments: { question: 'اشرح المنهج', mode: 'METHOD' } } },
  { jsonrpc: '2.0', id: 5, method: 'tools/call', params: { name: 'lisan_status', arguments: { url: 'https://example.invalid/' } } },
];
const timer = setTimeout(() => { child.kill(); process.exitCode = 1; console.error('TIMEOUT'); }, 60000);
child.on('error', err => { clearTimeout(timer); console.error(err.message); process.exitCode = 1; });
child.on('close', code => {
  clearTimeout(timer);
  try {
    assert.equal(code, 0);
    const lines = stdout.trim().split(/\r?\n/).filter(Boolean).map(JSON.parse);
    const byId = new Map(lines.map(x => [x.id, x]));
    assert.equal(byId.get(1)?.result?.protocolVersion, '2025-11-25');
    const tools = byId.get(2)?.result?.tools;
    assert.equal(tools?.length, 7);
    assert.ok(tools.every(t => t.annotations?.readOnlyHint === true));
    const status = byId.get(3)?.result?.structuredContent;
    assert.ok(status && !byId.get(3).error && !byId.get(3).result.isError, 'status not ready');
    const method = byId.get(4)?.result?.structuredContent;
    assert.equal(method?.status, 'METHOD_ONLY');
    assert.equal(method?.corpus_operations, 0);
    assert.ok(byId.get(5)?.error || byId.get(5)?.result?.isError, 'unknown URL argument not rejected');
    console.log(JSON.stringify({ status: 'PASS', scope: 'LOCAL_STDIO_MECHANICS_ONLY', node: process.version, tools: tools.map(t => t.name), corpus_status: status, method_only: method, invalid_argument_rejected: true, semantic_review: 'NOT_REVIEWED', librechat_ui: 'NOT_RUN', cloud_model_calls: 0 }, null, 2));
  } catch (err) {
    console.error(JSON.stringify({ status: 'FAIL', error: err.message, stderr, responses: stdout.slice(0,4000) })); process.exitCode = 1;
  }
});
child.stdin.end(requests.map(x => JSON.stringify(x)).join('\n') + '\n');
