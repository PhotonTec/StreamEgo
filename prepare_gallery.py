"""Prepare the original PPT examples for the VGGT-style scene galleries."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import subprocess
import json

ROOT = Path(__file__).resolve().parent
MEDIA = ROOT.parent / '_work/ppt-media'
ASSETS = ROOT / 'dist/assets'
FONT = '/System/Library/Fonts/Supplemental/Arial.ttf'

def metadata(index):
    return json.loads(subprocess.check_output(['ffprobe', '-v', 'quiet', '-show_entries',
        'stream=nb_frames,r_frame_rate:format=duration', '-of', 'json', str(MEDIA/f'media{index}.mp4')]))

def prepare(name, indexes, comparison=False):
    args = []
    for index in indexes:
        args += ['-i', str(MEDIA/f'media{index}.mp4')]
    filters = []
    labels = ['Exocentric input', 'StreamEgo', 'Ground truth', 'EgoX', 'Vista4D', 'Wan-VACE']
    for j, index in enumerate(indexes):
        timing = ''
        if comparison:
            stream = metadata(index)['streams'][0]
            numerator, denominator = map(int, stream['r_frame_rate'].split('/'))
            last_time = (int(stream['nb_frames'])-1)*denominator/numerator
            timing = f'setpts={5/last_time}*(PTS-STARTPTS),'
        filters.append(f'[{j}:v]{timing}fps=24,scale=480:480:force_original_aspect_ratio=decrease,'
            f'pad=480:480:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1,'
            f'drawtext=fontfile={FONT}:text={labels[j]}:fontsize=26:fontcolor=white:x=18:y=18:'
            f'box=1:boxcolor=black@0.65:boxborderw=8[v{j}]')
    layout = '0_0|480_0|960_0|0_480|480_480|960_480' if comparison else '0_0|480_0|960_0'
    filters.append(''.join(f'[v{j}]' for j in range(len(indexes)))+
        f'xstack=inputs={len(indexes)}:layout={layout}:shortest=1[v]')
    target = ASSETS / f'{"comparison" if comparison else "visualization"}-{name}.mp4'
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y',*args,'-filter_complex',';'.join(filters),
        '-map','[v]','-an','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-threads','2',
        '-movflags','+faststart',str(target)],check=True)
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss','0.5','-i',str(target),
        '-frames:v','1','-q:v','3',str(target.with_suffix('.jpg'))],check=True)
    print(target.name,flush=True)

jobs = [('cooking',[3,1,2],False),('piano',[6,5,4],False),('objects',[9,8,7],False),
        ('h2o',[10,11,12,13,14,15],True),('bicycle',[16,17,18,19,20,21],True),
        ('assembly',[22,24,27,23,25,26],True),('cpr',[28,29,30,31,32,33],True),
        ('h2o2',[34,35,36,37,38,39],True),('reading',[40,41,42,43,44,45],True),
        ('cooking',[46,47,48,49,50,51],True)]
with ThreadPoolExecutor(max_workers=3) as pool:
    list(pool.map(lambda args:prepare(*args),jobs))
