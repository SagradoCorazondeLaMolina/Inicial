#!/usr/bin/env python3
# Ejecutar: python descargar_fotos.py (necesita Internet y permiso para ver imágenes)
import json, pathlib, urllib.request, urllib.error, re, time
ROOT=pathlib.Path(__file__).resolve().parent
path=ROOT/'fotos.js'
source=path.read_text(encoding='utf-8').removeprefix('window.SCM_PHOTOS = ').strip().rstrip(';')
data=json.loads(source)
for sec in ('portada','galeria'):
    for i,p in enumerate(data[sec],1):
        target=ROOT/p['local']; target.parent.mkdir(parents=True,exist_ok=True)
        if not target.exists():
            url='https://drive.google.com/uc?export=download&id='+p['id']
            req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
            try:
                with urllib.request.urlopen(req,timeout=45) as res:
                    body=res.read(); content_type=res.headers.get('Content-Type','')
                if not content_type.startswith('image/') or len(body)<1000:raise ValueError('Respuesta de Drive no es imagen (verifica acceso público o descarga manual)')
                target.write_bytes(body)
                print('OK',target.relative_to(ROOT),len(body),'bytes')
            except Exception as e:print('PENDIENTE',p['name'],p['id'],str(e)[:160]); continue
        p['src']=p['local'];p['download']=p['local']
path.write_text('window.SCM_PHOTOS = '+json.dumps(data,ensure_ascii=False,indent=2)+';\n',encoding='utf-8')
print('Archivos disponibles:',sum((ROOT/p['local']).exists() for sec in ('portada','galeria') for p in data[sec]),'/34')
