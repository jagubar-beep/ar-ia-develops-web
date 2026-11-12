"""Validate static files, fragment routes, asset dimensions and catalog privacy."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json, re, subprocess
ROOT=Path(__file__).resolve().parent
class Page(HTMLParser):
    def __init__(self):super().__init__();self.ids=set();self.links=[];self.title=False;self.viewport=False;self.h1=0
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:assert a['id'] not in self.ids;self.ids.add(a['id'])
        if tag=='title':self.title=True
        if tag=='h1':self.h1+=1
        if tag=='meta' and a.get('name')=='viewport':self.viewport=True
        if tag=='img':assert a.get('alt') and a.get('width') and a.get('height')
        if tag=='script':raise AssertionError('No external scripts required for this static site.')
        for key in ('href','src'):
            if key in a:self.links.append(a[key])
pages={}
for f in ROOT.glob('*.html'):
    p=Page();p.feed(f.read_text(encoding='utf-8'));pages[f.name]=p
    assert p.title and p.viewport and p.h1==1,f.name
    text=f.read_text(encoding='utf-8')
    assert 'github.com/jagubar-beep/Librarium' not in text and 'internaltest/' not in text
for name,p in pages.items():
    for value in p.links:
        u=urlsplit(value)
        if u.scheme in ('https','http','mailto','data'):continue
        assert not u.scheme and not u.netloc,value
        target=unquote(u.path) or name
        assert (ROOT/target).is_file(),(name,value)
        if u.fragment:assert u.fragment in pages[target].ids,(name,value)
assert {'frontear','contacto'}.issubset(pages['index.html'].ids)
apps=json.loads((ROOT/'apps.json').read_text(encoding='utf-8'))
assert {'frontear','librarium'}.issubset({a['id'] for a in apps})
for a in apps:
    if a['id'] in ('frontear','librarium'):assert a['repositoryUrl'] is None
    if a['status']!='published':assert a['playStoreUrl'] is None
    for shot in a['screenshots']:
        raw=(ROOT/shot['src']).read_bytes();assert raw.startswith(b'\x89PNG\r\n\x1a\n')
# Historical privacy policy and icon must remain byte-identical.
for name in ('privacidad-frontear.html','frontear.png'):
    original=subprocess.run(['git','show',f'backup/pre-librarium-2026-11-12:{name}'],cwd=ROOT,capture_output=True,check=True).stdout
    current=(ROOT/name).read_bytes()
    if name.endswith('.html'):
        original=original.replace(b'\r\n',b'\n');current=current.replace(b'\r\n',b'\n')
    assert original==current,name
print(f'OK: {len(pages)} pages, every local route/anchor/asset, no private repository or tester link; FronteAR policy and icon unchanged.')
