#!/usr/bin/env python3
"""Make a web export from the current local Twine HTML, without video encoding."""
import argparse,base64,hashlib,html,json,re,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--input',required=True,type=Path,help='Current local Twine HTML export');a=p.parse_args()
root=Path(__file__).resolve().parents[1];text=a.input.read_text();seen={};(root/'assets').mkdir(exist_ok=True)
exts={'image/png':'png','image/jpeg':'jpg','image/svg+xml':'svg','audio/mpeg':'mp3','audio/mp3':'mp3'}
def asset(m):
 raw=base64.b64decode(m[2]);digest=hashlib.sha256(raw).hexdigest();rel='assets/'+digest[:20]+'.'+exts[m[1]]
 if digest not in seen:(root/rel).write_bytes(raw);seen[digest]={'path':rel,'size':len(raw),'sha256':digest}
 return rel
text=re.sub(r'data:((?:image|audio)/[A-Za-z0-9.+-]+);base64,([A-Za-z0-9+/=]+)',asset,text)
chapters={html.unescape(m[1]):html.unescape(m[2]) for m in re.finditer(r'<tw-passagedata\b[^>]*name="([^"]+)"[^>]*>(.*?)</tw-passagedata>',text,re.S)}
for video in json.loads((root/'media-manifest.json').read_text()):
 source=re.search(r'<source\s+src="([^"]+)"',chapters[video['chapter']]);assert source,video['chapter'];text=text.replace(source[1],video['url'])
text=text.replace('<title>毕设</title>','<title>旧页浮生 · 交互影游</title>').replace('请使用同一文件与浏览器继续','请使用同一网站与浏览器继续')
assert not re.search(r'file:/+',text),'Local file URL left in web export'
for m in re.finditer(r'<script\b[^>]*>(.*?)</script>',text,re.S):
 if m[1].strip():subprocess.run(['node','--check','-'],input=m[1],text=True,check=True,capture_output=True)
(root/'index.html').write_text(text);(root/'asset-manifest.json').write_text(json.dumps(list(seen.values()),ensure_ascii=False,indent=2))
print('Updated web export. Video files were not read, encoded, or changed.')
