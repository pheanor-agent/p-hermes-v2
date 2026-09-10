# Third-party notices

## Noto Sans KR — course-preview fonts

Copyright 2014–2021 Adobe (http://www.adobe.com/), with Reserved Font Name 'Source'.
Licensed under the SIL Open Font License, Version 1.1, not under a code license.
The complete copyright and license are distributed at
`docs/lectures/course-preview/fonts/OFL.txt`.

The original variable TTF is from Google Fonts. The locally converted WOFF2
preserves the complete character map and glyph set; there is no subsetting,
outline edit or naming change. Upstream revision, exact source URL, file
hashes and conversion versions are recorded in
`docs/lectures/course-preview/fonts/SOURCE.json`.

The page serves the font from this site; no runtime Google Fonts service is
used. No endorsement by the font authors is implied.

New explanatory diagrams in this preview are original educational vectors,
not actual model-generated images or evidence of media production. These
notices do not change the licensing of any previously published files.

## Hermes KR — current wiki, blog and HTML lectures

`docs/assets/HermesKR.woff2` is a character subset of the original Noto Sans KR
font above, renamed Hermes KR. It remains under the SIL Open Font License 1.1.
The original font and full license remain distributed. Source/output hashes,
character coverage, and tool version are in `docs/assets/font-manifest.json`;
optional build dependencies are pinned in `requirements-assets.txt`.

The current diagrams and explanatory prose are newly authored. References
listed in the wiki and course inform the explanations and design choices;
third-party illustrations and article text were not copied into this site.

## reveal.js 6.0.1

The HTML lecture player vendors reveal.js under the MIT license. Its complete
license, pinned upstream source, version and tarball checksum are in
`site/slides/vendor/reveal/`. The deployed copies are under
`docs/slides/assets/vendor/reveal/`. No CDN is required during a lecture.

## Educational image and video assets

The LUMA lamp is a fictional educational product. Four raster photos and the
design art board were prepared with OpenAI's built-in image generation tool.
They are supplied under this repository's MIT terms to the extent rights apply.
No real brand endorsement is implied. Prompts and reference relationships are
recorded in `content/slides/media-provenance.json` and
`design/art-board-prompts.json`.

The two 12-second MP4s are separately encoded still-shot edits of the same three
source images. They contain no generated motion or audio. The 2-second test
pattern is a separate FFmpeg fixture. Encoding measurements and hashes are in
`content/slides/video-evidence.json`. Boundary images are extracted from the
actual 12-second edit at 3.96 and 4.00 seconds.

The four WebM recordings show real public-code executions on synthetic data.
The viewer displays selected return fields immediately after each call. Receipts
are in `content/slides/recording-*.json`. These recordings do not contain private
operational logs, user conversations or credentials.
