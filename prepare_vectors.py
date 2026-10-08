"""Convert the supplied PDF figures to SVG while retaining vector graphics.

Usage: python3 prepare_vectors.py /path/to/paper/figures
Requires pdf2svg. The webpage links directly to the original PDFs as well.
"""
from pathlib import Path
import shutil
import subprocess
import sys

source = Path(sys.argv[1])
assets = Path(__file__).resolve().parent / 'dist/assets'
for name, filename in [('teaser', 'teaser-region.pdf'),
                       ('teacher', 'pipeline-teacher.pdf'),
                       ('student', 'pipeline-helios-new.pdf'),
                       ('inference-pipeline', 'latency-timeline.pdf')]:
    subprocess.run(['pdf2svg', str(source / filename), str(assets / f'{name}.svg')], check=True)
    shutil.copyfile(source / filename, assets / f'{name}.pdf')
