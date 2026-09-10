# Six-course HTML lecture validation

The delivery target is [GitHub Pages](https://pheanor-agent.github.io/p-hermes-v2/lectures/). The reading series is named **Blog**; the six separate presentation decks use fixed 16:9 slides. PDF distribution is outside the requested scope.

| Course | Slides | Planned teaching / questions |
|---|---:|---:|
| Overview | 32 | 50 / 10 minutes |
| Tasks | 32 | 65 / 10 minutes |
| Knowledge | 33 | 65 / 10 minutes |
| Catalog | 32 | 65 / 10 minutes |
| Image | 31 | 65 / 10 minutes |
| Video | 32 | 65 / 10 minutes |

The 192 slides cover all 72 agreed scenes and 38 course-level keyword definitions. Each scene has authored explanation, an audience question and answer, presentation cues, sources and a transition. Time includes observation and application activities. The planned 435 minutes is not a measured delivery time for a human lecturer.

## Content and evidence

- [Asset map](../content/slides/asset-map.json): fulfillment of all A01–A13 visual and media roles.
- [Executed evidence](../content/slides/evidence.json): CAS, approval invalidation, transaction rollback, recovery, substring search and retirement, catalog rejection cases, binding and changed image references. The checker reruns the public functions and compares the result.
- [Image provenance](../content/slides/media-provenance.json): four generated educational photos, prompts, references and hashes. These are separate from the public reference runtime.
- [Video evidence](../content/slides/video-evidence.json): the same three source images in two actual 12-second encodings, 4+4+4 and 2+6+4 seconds. A separate real 2-second H.264 test file is inspected with the public ffprobe wrapper. The 5-second public timeline JSON remains a separate artifact.
- Four recordings display selected return fields immediately after real public function calls. Their receipts are stored in `content/slides/recording-*.json`. No model generation is implied by the recordings.
- [Web media descriptions and execution transcripts](../docs/lectures/media.html) provide a reading alternative to the silent videos.

## Screen and interaction review

All 192 slides were rendered at 1280×720 and 1920×1080. Every initial state and final fragment state was captured. Automated checks inspect overflow, overlap with the footer, missing images, font loading and hidden presenter notes. The [screen report](lecture-screen-review.json) merges the complete sweep with targeted checks after corrections. [Six representative screenshots](lecture-screens/) preserve actual rendered output.

Visual inspection covered all course contact sheets and full-size selections. Corrections included the CAS question position, hash comparison spacing, preserving the entire boundary frames, a wrapped catalog label, code labels and layout, and making the four real recordings fill the slide. The tasks sequence now proceeds from comparison code to real recording to the retry decision, with specific presenter notes for each screen.

Website review covers the home page, course directory, topic outline, guide, blog and media reading page at desktop and mobile widths. Browser checks exercise scene links, fragment navigation, full screen, video play/pause, a separate speaker window and reduced motion. A network-disabled browser also opens the same checked-in `docs` files and plays their media and speaker view.

The native slide controls and all runtime assets are served locally with the site; no external presentation service is required. Browser playback is tested both at the start and through the actual end of each authored video.

## Timing and review limits

The ten-minute T04–T05 excerpt is checked as a timed **visual cue rehearsal** using the real recording, question hold and sequential reveals. Its event log records wall-clock time and slide state. It does not measure spoken delivery or audience reactions. A human lecturer should adjust the planned lesson times after teaching practice with their intended audience.

Automated checks and author review do not establish learner engagement, retention or acceptance. Safari, physical projectors and screen-reader speech were not tested. The contract tests previously passed 15 cases on Windows with the unprivileged symlink test skipped; the Linux CI passed all 16 tests.

## Release evidence

Completed local results: [browser review](lecture-browser-review.json), [full media playback](lecture-media-review.json) and [600-second visual cue rehearsal](lecture-cue-review.json). All three passed. [GitHub deployment verification](lecture-deployment.json) records successful CI and Pages runs, and exact byte comparisons for 55 public pages and assets against content commit `6301fa72710ebcdfa7bc9fb4f97c202d4bf5a59e`. [Public browser review](lecture-public-browser-review.json) passed desktop/mobile navigation, scene links, fragments, full screen, seven media controls, speaker view and reduced motion at the live URL.
