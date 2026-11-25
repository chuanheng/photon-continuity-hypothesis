"""Check center locations against the original, original publication PDF supplied as a path."""
import hashlib
import json
from pathlib import Path
import sys
import fitz
import numpy as np

def inspect(pdf):
    meta=json.loads(Path(__file__).with_name('figure_inputs.json').read_text())
    if hashlib.sha256(pdf.read_bytes()).hexdigest()!=meta['pdf_sha256']:
        raise ValueError('PDF digest does not match input calibration')
    doc=fitz.open(pdf)
    out={}
    for page,key in [(5,'fig2'),(6,'fig3')]:
        image=fitz.Pixmap(doc,doc[page].get_images()[0][0])
        raster=np.frombuffer(image.samples,np.uint8).reshape(image.height,image.width,image.n)
        result=[]
        for x,y,top,bottom in meta[key]['points']:
            patch=raster[y-2:y+3,x-2:x+3,0]
            result.append(float(np.mean(patch<128)))
        out[key]=result
    return out
if __name__=='__main__':
    print(json.dumps(inspect(Path(sys.argv[1])),indent=2))
