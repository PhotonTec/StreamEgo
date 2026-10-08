"""Replace WPS's rasterized calligraphic H/S/U with font-independent paths.

The three image XObjects are reused at six positions in the supplied teaser.
Replacing them in place retains every positioning transform and other element.
Requires PyMuPDF; the normalized glyph paths are stored alongside this script.
"""
import json
from pathlib import Path

import fitz


def repair_teaser(source, destination):
    paths = json.loads(Path(__file__).with_name('teaser_math_paths.json').read_text())['labels']
    document = fitz.open(source)
    dimensions = {(66, 62): 'H', (53, 60): 'S', (60, 60): 'U'}
    targets = {image[0]: (image, dimensions[tuple(image[2:4])])
               for image in document[0].get_images()
               if tuple(image[2:4]) in dimensions}
    if len(targets) != 3:
        raise ValueError('Expected the three original WPS math image objects.')
    for xref, (image, label) in targets.items():
        mask = fitz.Pixmap(document, image[1])
        width, height = mask.width, mask.height
        samples = mask.samples
        ink = [(i % width, i // width) for i, value in enumerate(samples) if value >= 128]
        left = min(x for x, _ in ink)
        right = max(x for x, _ in ink) + 1
        top = min(y for _, y in ink)
        bottom = max(y for _, y in ink) + 1
        # PDF image coordinates use a unit square, with y increasing upwards.
        transform = ((right - left) / width, (bottom - top) / height,
                     left / width, (height - bottom) / height)
        sx, sy, tx, ty = transform
        stream = f'q\n0 g\n{sx:.8f} 0 0 {sy:.8f} {tx:.8f} {ty:.8f} cm\n{paths[label]}\nQ\n'
        document.update_object(xref, '<< /Type /XObject /Subtype /Form /FormType 1 '
                               '/BBox [0 0 1 1] /Resources << >> >>')
        document.update_stream(xref, stream.encode('ascii'))
    document.save(destination, garbage=4, deflate=True)
    document.close()


if __name__ == '__main__':
    import sys
    repair_teaser(sys.argv[1], sys.argv[2])
