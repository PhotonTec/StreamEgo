"""Embed PDF image transparency directly, avoiding browser SVG mask filters.

pdf2svg exports a color image and grayscale soft mask as separate images.
Combine their original pixels into lossless RGBA PNGs without resizing; leave
the SVG's vector paths, clipping paths and placement transforms untouched.
"""
import base64
import io
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image

SVG = 'http://www.w3.org/2000/svg'
XLINK = 'http://www.w3.org/1999/xlink'
HREF = '{' + XLINK + '}href'
ET.register_namespace('', SVG)
ET.register_namespace('xlink', XLINK)


def normalize_svg_images(path):
    tree = ET.parse(path)
    root = tree.getroot()
    ids = {node.get('id'): node for node in root.iter() if node.get('id')}
    masks = set()
    alpha_images = set()
    converted = {}
    placements = 0
    for group in root.iter('{' + SVG + '}g'):
        reference = group.get('mask')
        if reference is None:
            continue
        match = re.fullmatch(r'url\(#([^\)]+)\)', reference)
        if not match:
            raise ValueError('Unsupported SVG mask reference')
        mask_id = match.group(1)
        mask = ids[mask_id]
        uses = mask.findall('.//{' + SVG + '}use')
        if len(uses) != 1 or len(group) != 1:
            raise ValueError('Expected one image and one grayscale soft mask')
        alpha_use = uses[0]
        image_use = group[0]
        if image_use.tag != '{' + SVG + '}use':
            raise ValueError('Expected an image placement')
        if alpha_use.get('transform') != image_use.get('transform'):
            raise ValueError('Color and alpha transforms differ')
        image_id = image_use.get(HREF)[1:]
        alpha_id = alpha_use.get(HREF)[1:]
        if image_id in converted:
            if converted[image_id] != alpha_id:
                raise ValueError('One color image has multiple different masks')
        else:
            image_node = ids[image_id]
            alpha_node = ids[alpha_id]
            def decode(node):
                data = node.get(HREF).split(',', 1)[1]
                return Image.open(io.BytesIO(base64.b64decode(data)))
            color = decode(image_node).convert('RGBA')
            alpha = decode(alpha_node).convert('L')
            if color.size != alpha.size:
                raise ValueError('Color and alpha image sizes differ')
            color.putalpha(alpha)
            output = io.BytesIO()
            color.save(output, format='PNG')
            image_node.set(HREF, 'data:image/png;base64,' +
                           base64.b64encode(output.getvalue()).decode('ascii'))
            converted[image_id] = alpha_id
        group.attrib.pop('mask')
        masks.add(mask_id)
        alpha_images.add(alpha_id)
        placements += 1
    for parent in root.iter():
        for child in list(parent):
            if child.get('id') in masks | alpha_images | {'filter-remove-color', 'filter-color-to-alpha'}:
                parent.remove(child)
    if root.findall('.//{' + SVG + '}mask') or root.findall('.//{' + SVG + '}filter'):
        raise ValueError('Unconverted masks or filters remain')
    tree.write(path, encoding='utf-8', xml_declaration=True)
    return placements


if __name__ == '__main__':
    import sys
    for filename in sys.argv[1:]:
        print(f'{Path(filename).name}: {normalize_svg_images(filename)} transparent image placements normalized')
