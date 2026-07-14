#!/usr/bin/env python3
"""Extract eligible Curse of the Azure Bonds visual DAX assets to exact-size PNGs."""
from __future__ import annotations
import argparse, csv, json, struct, hashlib
from pathlib import Path
from PIL import Image

EGA=[(0,0,0),(0,0,173),(0,173,0),(0,173,173),(173,0,0),(173,0,173),(173,82,0),(173,173,173),(82,82,82),(82,82,255),(82,255,82),(82,255,255),(255,82,82),(255,82,255),(255,255,82),(255,255,255)]
FIELDS=['archive','area','block','frame','width','height','x','y','category_guess','animated','delay','png','sha256']

def decompress(comp:bytes, raw_size:int)->bytes:
    out=bytearray(); i=0
    while i<len(comp):
        run=struct.unpack_from('<b',comp,i)[0]
        if run>=0:
            n=run+1; out.extend(comp[i+1:i+1+n]); i+=n+1
        else:
            n=-run; out.extend(comp[i+1:i+2]*n); i+=2
    if len(out)!=raw_size: raise ValueError(f'decompressed {len(out)}, expected {raw_size}')
    return bytes(out)

def dax_blocks(path:Path):
    data=path.read_bytes(); header_bytes=struct.unpack_from('<H',data,0)[0]; base=header_bytes+2
    if header_bytes%9: raise ValueError(f'invalid header size {header_bytes}')
    for pos in range(2,base,9):
        block,offset,raw_size,comp_size=struct.unpack_from('<BiHH',data,pos)
        comp=data[base+offset:base+offset+comp_size]
        if len(comp)!=comp_size: raise ValueError(f'block {block}: truncated compressed data')
        yield block,decompress(comp,raw_size)

def pixels_to_png(nibbles:bytes,width:int,height:int,out:Path):
    expected=(width*height)//2
    if len(nibbles)!=expected: raise ValueError(f'pixel bytes {len(nibbles)}, expected {expected}')
    pix=[]
    for b in nibbles: pix.extend((b>>4,b&15))
    im=Image.new('P',(width,height)); palette=[]
    for rgb in EGA: palette.extend(rgb)
    palette.extend([0,0,0]*(256-len(EGA))); im.putpalette(palette)
    im.putdata(pix); out.parent.mkdir(parents=True,exist_ok=True); im.save(out,optimize=False)

def category(name:str)->str:
    if name.startswith('BIGPIC'): return 'large_scene'
    if name.startswith('PIC'): return 'scene_or_event'
    if name.startswith('FINAL'): return 'finale_scene'
    if name.startswith('HEAD'): return 'character_head'
    if name.startswith('BODY'): return 'character_body'
    if name=='TITLE': return 'title_screen'
    return 'unknown'

def extract_standard(name,block,raw):
    if len(raw)<17: raise ValueError('short image block')
    height,width_units,x,y=struct.unpack_from('<hhhh',raw,0); frames=raw[8]
    width=width_units*8; frame_bytes=width*height//2; needed=17+frames*frame_bytes
    if width<=0 or height<=0 or frames<=0 or needed!=len(raw): raise ValueError(f'invalid standard image header/dimensions ({width}x{height}, frames={frames}, bytes={len(raw)}/{needed})')
    return [{'frame':i,'width':width,'height':height,'x':x,'y':y,'delay':None,'pixels':raw[17+i*frame_bytes:17+(i+1)*frame_bytes]} for i in range(frames)]

def extract_pic(name,block,raw):
    if not raw: raise ValueError('empty PIC block')
    count=raw[0]; pos=1; result=[]; first=None
    if count<=0: raise ValueError('zero PIC frames')
    for frame in range(count):
        if pos+19>len(raw): raise ValueError(f'frame {frame}: short header')
        delay=struct.unpack_from('<I',raw,pos)[0]; pos+=4
        height,width_units=struct.unpack_from('<hh',raw,pos); pos+=4
        x,y=struct.unpack_from('<hh',raw,pos); pos+=4
        pos+=1 # format flag/padding byte after y
        pos+=8 # palette/remap metadata
        width=width_units*8; n=width*height//2
        if width<=0 or height<=0 or pos+n>len(raw): raise ValueError(f'frame {frame}: invalid dimensions/data ({width}x{height})')
        enc=bytearray(raw[pos:pos+n]); pos+=n
        if frame==0: first=bytes(enc)
        elif name.startswith(('PIC','FINAL')):
            enc=bytearray(a^b for a,b in zip(enc,first))
        result.append({'frame':frame,'width':width,'height':height,'x':x,'y':y,'delay':delay,'pixels':bytes(enc)})
    if pos!=len(raw): raise ValueError(f'{len(raw)-pos} trailing bytes')
    return result

def eligible(src:Path):
    names=['TITLE.DAX']
    for prefix in ('PIC','BIGPIC','HEAD','BODY'):
        names += [f'{prefix}{i}.DAX' for i in range(1,7)]
    names += sorted(p.name for p in src.glob('FINAL*.DAX'))
    return [src/n for n in names if (src/n).is_file()]

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('source',type=Path); ap.add_argument('--output',type=Path,default=Path(__file__).resolve().parent)
    a=ap.parse_args(); out=a.output.resolve(); pngroot=out/'png'; pngroot.mkdir(parents=True,exist_ok=True)
    rows=[]; archives=[]; errors=[]
    for path in eligible(a.source):
        name=path.stem.upper(); area=int(name[-1]) if name[-1:].isdigit() else None; blocks=0; frames_total=0
        for block,raw in dax_blocks(path):
            blocks+=1
            try: frames=extract_pic(name,block,raw) if name.startswith(('PIC','FINAL')) else extract_standard(name,block,raw)
            except Exception as e: errors.append({'archive':path.name,'block':block,'error':str(e)}); continue
            animated=len(frames)>1; frames_total+=len(frames)
            for f in frames:
                rel=Path('png')/name/f'{name}_block_{block:03d}_frame_{f["frame"]:03d}.png'; dest=out/rel
                pixels_to_png(f['pixels'],f['width'],f['height'],dest)
                rows.append({'archive':path.name,'area':area,'block':block,'frame':f['frame'],'width':f['width'],'height':f['height'],'x':f['x'],'y':f['y'],'category_guess':category(name),'animated':animated,'delay':f['delay'],'png':rel.as_posix(),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()})
        archives.append({'archive':path.name,'area':area,'blocks':blocks,'frames':frames_total,'bytes':path.stat().st_size})
    rows.sort(key=lambda r:(r['archive'],r['block'],r['frame']))
    (out/'manifest.json').write_text(json.dumps(rows,indent=2)+'\n')
    with (out/'manifest.csv').open('w',newline='') as fp:
        w=csv.DictWriter(fp,fieldnames=FIELDS); w.writeheader(); w.writerows(rows)
    summary={'source':str(a.source.resolve()),'eligible_archives':[p.name for p in eligible(a.source)],'archive_count':len(archives),'block_count':sum(x['blocks'] for x in archives),'frame_count':len(rows),'png_count':sum(1 for _ in pngroot.rglob('*.png')),'archives':archives,'errors':errors}
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    if errors: raise SystemExit(f'extraction completed with {len(errors)} errors; see summary.json')
    print(json.dumps(summary,indent=2))
if __name__=='__main__': main()
