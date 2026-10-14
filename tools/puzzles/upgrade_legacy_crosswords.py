#!/usr/bin/env python3
"""Add one-character PDF fields to existing raster-grid lesson crosswords.

Default is a DRY RUN: validates all six normal/easy PDFs without touching them.
Apply explicitly with --apply. Leaves original artwork, clues and answer keys
unchanged; orders fields Across-first using contiguous horizontal runs.
"""
from __future__ import annotations
import argparse
import collections
from io import BytesIO
from pathlib import Path
import tempfile
import fitz
import numpy as np
from PIL import Image
import cv2

BASE=Path("assets/puzzles/crosswords")
STEMS=("What-is-FND-crossword","Biopsychosocial-What-crossword","Recovery-crossword")

def grid_boxes(doc,page):
    imgs=page.get_images(full=True)
    if len(imgs)!=1:
        raise ValueError(f"Expected one crossword grid image, found {len(imgs)}")
    xref=imgs[0][0]
    placements=page.get_image_rects(xref)
    if len(placements)!=1:
        raise ValueError(f"Expected one grid image placement, found {len(placements)}")
    source=doc.extract_image(xref)
    arr=np.asarray(Image.open(BytesIO(source["image"])).convert("L"))
    mask=(arr < 150).astype("uint8")*255
    contours,_=cv2.findContours(mask,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    candidates=[]
    for contour in contours:
        x,y,w,h=cv2.boundingRect(contour)
        if 8<=w<=80 and 8<=h<=80 and abs(w-h)<=3:
            candidates.append((x,y,w,h))
    if not candidates:
        raise ValueError("No square borders detected")
    popular=collections.Counter((w,h) for _,_,w,h in candidates).most_common(1)[0]
    side=popular[0][0]
    boxes=[b for b in candidates if abs(b[2]-side)<=1 and abs(b[3]-side)<=1]
    if len(boxes)<50 or len(boxes)!=popular[1]:
        raise ValueError(f"Square-border detection uncertain: {len(boxes)} vs {popular}")
    def pitch(vals):
        unique=sorted(set(vals))
        diffs=[b-a for a,b in zip(unique,unique[1:]) if b-a>2]
        p=collections.Counter(diffs).most_common(1)[0][0]
        if p<8: raise ValueError("No consistent grid pitch")
        return p
    xp=pitch([b[0] for b in boxes])
    yp=pitch([b[1] for b in boxes])
    if abs(xp-yp)>1:raise ValueError(f"Non-square grid spacing {xp}x{yp}")
    ox=min(b[0] for b in boxes);oy=min(b[1] for b in boxes)
    m={}
    for x,y,w,h in boxes:
        col=round((x-ox)/xp);row=round((y-oy)/yp)
        if abs(x-(ox+col*xp))>1 or abs(y-(oy+row*yp))>1:
            raise ValueError("Misaligned grid")
        if (col,row) in m:raise ValueError("Duplicate grid cell")
        m[col,row]=(x,y,w,h)
    pdfplacement=placements[0]
    dx=pdfplacement.width / arr.shape[1]
    dy=pdfplacement.height / arr.shape[0]
    pdf_pitch=xp*dx
    if pdf_pitch<13.5:
        raise ValueError(f"Square too small ({pdf_pitch:.2f}pt); redesign needed")
    return m,pdfplacement,dx,dy,pdf_pitch,arr

def tab_sequence(grid):
    keys=set(grid)
    ordered=[];used=set()
    for y in sorted(set(y for x,y in keys)):
        for x in sorted(set(x for x,y0 in keys if y0==y)):
            if (x-1,y) in keys or (x+1,y) not in keys:continue
            run=[];k=x
            while (k,y) in keys:run.append((k,y));k+=1
            if len(run)>=2:
                for c in run:
                    if c not in used:used.add(c);ordered.append(c)
    for x in sorted(set(x for x,y in keys)):
        for y in sorted(set(y for x0,y in keys if x0==x)):
            if (x,y-1) in keys or (x,y+1) not in keys:continue
            k=y
            while (x,k) in keys:
                if (x,k) not in used:used.add((x,k));ordered.append((x,k))
                k+=1
    for y,x in sorted((y,x) for x,y in keys):
        if (x,y) not in used:ordered.append((x,y));used.add((x,y))
    if len(ordered)!=len(keys) or len(set(ordered))!=len(keys):
        raise ValueError("Tab order lost cells")
    return ordered

def convert(source,destination,expected=None):
    doc=fitz.open(source)
    if len(doc)!=1:raise ValueError(f"{source}: must stay one page")
    page=doc[0]
    if list(page.widgets() or []):raise ValueError(f"{source}: already fillable")
    boxes,placement,dx,dy,side,image=grid_boxes(doc,page)
    if expected is not None and set(boxes)!=expected:
        raise ValueError("Normal and Easy grid cells disagree")
    blank={}
    for pos,(x,y,w,h) in boxes.items():
        # Black filled squares are not writable. Puzzle images are the source of truth.
        pix=image[min(image.shape[0]-1,y+h//2),min(image.shape[1]-1,x+w//2)]
        if pix>110:blank[pos]=(x,y,w,h)
    if len(blank)<len(boxes)*.8:
        raise ValueError("Unexpected number of dark / blocked cells")
    order=tab_sequence(blank)
    for col,row in order:
        x,y,w,h=blank[col,row]
        left=placement.x0+x*dx;top=placement.y0+y*dy
        width=side;height=side
        rect=fitz.Rect(left+max(2,width*.17),top+max(4.0,height*.30),left+width-.4,top+height-.5)
        if not rect.is_valid or rect.width<5 or rect.height<5:raise ValueError("Field rect too small")
        field=fitz.Widget()
        field.field_name=f"cell_{col}_{row}"
        field.field_label=f"Crossword letter at column {col+1}, row {row+1}"
        field.field_type=fitz.PDF_WIDGET_TYPE_TEXT
        field.field_value=""
        field.text_maxlen=1
        field.text_align=1
        field.text_font="Helv"
        field.text_fontsize=min(10,max(8,side*.65))
        field.text_color=(0,0,0)
        field.border_width=0
        field.fill_color=None
        field.rect=rect
        page.add_widget(field)
    doc.xref_set_key(page.xref,"Tabs","/A")
    doc.save(destination,deflate=True,garbage=4)
    doc.close()
    test=fitz.open(destination)
    widgets=list(test[0].widgets() or [])
    if len(widgets)!=len(order) or any(w.text_maxlen!=1 for w in widgets):
        raise ValueError("Fields or character limits did not survive save")
    if [w.field_name for w in widgets]!=[f"cell_{x}_{y}" for x,y in order]:
        raise ValueError("Across-first annotation ordering did not survive")
    if test.xref_get_key(test[0].xref,"Tabs")!=("name","/A"):
        raise ValueError("Missing tab-order directive")
    test.close()
    return set(boxes),len(order),side

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--apply",action="store_true")
    args=parser.parse_args()
    with tempfile.TemporaryDirectory() as td:
        for stem in STEMS:
            shape=None
            for variant in ("","-easy"):
                target=BASE/f"{stem}{variant}-09-2026.pdf"
                doc=fitz.open(target)
                if list(doc[0].widgets() or []):
                    print(f"SKIP already fillable {target.name}")
                    doc.close();continue
                doc.close()
                out=Path(td)/target.name
                coords,n,pitch=convert(target,out,expected=shape)
                if shape is None:shape=coords
                print(f"{'APPLY' if args.apply else 'CHECK'} {target.name}: fields={n} side={pitch:.1f}pt pages=1 tab-order=Across-first size={out.stat().st_size}")
                if args.apply:
                    out.replace(target)
if __name__=="__main__":main()
