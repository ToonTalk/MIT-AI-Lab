from pathlib import Path
import shutil

root = Path(".").resolve()
categories = ["Lisp", "compiled code", "other code", "email", "docs", "other"]

for cat in categories:
    cat_dir = root / cat
    if not cat_dir.exists():
        continue

    # collect files first so moving doesn't interfere with traversal
    files = [p for p in cat_dir.rglob("*") if p.is_file()]

    for src in files:
        # Skip files already at top level of the category
        if src.parent == cat_dir:
            continue

        rel = src.relative_to(cat_dir)
        parts = rel.parts

        # detect archive id (e.g. 7005017 from 7005017/ken/file)
        archive_id = parts[0] if len(parts) >= 2 else "src"

        # flatten target name
        base_name = src.name
        dst = cat_dir / base_name

        if dst.exists():
            stem = src.stem
            suffix = src.suffix
            dst = cat_dir / f"{stem}_{archive_id}{suffix}"
            i = 2
            while dst.exists():
                dst = cat_dir / f"{stem}_{archive_id}_{i}{suffix}"
                i += 1

        shutil.move(str(src), str(dst))

    # remove empty directories under category
    # deepest first
    for d in sorted([p for p in cat_dir.rglob("*") if p.is_dir()], key=lambda p: len(p.parts), reverse=True):
        try:
            d.rmdir()
        except OSError:
            pass

print("Done flattening category folders.")
