#!/usr/bin/env python3
"""Web image pipeline: stock photos (Pexels, downloaded to ../stock) -> responsive WebP; Dropbox/brochure art -> WebP."""
from PIL import Image
import os,glob
Image.MAX_IMAGE_PIXELS=None
O='site/img/'
def webp(im,p,w,q):
    im=im.convert('RGB')
    if im.width>w: im=im.resize((w,round(im.height*w/im.width)),Image.LANCZOS)
    im.save(p,'WEBP',quality=q,method=6);return os.path.getsize(p)
STOCK={'fairway':'8218725','lush':'32401757','bunkers':'6573872','sunset':'6256829','flag':'4398355'}
for n,i in STOCK.items():
    im=Image.open(f'../stock/px-{i}.jpg')
    for w,q in [(640,62),(1280,60),(1920,56)]:
        webp(im,f'{O}stock/{n}-{w}.webp',w,q)
# convert existing art to webp
conv=[('models/*.jpg',640,66),('plans/*-plan.jpg',1400,58),('plans/*-thumb.jpg',560,62),('site-plan.jpg',1400,72),('condo-map.jpg',1300,72),('brochure-map.jpg',1100,64),('rec-centre-layout.jpg',1100,70),('hagen.jpg',1000,70),('sign.jpg',1200,66),('taylor.jpg',480,74),('leigh.jpg',480,74),('team.jpg',1600,70)]
for pat,w,q in conv:
    for f in glob.glob(O+pat):
        webp(Image.open(f),f[:-4]+'.webp',w,q);os.remove(f)
