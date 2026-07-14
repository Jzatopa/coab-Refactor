#!/usr/bin/env python3
import csv,hashlib,json,re,sys
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parent
rows=json.loads((ROOT/'manifest.json').read_text()); summary=json.loads((ROOT/'summary.json').read_text())
with (ROOT/'manifest.csv').open(newline='') as f: csvrows=list(csv.DictReader(f))
assert len(rows)==len(csvrows)==summary['frame_count']==summary['png_count']
assert not summary['errors']
assert summary['block_count']==sum(a['blocks'] for a in summary['archives'])
allowed=re.compile(r'^(TITLE|PIC[1-6]|BIGPIC[1-6]|HEAD[1-6]|BODY[1-6]|FINAL.*)\.DAX$')
assert all(allowed.match(a['archive']) for a in summary['archives'])
assert not any(a['archive'].startswith(('CPIC','TILES','SPRIT','GEO','WALLDEF')) for a in summary['archives'])
seen=set(); dims=set(); animated=0
for r in rows:
    key=(r['archive'],r['block'],r['frame']); assert key not in seen; seen.add(key)
    p=ROOT/r['png']; assert p.is_file()
    with Image.open(p) as im:
        assert im.size==(r['width'],r['height']); assert im.format=='PNG'; dims.add(im.size)
    assert hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256']
    animated+=bool(r['animated'])
# Representative sample: one from every included archive, composited at 1:1 with labels only outside images.
chosen=[]
for a in summary['eligible_archives']:
    chosen.append(next(r for r in rows if r['archive']==a))
thumbs=[]
for r in chosen:
    im=Image.open(ROOT/r['png']).convert('RGB'); thumbs.append((r,im))
cellw=max(im.width for _,im in thumbs)+20; cellh=max(im.height for _,im in thumbs)+42; cols=4; rowsn=(len(thumbs)+cols-1)//cols
sheet=Image.new('RGB',(cellw*cols,cellh*rowsn),(32,32,32)); d=ImageDraw.Draw(sheet)
for i,(r,im) in enumerate(thumbs):
    x=(i%cols)*cellw+10; y=(i//cols)*cellh+24; sheet.paste(im,(x,y)); d.text((x,6+(i//cols)*cellh),f"{r['archive']} b{r['block']} f{r['frame']} {r['width']}x{r['height']}",fill='white')
sheet.save(ROOT/'verification-samples.png')
report={'status':'pass','archives':summary['archive_count'],'blocks':summary['block_count'],'frames':len(rows),'pngs':summary['png_count'],'animated_frame_rows':animated,'unique_dimensions':[list(x) for x in sorted(dims)],'sample_count':len(chosen),'sample_sheet':'verification-samples.png'}
(ROOT/'verification.json').write_text(json.dumps(report,indent=2)+'\n'); print(json.dumps(report,indent=2))
