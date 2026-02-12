from pathlib import Path
import os

root = Path('.').resolve()
categories = ['Lisp', 'compiled code', 'other code', 'email', 'docs', 'other']

lisp_ext = {'.lisp', '.llisp', '.lmlisp', '.lispm', '.lispq'}
compiled_ext = {'.fasl', '.unfasl', '.ounfas', '.qfasl'}
other_code_ext = {'.lap', '.decl', '.depend', '.macros', '.patch'}
email_markers = ['mail', 'rmail', 'letter']
doc_ext = {'.doc', '.pub'}
doc_markers = ['resume', 'thesis', 'paper', 'plan', 'talk', 'bib', 'story', 'title', 'dict', 'defns', 'line', 'look.at', 'to.do']

for c in categories:
    Path(c).mkdir(exist_ok=True)

for p in sorted(root.rglob('*')):
    if not p.is_file():
        continue
    rel = p.relative_to(root)

    if rel.parts[0] == '.git':
        continue
    if rel.parts[0] in categories:
        continue
    if len(rel.parts) == 1 and rel.name.startswith('.'):
        continue

    name = p.name
    low = name.lower()
    suf = p.suffix.lower()

    if suf in compiled_ext:
        cat = 'compiled code'
    elif suf in lisp_ext or (low.startswith('lisp.') and suf not in compiled_ext) or (low.endswith('.(init)') and ('lisp' in low or 'lispm' in low)):
        cat = 'Lisp'
    elif suf in other_code_ext or low.endswith('.(init)') or low.endswith('.(dir)'):
        cat = 'other code'
    elif any(m in low for m in email_markers):
        cat = 'email'
    elif suf in doc_ext or any(m in low for m in doc_markers):
        cat = 'docs'
    else:
        cat = 'other'

    dst = root / cat / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    os.replace(p, dst)

print("Done.")
