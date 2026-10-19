"""Extract reference text and render source pages; never translate or overwrite translations."""
import argparse
import hashlib
import json
from pathlib import Path
import pymupdf

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('pdf')
parser.add_argument('--work', required=True)
parser.add_argument('--title', required=True)
parser.add_argument('--lang', default='zh-CN')
args = parser.parse_args()
source, work = Path(args.pdf).resolve(), Path(args.work).resolve()
digest = hashlib.sha256(source.read_bytes()).hexdigest()
manifest = work / 'manifest.json'
if manifest.exists():
    previous = json.loads(manifest.read_text(encoding='utf-8'))
    if previous.get('source_sha256') != digest:
        raise ValueError('Different or untracked source: use a new work directory')
for name in ('images', 'source', 'translations'):
    (work / name).mkdir(parents=True, exist_ok=True)
pages = []
with pymupdf.open(source) as doc:
    if not len(doc):
        raise ValueError('PDF has no pages')
    for num, page in enumerate(doc, 1):
        stem = f'page-{num:04}'
        text = page.get_text(sort=True)
        (work / 'source' / (stem+'.txt')).write_text(text, encoding='utf-8')
        image = f'images/{stem}.png'
        page.get_pixmap(matrix=pymupdf.Matrix(1.8, 1.8)).save(str(work / image))
        pages.append({'translation': f'translations/{stem}.md', 'image': image, 'text_chars': len(text.strip())})
manifest.write_text(json.dumps({'title': args.title, 'lang': args.lang, 'source_sha256': digest, 'source_name': source.name, 'pages': pages}, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'manifest': str(manifest), 'pages': len(pages), 'needs_visual_or_ocr': [i for i,p in enumerate(pages, 1) if p['text_chars'] < 20]}))
