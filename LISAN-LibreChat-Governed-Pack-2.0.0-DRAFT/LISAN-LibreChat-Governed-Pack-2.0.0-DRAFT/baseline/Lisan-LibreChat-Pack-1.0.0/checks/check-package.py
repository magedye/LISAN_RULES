"""Read-only integrity and cross-reference checks for the authored package."""
from pathlib import Path
import csv
import hashlib
import json
import re
import sys
import zipfile

sys.stdout.reconfigure(encoding='utf-8')
root = Path(__file__).resolve().parents[1]
def readj(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(data): return hashlib.sha256(data).hexdigest()
failures = []
def check(value, message):
    if not value: failures.append(message)

design = readj(root/'evidence/PACKAGE_DESIGN.json')
agents = sorted(p.name.split('.')[0] for p in (root/'agents').glob('*.instructions.md'))
skills = sorted(p.parent.name for p in (root/'skills').glob('*/SKILL.md'))
prompts = sorted(p.name for p in (root/'prompts').glob('P*.md'))
check(agents == sorted(design['agents']) and len(agents) == 10, 'agent catalog mismatch')
check(skills == sorted(design['skills']) and len(skills) == 19, 'skill catalog mismatch')
check(len(prompts) == 12, 'prompt count mismatch')
with (root/'docs/FUNCTION_TRACEABILITY.csv').open(encoding='utf-8-sig', newline='') as f:
    functions = list(csv.DictReader(f))
check(len(functions) == 37 and {x['id'] for x in functions} == set(design['functions']), 'function traceability mismatch')
layers = re.findall(r'^\| (\d+) \|', (root/'docs/07_LAYER_MAP_AR.md').read_text(encoding='utf-8'), re.M)
check(set(map(int, layers)) == set(range(1,31)), '30-layer mapping mismatch')
directives = re.findall(r'^\| (\d+) \|', (root/'docs/13_LISAN_35_DIRECTIVES_AR.md').read_text(encoding='utf-8'), re.M)
check(set(map(int, directives)) == set(range(1,36)), '35-directive mapping mismatch')
evals = readj(root/'templates/EVAL_MATRIX.json')
expected_evals = {f'T{i:02d}' for i in range(1,13)} | {f'LC{i:02d}' for i in range(1,22)}
check({x['id'] for x in evals} == expected_evals and len(evals) == 33, 'behavioral cases mismatch')
check(all(x['verdict'] == 'NOT_RUN' for x in evals), 'unexpected unexecuted behavioral PASS claim')
with (root/'agents/AGENT_CATALOG.csv').open(encoding='utf-8-sig', newline='') as f:
    for row in csv.DictReader(f):
        check(set(filter(None, row['skills'].split(';'))) <= set(skills), f"unknown skill: {row['code']}")
        children = list(filter(None, row['children'].split(';')))
        check(children == (design['core_children'] if row['code'] == 'ORCH' else []), f"bad child allowlist: {row['code']}")

authored = [p for p in root.rglob('*.md') if p.relative_to(root).parts[0] not in {'sources','runtime'}]
links = 0
for p in authored:
    text = p.read_text(encoding='utf-8-sig')
    check('\ufffd' not in text, f'encoding replacement: {p.relative_to(root)}')
    for link in re.findall(r'\[[^\]]+\]\(([^)]+)\)', text):
        if re.match(r'^(https?://|mailto:|#)', link): continue
        target = link.split('#',1)[0].strip('<>')
        check((p.parent/target).exists(), f'broken link: {p.relative_to(root)} -> {target}')
        links += 1
for p in root.rglob('*.json'):
    try: readj(p)
    except Exception as e: failures.append(f'JSON error: {p.relative_to(root)}: {type(e).__name__}')

runtime = readj(root/'evidence/REUSED_RUNTIME_FILES.json')
for entry in runtime:
    check(sha((root/entry['package_path']).read_bytes()) == entry['sha256'], f"runtime changed: {entry['package_path']}")
custody = readj(root/'evidence/INPUT_CUSTODY.json')
for entry in custody:
    if 'copy' in entry:
        check(sha((root/entry['copy']).read_bytes()) == entry['sha256'], f"input copy changed: {entry['copy']}")
archive_checked = False
archive = next((x for x in custody if x.get('source','').endswith('.zip')), None)
if archive and Path(archive['source']).is_file():
    check(sha(Path(archive['source']).read_bytes()) == archive['sha256'], 'original archive hash mismatch')
    with zipfile.ZipFile(archive['source']) as z:
        for entry in runtime:
            check(sha(z.read(entry['archive_entry'])) == entry['sha256'], f"archive runtime mismatch: {entry['package_path']}")
    archive_checked = True
secret_patterns = [re.compile(rb'\bsk-[A-Za-z0-9]{24,}\b'), re.compile(rb'\bghp_[A-Za-z0-9]{30,}\b')]
credential_matches = []
for p in root.rglob('*'):
    if p.is_file() and p.suffix.lower() in {'.md','.json','.yaml','.yml','.txt','.example','.mjs','.cjs','.py'}:
        data = p.read_bytes()
        if any(pattern.search(data) for pattern in secret_patterns): credential_matches.append(str(p.relative_to(root)))
check(not credential_matches, 'credential-like literals found; inspect listed paths without printing secrets')
report = {
    'status': 'PASS' if not failures else 'FAIL', 'scope': 'PACKAGE_STRUCTURE_CUSTODY_AND_AUTHORED_LINKS_ONLY',
    'agents':len(agents), 'skills':len(skills), 'prompts':len(prompts), 'functions':len(functions), 'layers':len(layers),
    'source_directives':len(directives), 'behavioral_cases_prepared_not_run':len(evals),
    'authored_markdown_files':len(authored), 'authored_relative_links_checked':links,
    'runtime_files_unchanged':len(runtime), 'original_archive_checked':archive_checked,
    'credential_like_literal_paths':credential_matches, 'failures':failures,
    'excluded_link_scope':'Original sources and runtime notices retain their source-context links; no remote link availability claim.',
    'not_proven':['LibreChat UI integration','model behavior','semantic correctness','independent review','deployment acceptance']
}
print(json.dumps(report,ensure_ascii=False,indent=2))
sys.exit(0 if not failures else 1)
