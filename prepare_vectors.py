"""Convert the supplied PDF figures to SVG while retaining vector graphics.

Usage: python3 prepare_vectors.py /path/to/paper/figures
Requires pdf2svg and PyMuPDF. The teaser's WPS math bitmaps are repaired
in the PDF first, so both the SVG and linked PDF contain vector H/S/U labels.
"""
from pathlib import Path
import shutil
import subprocess
import sys
from repair_teaser_math import repair_teaser

source = Path(sys.argv[1])
assets = Path(__file__).resolve().parent / 'dist/assets'
for name, filename in [('teaser', 'teaser-region.pdf'),
                       ('teacher', 'pipeline-teacher.pdf'),
                       ('student', 'pipeline-helios-new.pdf'),
                       ('inference-pipeline', 'latency-timeline.pdf')]:
    pdf = assets / f'{name}.pdf'
    if name == 'teaser':
        repair_teaser(source / filename, pdf)
    else:
        shutil.copyfile(source / filename, pdf)
    subprocess.run(['pdf2svg', str(pdf), str(assets / f'{name}.svg')], check=True)
