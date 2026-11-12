#!/usr/bin/env python3
"""Regenerates web images from the Dropbox downloads in ../src_assets (floor plans PDF pages rendered to ../src_assets/fp)."""
from PIL import Image
S='../src_assets/fp/';O='site/img/'
def save(im,p,w,q):
    im=im.convert('RGB')
    if im.width>w: im=im.resize((w,int(im.height*w/im.width)),Image.LANCZOS)
    im.save(p,quality=q,optimize=True,progressive=True)
elev={'grand-cypress':[1],'doral':[3,4],'augusta':[6,7],'castle-pines':[9,10],'innisbrook':[12,13],'pebble-beach':[15,16],'pinehurst':[18,19]}
plans={'grand-cypress':2,'doral':5,'augusta':8,'castle-pines':11,'innisbrook':14,'pebble-beach':17,'pinehurst':20}
for m,pgs in elev.items():
    for i,p in enumerate(pgs): save(Image.open(f'{S}pg-{p:02d}.png'),f'{O}models/{m}-elev{i+1}.jpg',640,66)
for m,p in plans.items():
    im=Image.open(f'{S}plan_rot_{p:02d}.png');save(im,f'{O}plans/{m}-plan.jpg',1400,58);save(im,f'{O}plans/{m}-plan-thumb.jpg',560,64)
