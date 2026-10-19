"""Build agent-translated Markdown pages into an offline bilingual handout."""
import argparse
import base64
import html
import json
from pathlib import Path
import re
import subprocess
import zipfile


def render(text, pandoc):
    result = subprocess.run([pandoc, '-f', 'markdown+tex_math_dollars-raw_html', '-t', 'html5', '--mathml'], input=text, capture_output=True, encoding='utf-8', check=True)
    if result.stderr.strip():
        raise ValueError('Review Pandoc diagnostics: ' + result.stderr)
    if re.search(r'<img\b', result.stdout, re.I):
        raise ValueError('Original page images are embedded separately; remove duplicate Markdown images or extend the builder to embed extra images.')
    return result.stdout


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for key in ('manifest', 'output'):
        parser.add_argument('--' + key, required=True)
    parser.add_argument('--pandoc', default='pandoc')
    parser.add_argument('--stem', default='lecture_bilingual')
    parser.add_argument('--css')
    args = parser.parse_args()
    if not re.fullmatch(r'[\w-]+', args.stem):
        raise ValueError('Invalid filename stem')
    manifest = Path(args.manifest).resolve()
    root = manifest.parent
    data = json.loads(manifest.read_text(encoding='utf-8-sig'))
    pages = data['pages']
    if not pages:
        raise ValueError('No pages')
    if len({p['translation'] for p in pages}) != len(pages):
        raise ValueError('Duplicate translated page')
    blocks, toc, markdown, image_files = [], [], [], []
    for num, page in enumerate(pages, 1):
        content = (root / page['translation']).read_text(encoding='utf-8-sig').strip()
        if not re.match(r'^# [^\n]+', content):
            raise ValueError(f'Page {num} needs a translated # title')
        heading, _, body = content.partition('\n')
        title_html = re.sub(r'^<p>|</p>$', '', render(heading[2:], args.pandoc).strip())
        body_html = render(body, args.pandoc)
        image = root / page['image']
        if image.suffix.lower() != '.png':
            raise ValueError('Use rendered PNG source pages')
        embedded = base64.b64encode(image.read_bytes()).decode('ascii')
        image_name = f'images/page-{num:04}.png'
        image_files.append((image, image_name))
        blocks.append(f'<section id="page-{num}"><h2>{num:02} · {title_html}</h2><div class="spread"><aside class="source"><img src="data:image/png;base64,{embedded}" alt="Original page {num}"><p class="caption">{num} / {len(pages)}</p></aside><article>{body_html}</article></div></section>')
        toc.append(f'<a href="#page-{num}">{num:02}</a>')
        markdown.append(f'## {num:02} · {heading[2:]}\n\n{body.strip()}\n\n![Original page {num}]({image_name})\n')
    css_path = Path(args.css) if args.css else Path(__file__).resolve().parents[1] / 'assets/bilingual.css'
    css = css_path.read_text(encoding='utf-8')
    title = html.escape(data['title'])
    lang = html.escape(data.get('lang', 'zh-CN'), quote=True)
    document = f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><style>{css}</style></head><body><header><h1>{title}</h1></header><nav>'+''.join(toc)+'</nav>'+''.join(blocks)+'</body></html>'
    out = Path(args.output).resolve()
    out.mkdir(parents=True, exist_ok=True)
    target = out / (args.stem + '.html')
    target.write_text(document, encoding='utf-8')
    with zipfile.ZipFile(out / (args.stem + '_markdown.zip'), 'w', zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(args.stem + '.md', '# ' + data['title'] + '\n\n' + '\n'.join(markdown))
        for source, name in image_files:
            archive.write(source, name)
    print(json.dumps({'pages': len(pages), 'html': str(target), 'html_bytes': target.stat().st_size}))


if __name__ == '__main__':
    main()
