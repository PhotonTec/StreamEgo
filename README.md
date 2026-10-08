# StreamEgo

Academic project page for **StreamEgo: Streaming Exocentric-to-Egocentric Video Generation**, following the [VGGT](https://vgg-t.github.io/) project-page template.

The page starts with three continuous generation examples, followed by the paper teaser, abstract, Teacher / Student method diagrams, an inference pipeline with timing details, and all seven qualitative comparisons. Authors and numbered affiliations appear above the figures. The arXiv button is marked **coming soon** until the manuscript URL is available.

## Local preview

```sh
python3 serve.py
```

Open http://127.0.0.1:8765. The preview server supports video seeking.

## Publication

GitHub Pages serves `dist/`. The workflow in `.github/workflows/pages.yml` publishes each push to `main`. No build or package installation is needed.

To add the arXiv link later, replace the disabled `#arxiv-button` in `dist/index.html` with a link to the published manuscript, retaining its existing button classes.

## Figures

The webpage displays **SVG vectors converted from the supplied PDFs**, preserving the vector paths and glyphs. Embedded photographs retain the source PDF's raster content. Each figure opens its PDF for full-size viewing. The teaser's six H/S/U math labels were exported by WPS as small raster images; these are replaced in both formats with calligraphic vector outlines derived from KaTeX Caligraphic Regular, keeping the original positions and sizes. Displaying them requires no installed math fonts. Embedded image soft masks are merged losslessly into native PNG alpha channels to avoid SVG filter and mask artifacts in browsers; the vector paths remain intact.

To regenerate the figures:

```sh
python3 prepare_vectors.py /path/to/paper/figures
```

This requires `pdf2svg`, PyMuPDF and Pillow (`pip install pymupdf Pillow`). It repairs the teaser math labels and exports the teaser, teacher, student, and inference timeline figures. The VAE decoding device in the timing table is **H100**, corrected by the authors.

## Video examples

`prepare_gallery.py` assembles the actual videos embedded in the supplied presentation, including input, StreamEgo, and ground truth. Comparison examples also include EgoX, Vista4D, and Wan-VACE. Labels remain visible in fullscreen. The complete long examples last 30, 30, and 10 seconds.

Some short baseline exports encode a five-second sample as 49 frames at 30 FPS. Their temporal endpoints are aligned to the five-second comparison sample by adjusting playback timestamps and repeating frames where required. No new motion is synthesized. These are qualitative demonstrations, not wall-clock throughput benchmarks.

The public repository includes only the website, referenced assets, and preparation helpers. Presentation source files, manuscript source archives, obsolete generated downloads, and local verification outputs are excluded.

## Template attribution

The page layout is adapted from [VGGT](https://vgg-t.github.io/) and [Nerfies](https://nerfies.github.io/), with attribution in the footer. The upstream template uses CC BY-SA 4.0; Bulma uses the MIT license. Google Sans and Noto Sans are bundled locally to avoid external font requests.
