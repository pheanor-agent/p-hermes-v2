"""Arrange already-rendered QA screenshots for visual inspection; no artwork creation."""
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw
import sys

ROOT=Path(__file__).resolve().parents[1]
def main():
    for slug in sys.argv[1:]:
        folder=ROOT/'.work/slide-review'/slug
        paths=sorted(folder.glob('*-1280-final.png'))
        for start in range(0,len(paths),8):
            sheet=Image.new('RGB',(1280,1536),'#d7dde7');draw=ImageDraw.Draw(sheet)
            for j,path in enumerate(paths[start:start+8]):
                x=(j%2)*640;y=(j//2)*384
                with Image.open(path) as im:sheet.paste(ImageOps.contain(im,(640,360)),(x,y))
                draw.text((x+12,y+364),f'{slug} / slide {start+j+1:02}',fill='#19253b')
            output=folder/f'contact-{start//8+1}.png';sheet.save(output)
            print(output.relative_to(ROOT))
if __name__=='__main__':main()
