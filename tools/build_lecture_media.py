"""Encode explicitly educational still-shot edits with installed FFmpeg.

This optional authoring tool is separate from the reference compiler.
Run at the repository root. It never invokes a generative model.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from p_hermes.media import inspect_video

def run(args):
    subprocess.run(args,check=True,capture_output=True)

def main():
    media=ROOT/'site/slides/media'
    images=['luma-left.png','luma-detail.png','luma-center.png']
    variants={'edit-a.mp4':[4,4,4],'edit-b.mp4':[2,6,4]}
    manifest={'scope':'Educational editing of synthetic still images using FFmpeg, separate from p-hermes compilation. No generated motion or audio.', 'variants':{}}
    for name,durations in variants.items():
        args=['ffmpeg','-y','-v','error']
        for image,duration in zip(images,durations):args+=['-loop','1','-framerate','25','-t',str(duration),'-i',str(media/image)]
        filters=[]
        for i in range(3):filters.append(f'[{i}:v]scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2:color=0xF6F4ED,setsar=1,fps=25[v{i}]')
        filters.append('[v0][v1][v2]concat=n=3:v=1:a=0[out]')
        args+=['-filter_complex',';'.join(filters),'-map','[out]','-c:v','libx264','-preset','medium','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(media/name)]
        run(args)
        manifest['variants'][name]={'images':images,'durations':durations,'probe':inspect_video(media/name,expected_duration=12)}
    run(['ffmpeg','-y','-v','error','-f','lavfi','-i','testsrc2=size=1280x720:rate=25','-t','2','-c:v','libx264','-pix_fmt','yuv420p','-movflags','+faststart',str(media/'probe-2s.mp4')])
    manifest['probe_fixture']=inspect_video(media/'probe-2s.mp4',expected_duration=2)
    for name,time in [('boundary-before.png','3.96'),('boundary-after.png','4.00')]:
        run(['ffmpeg','-y','-v','error','-ss',time,'-i',str(media/'edit-a.mp4'),'-frames:v','1',str(media/name)])
    for item in manifest['variants'].values():
        item['source_sha256']={name:hashlib.sha256((media/name).read_bytes()).hexdigest() for name in images}
    (ROOT/'content/slides/video-evidence.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Encoded two 12-second edits and a separate 2-second probe fixture; verified all three with the public inspect_video function.')

if __name__=='__main__':main()
