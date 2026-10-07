#!/usr/bin/env python3
"""[Codex] Audit every exported HTML link; this is not factual verification."""
import argparse
import collections
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit


class Document(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'):
            self.ids.add(attrs['id'])
        if tag == 'a' and attrs.get('href'):
            self.links.append(attrs['href'])


def exported_path(root, route):
    target = root / route.strip('/')
    for candidate in (target, Path(str(target) + '.html'), target / 'index.html'):
        if candidate.is_file():
            return candidate
    return None


def audit(root, base):
    documents = {}
    for page in sorted(root.rglob('*.html')):
        document = Document()
        document.feed(page.read_text())
        documents[page] = document
    issues = collections.defaultdict(set)
    count = 0
    for page, document in documents.items():
        for href in document.links:
            count += 1
            url = urlsplit(href)
            if url.hostname == 'arxiv.org' and any(x in url.path for x in ('/doi:', '/openalex:', '/cr:')):
                issues[('wrong-paper-url', href)].add(str(page.relative_to(root)))
            if url.scheme or url.netloc:
                if url.scheme and url.scheme not in ('https', 'http', 'mailto', 'tel'):
                    issues[('unexpected-scheme', href)].add(str(page.relative_to(root)))
                continue
            if url.path.startswith('/') and not (url.path == base or url.path.startswith(base + '/')):
                issues[('missing-base-path', href)].add(str(page.relative_to(root)))
                continue
            if not url.path:
                target = page
            elif url.path.startswith('/'):
                target = exported_path(root, unquote(url.path[len(base):]))
            else:
                route = urljoin('/' + str(page.relative_to(root)), unquote(url.path))
                target = exported_path(root, route)
            if not target:
                issues[('missing-page', href)].add(str(page.relative_to(root)))
            elif url.fragment and target in documents and unquote(url.fragment) not in documents[target].ids:
                issues[('missing-anchor', href)].add(str(page.relative_to(root)))
    return {
        'scope': 'Exported HTML links only; not source accuracy or client-only interactions.',
        'pages': len(documents), 'links': count,
        'issues': [{'type': kind, 'target': target, 'pages': sorted(pages)}
                   for (kind, target), pages in sorted(issues.items())],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path('out'))
    parser.add_argument('--base', default='/mirror-symmetry-atlas')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    report = audit(args.root, args.base.rstrip('/'))
    if not report['pages']:
        parser.error('No exported HTML found; build before auditing.')
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    counts = collections.Counter(issue['type'] for issue in report['issues'])
    print(json.dumps({'pages': report['pages'], 'links': report['links'], 'issue_targets': dict(counts)}, ensure_ascii=False))
    return 1 if report['issues'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
