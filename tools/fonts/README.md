# Fonts

Build input for `../build-banner.py`. The banner's wordmark and tagline are outlined
before they are written to SVG — GitHub serves README images through a proxy that has
never seen the site's webfonts, so a `<text>` element would fall back to Arial and the
banner would stop being the brand.

| File | Family | Cut |
|---|---|---|
| `BricolageGrotesque-SemiBold-var.ttf` | Bricolage Grotesque | wght pinned at 600, `opsz` axis 12–96 |
| `Inter-Medium-var.ttf` | Inter | wght pinned at 500, `opsz` axis 14–32 |

Both are the **latin** subsets served by `fonts.googleapis.com`, decompressed from the
woff2 the browser receives. They are variable, because optical size is not optional here:
Bricolage Grotesque at `opsz` 12 is a text face (an `o` is 607 units wide) and at `opsz` 96
it is the display face the hero headline is set in (562 units). Instancing the axis at
render time is what makes a 200 px wordmark match the landing page instead of merely
resembling it.

Re-fetch (only if the families are updated upstream):

```sh
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36'
curl -s -H "User-Agent: $UA" \
  'https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600&display=swap'
# take the URL from the /* latin */ block, download the .woff2, then:
python -c "from fontTools.ttLib import TTFont; f = TTFont('x.woff2'); f.flavor = None; f.save('x.ttf')"
```

Both families are licensed under the SIL Open Font License 1.1 — `OFL-BricolageGrotesque.txt`
and `OFL-Inter.txt`. Redistribution is permitted; the fonts are used here, not modified
beyond decompression and the weight axis being pinned by Google's own subsetter.
