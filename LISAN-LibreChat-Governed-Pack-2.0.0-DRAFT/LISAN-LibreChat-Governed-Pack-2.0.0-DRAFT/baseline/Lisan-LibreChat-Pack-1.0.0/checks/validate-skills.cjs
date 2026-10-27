/* Parses authored SKILL.md files with the pinned upstream parser. No app writes. */
const fs = require('node:fs');
const path = require('node:path');
const Module = require('node:module');
const assert = require('node:assert/strict');
const [sourceRoot, dependencyRoot] = process.argv.slice(2);
if (!sourceRoot || !dependencyRoot) throw new Error('Usage: node validate-skills.cjs <upstream-root> <node_modules>');
process.env.NODE_PATH = dependencyRoot;
Module._initPaths();
const ts = require('typescript');
require.extensions['.ts'] = (module, filename) => {
  const { outputText } = ts.transpileModule(fs.readFileSync(filename, 'utf8'), {
    compilerOptions: { module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2022, esModuleInterop: true },
    fileName: filename,
  });
  module._compile(outputText, filename);
};
const { parseSkillMarkdown } = require(path.join(sourceRoot, 'packages/api/src/skills/parse.ts'));
const root = path.resolve(__dirname, '../skills');
const skills = [];
for (const dir of fs.readdirSync(root, { withFileTypes: true })) {
  if (!dir.isDirectory()) continue;
  const raw = fs.readFileSync(path.join(root, dir.name, 'SKILL.md'), 'utf8');
  const parsed = parseSkillMarkdown(raw);
  assert.ok(!parsed.parseError, `${dir.name}: parse error`);
  assert.equal(parsed.invalidBooleans.length, 0);
  assert.equal(parsed.name, dir.name);
  assert.match(parsed.name, /^[a-z0-9][a-z0-9-]{0,63}$/);
  assert.ok(parsed.description.length > 0 && parsed.description.length <= 1024);
  assert.ok(raw.length <= 100000);
  assert.ok(!Object.keys(parsed.frontmatter || {}).some(k => k.replace(/-/g, '').toLowerCase() === 'allowedtools'));
  skills.push({ name: parsed.name, length: raw.length });
}
assert.equal(skills.length, 19);
console.log(JSON.stringify({ status: 'PASS', scope: 'UPSTREAM_SKILL_PARSER_AND_AUTHORED_PACKAGE_LIMITS',
  source_root: sourceRoot, skills, tools_expanded_by_skills: false, ui_loading: 'NOT_RUN' }, null, 2));
