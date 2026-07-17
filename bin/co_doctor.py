#!/usr/bin/env python3
import argparse, json, re
from pathlib import Path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--vault', required=True)
    ap.add_argument('--port', required=True)
    args = ap.parse_args()
    vault = Path(args.vault)
    port = Path(args.port)
    issues = []
    for d in ['.raw','wiki/sources','wiki/entities','wiki/concepts','wiki/questions','scripts','Inbox']:
        if not (vault/d).exists():
            issues.append({'level':'error','code':'missing_dir','path':d})
    for f in ['HERMES.md','wiki/index.md','wiki/log.md','wiki/hot.md','.raw/.manifest.json']:
        if not (vault/f).exists():
            issues.append({'level':'error','code':'missing_file','path':f})
    man_path = vault/'.raw'/'.manifest.json'
    if man_path.exists():
        man = json.loads(man_path.read_text(encoding='utf-8'))
        for k in (man.get('sources') or {}):
            if not (vault/k).exists():
                issues.append({'level':'error','code':'manifest_missing','path':k})
    # empty indexes
    for p in (vault/'wiki').rglob('_index.md'):
        if p.stat().st_size < 80:
            issues.append({'level':'warn','code':'thin_index','path':str(p.relative_to(vault))})
    # retrieval readiness
    if not (vault/'.vault-meta'/'bm25'/'index.json').exists():
        issues.append({'level':'warn','code':'bm25_missing'})
    skills = list(Path.home().joinpath('.hermes/skills/note-taking').glob('claude-obsidian*'))
    out = {
        'vault': str(vault),
        'skills': len(skills),
        'issues': issues,
        'error': sum(1 for i in issues if i['level']=='error'),
        'warn': sum(1 for i in issues if i['level']=='warn'),
        'ok': all(i['level']!='error' for i in issues),
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    raise SystemExit(0 if out['ok'] else 1)

if __name__ == '__main__':
    main()
