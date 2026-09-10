# Release validation

Current six-course HTML release: [lecture validation](lecture-validation.md) and [release checklist](lecture-release-checklist.md).

## Initial release archive

This record covers the initial release before its reading material was
reclassified as a seven-part blog. The six-course replacement is covered by the current record above.
The initial release contained 8 wiki pages, 7 chapters and 26 lecture sections.

Validated locally:

- 16 contract tests: Linux16 passed; Windows15 passed and1 skipped because unprivileged symlink creation was unavailable.
- 23 executable documentation examples passed. Explanatory snippets and optional ffprobe commands were tracked separately; a synthetic H.264 file was inspected with ffprobe on Linux.
- 17 current HTML pages,424 local links and anchors checked.
- All26 slides traversed in a Chromium-based browser; chapter transitions, previous navigation, notes and Escape checked.
- 390px mobile and640px reflow inspected; text remained available with JavaScript blocked.
- Reviewed public files scanned for known private paths, internal identifiers and credential patterns. See [PRIVACY.md](../PRIVACY.md) for the scope of this check.
- The self-hosted font subset covers541 Korean characters. File hashes and reproducible build inputs are recorded in the font manifest.

Browser zoom shortcuts had no effect in the review environment; this release does not claim a successful200% zoom test. Print rules were reviewed statically; native print preview, Safari, screen-reader speech and physical mobile devices were not tested.

These checks establish observed behavior and review coverage. They do not establish perceptual media quality or learner acceptance. The demo authors a fixed SVG and a timeline JSON; it does not generate model images or encode a video.
