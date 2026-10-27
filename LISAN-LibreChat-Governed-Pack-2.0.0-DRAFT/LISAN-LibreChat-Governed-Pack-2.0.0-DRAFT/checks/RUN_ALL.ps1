$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
Set-Location $root
python checks/validate_distribution.py
if ($LASTEXITCODE -ne 0) { throw 'Distribution check failed' }
Set-Location (Join-Path $root 'reference')
python -m unittest discover -s tests -v
if ($LASTEXITCODE -ne 0) { throw 'Unit tests failed' }
python -m lisan_gov demo
if ($LASTEXITCODE -ne 0) { throw 'Synthetic demo failed' }
python -m lisan_gov corpus-smoke --stdio '..\baseline\Lisan-LibreChat-Pack-1.0.0\runtime\tools\stdio.mjs'
if ($LASTEXITCODE -ne 0) { throw 'Read-only corpus smoke failed' }
