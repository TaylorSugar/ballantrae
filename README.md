# Ballantrae.ca: Real Estate Guide to Ballantrae Golf and Country Club

Static site by the Sugar Team. Preview (deed.page): https://ballantrae-preview.deed.page/

- `site/` is the built output (plain HTML, CSS, JS, WebP). Deploy it as-is. For Cloudflare Pages: no build command, output directory `site`.
- Rebuild from the data: `./rebuild.sh` (runs `extract_sales.py` on `data/source/*.xlsx`, then `build.py`).
- Page copy is in `content.py`; `data/for_sale.json` is the dated For Sale Now snapshot.
- Pages are `noindex` until launch.
- Stock golf photos are from Pexels (free licence) and are credited in the site footer.

## Private data kept out of this public repo
The official sales workbook (`Official Ballantrae Golf and Country Sales Data.xlsx`) and the file extracted from it, `data/sales.json`, are **not** in this repository. `sales.json` holds MLS numbers, assessment values and condition notes that the public site does not show. Raw Dropbox sources (PDFs, PSDs, original scans) are also excluded.
- The built site in `site/` already contains every public number, so it can be deployed as-is.
- To rebuild, the Sugar Team places the workbook at `data/source/` locally and runs `./rebuild.sh`. `data/for_sale.json` (the dated For Sale Now snapshot) is included.
