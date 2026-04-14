#!/usr/bin/env python3
"""Download arXiv LaTeX source files for papers listed in people YAML files.

Usage:
  python3 scripts/download-arxiv-sources.py [slug1 slug2 ...]
  python3 scripts/download-arxiv-sources.py --all

Downloads to data/papers/sources/{arxiv_id}/
"""

import yaml
import os
import sys
import subprocess
import time
import tarfile
import gzip
import shutil

PEOPLE_DIR = "data/people"
SOURCES_DIR = "data/papers/sources"

def get_paper_ids(slugs=None):
    """Extract arXiv IDs from people YAML files."""
    ids = set()
    people_dir = PEOPLE_DIR
    files = os.listdir(people_dir)
    for f in sorted(files):
        if not f.endswith('.yaml'):
            continue
        slug = f.replace('.yaml', '')
        if slugs and slug not in slugs:
            continue
        with open(os.path.join(people_dir, f)) as fh:
            p = yaml.safe_load(fh) or {}
        for pub in (p.get('publications') or []):
            aid = pub.get('id', '')
            if aid and not aid.startswith('['):
                ids.add(aid)
    return sorted(ids)

def download_source(arxiv_id, out_dir):
    """Download and extract arXiv source for a paper."""
    paper_dir = os.path.join(out_dir, arxiv_id)
    if os.path.exists(paper_dir) and any(
        f.endswith('.tex') for f in os.listdir(paper_dir)
    ):
        return "exists"

    os.makedirs(paper_dir, exist_ok=True)
    url = f"https://arxiv.org/e-print/{arxiv_id}"
    tmp_file = os.path.join(paper_dir, "source.tar.gz")

    # Download
    result = subprocess.run(
        ['curl', '-sL', '--noproxy', '*', '--max-time', '30',
         '-o', tmp_file, url],
        capture_output=True, text=True
    )

    if not os.path.exists(tmp_file) or os.path.getsize(tmp_file) < 100:
        shutil.rmtree(paper_dir, ignore_errors=True)
        return "download_failed"

    # Try to extract
    try:
        # Check if it's a tar.gz
        if tarfile.is_tarfile(tmp_file):
            with tarfile.open(tmp_file) as tar:
                tar.extractall(path=paper_dir)
            os.remove(tmp_file)
            return "ok"
        else:
            # Might be a single gzipped file
            try:
                with gzip.open(tmp_file, 'rb') as gz:
                    content = gz.read()
                # Write as .tex
                with open(os.path.join(paper_dir, 'main.tex'), 'wb') as f:
                    f.write(content)
                os.remove(tmp_file)
                return "ok"
            except:
                # Might be plain tex
                os.rename(tmp_file, os.path.join(paper_dir, 'main.tex'))
                return "ok"
    except Exception as e:
        return f"extract_failed: {e}"

def main():
    if '--all' in sys.argv:
        slugs = None
    elif len(sys.argv) > 1:
        slugs = sys.argv[1:]
    else:
        print("Usage: python3 scripts/download-arxiv-sources.py [slug1 slug2 ...] | --all")
        sys.exit(1)

    ids = get_paper_ids(slugs)
    print(f"Found {len(ids)} unique papers to download")

    os.makedirs(SOURCES_DIR, exist_ok=True)
    ok = skip = fail = 0

    for i, aid in enumerate(ids):
        status = download_source(aid, SOURCES_DIR)
        if status == "exists":
            skip += 1
        elif status == "ok":
            ok += 1
            print(f"  [{i+1}/{len(ids)}] {aid} ✓")
        else:
            fail += 1
            print(f"  [{i+1}/{len(ids)}] {aid} ✗ {status}")

        if status != "exists":
            time.sleep(2)  # be nice to arXiv

    print(f"\nDone: {ok} downloaded, {skip} existed, {fail} failed")

if __name__ == '__main__':
    main()
