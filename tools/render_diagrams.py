"""Render tutorial SVGs at mobile width for visual review.

Requires Inkscape and Pillow only for review; SVG generation uses stdlib.
Usage: python tools/render_diagrams.py /tmp/tutorial-diagram-review
"""
from pathlib import Path
import subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageDraw
root=Path(__file__).resolve().parents[1]
out=Path(sys.argv[1] if len(sys.argv)>1 else '/tmp/tutorial-diagram-review')
out.mkdir(parents=True,exist_ok=True)
files=sorted((root/'assets/diagrams').glob('*.svg'))
def render(f):
 subprocess.run(['inkscape',str(f),'--export-type=png','--export-width=375','--export-filename='+str(out/(f.stem+'.png'))],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
with ThreadPoolExecutor(max_workers=4) as pool:
 list(pool.map(render, files))
for start in range(0,len(files),4):
 batch=files[start:start+4]
 ims=[Image.open(out/(f.stem+'.png')).convert('RGB') for f in batch]
 sheet=Image.new('RGB',(790,max(im.height for im in ims[:2])+max([im.height for im in ims[2:]] or [0])+100),'#dce2e8')
 d=ImageDraw.Draw(sheet)
 row_y=0
 for i,im in enumerate(ims):
  if i==2:row_y=max(z.height for z in ims[:2])+50
  x=10+(i%2)*395
  d.text((x,row_y+8),batch[i].stem,fill='#182638')
  sheet.paste(im,(x,row_y+30))
 sheet.save(out/f'review-{start//4+1:02d}.png')
print(f'Rendered {len(files)} figures at 375 px into {out}')
