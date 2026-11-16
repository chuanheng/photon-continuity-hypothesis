#!/usr/bin/env bash
set -euo pipefail
# v0.87: Run on a computer with a pre-authenticated GitHub clone.
# Args: /path/to/parent_with_photon_v051 ... photon_v066  /path/to/github_clone
ROOT="${1:-/mnt/data}"
TARGET="${2:-photon-continuity-hypothesis}"
BRANCH="research/v0.1-initial-draft"

if [[ ! -d "$TARGET/.git" ]]; then
  echo "ERROR: provide an already authenticated local git clone" >&2
  exit 1
fi
if [[ ! -f "$ROOT/photon_v087/results/historical_file_manifest.json" ]]; then
  echo "ERROR: SHA-256 manifest not found in ROOT/photon_v087" >&2
  exit 1
fi

(cd "$TARGET" && git checkout "$BRANCH")
for n in $(seq -w 051 066); do
  src="$ROOT/photon_v$n"
  [[ -d "$src" ]] || { echo "Missing $src" >&2; exit 1; }
  dest="$TARGET/backfill/photon_v$n"
  mkdir -p "$dest"
  tar --exclude='__pycache__' --exclude='*.pyc' -C "$src" -cf - . | tar -C "$dest" -xf -
done

python - "$ROOT" "$TARGET" <<'PY'
import hashlib,json,pathlib,sys
root,repo=map(pathlib.Path,sys.argv[1:])
m=json.loads((root/'photon_v087/results/historical_file_manifest.json').read_text())
failed=[]
for f in m:
    n=f['version'].split('.')[1].zfill(3)
    path=repo/'backfill'/('photon_v'+n)/f['path']
    if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest()!=f['sha256']:
        failed.append(str(path))
if failed:
    raise SystemExit('Pre-push SHA-256 mismatch:\n'+'\n'.join(failed))
print('Verified',len(m),'original files prior to git commit')
PY

(cd "$TARGET" &&
  git add backfill &&
  if ! git diff --cached --quiet; then
    git commit -m "archive: restore v0.51-v0.66 historical research files"
    git push origin "$BRANCH"
  else
    echo "No new historical changes to commit"
  fi)
echo "Complete. Re-fetch and compare exact bytes remotely before claiming archival completion."
