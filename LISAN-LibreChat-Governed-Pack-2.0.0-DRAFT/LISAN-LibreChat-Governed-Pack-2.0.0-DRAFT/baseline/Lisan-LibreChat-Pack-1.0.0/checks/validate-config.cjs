/* Read-only validation using the pinned upstream LibreChat configSchema. */
const fs = require('node:fs');
const path = require('node:path');
const Module = require('node:module');
const [sourceRoot, dependencyRoot, ...configPaths] = process.argv.slice(2);
if (!sourceRoot || !dependencyRoot || configPaths.length === 0) {
  throw new Error('Usage: node validate-config.cjs <source-root> <node_modules> <yaml> [more-yaml]');
}
process.env.NODE_PATH = dependencyRoot;
Module._initPaths();
const ts = require('typescript');
const yaml = require('js-yaml');
require.extensions['.ts'] = (module, filename) => {
  const source = fs.readFileSync(filename, 'utf8');
  const compiled = ts.transpileModule(source, {
    compilerOptions: { module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2022, esModuleInterop: true },
    fileName: filename,
  });
  module._compile(compiled.outputText, filename);
};
const { configSchema } = require(path.join(sourceRoot, 'packages/data-provider/src/config.ts'));
function inspect(a, b, missing, prefix = '') {
  if (!a || typeof a !== 'object') return;
  for (const key of Object.keys(a)) {
    const p = prefix ? `${prefix}.${key}` : key;
    if (!b || !Object.hasOwn(b, key)) missing.push(p);
    else inspect(a[key], b[key], missing, p);
  }
}
const files = [];
for (const configPath of configPaths) {
  const input = yaml.load(fs.readFileSync(configPath, 'utf8'));
  const result = configSchema.safeParse(input);
  if (!result.success) {
    console.error(JSON.stringify({ file: configPath, issues: result.error.issues }, null, 2));
    process.exit(1);
  }
  const missing = [];
  inspect(input, result.data, missing);
  if (missing.length) {
    console.error(JSON.stringify({ file: configPath, silently_stripped_keys: missing }, null, 2));
    process.exit(1);
  }
  files.push({ file: path.basename(configPath), schema_version: input.version, input_keys_preserved: true });
}
console.log(JSON.stringify({ status: 'PASS', scope: 'LIBRECHAT_CONFIG_SCHEMA_ONLY',
  source_root: sourceRoot, files, deployment: 'NOT_RUN', ui: 'NOT_RUN' }, null, 2));
