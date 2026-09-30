# p-hermes — 공개 학습 자료

p-hermes는 지휘 에이전트와 작업 에이전트의 역할, 단계형 작업 흐름, 지식 참조, 이미지 파이프라인, 통합 경계를 한국어 강의·위키·오프라인 예제로 설명합니다. 공개 사이트는 `docs/`에서 제공하며 디자인 원고와 발표 자산은 `site/`에 보존됩니다.

## 시작하기

Python 3.11 이상이 필요합니다. 외부 서비스, GPU, API key 없이 예제를 실행할 수 있습니다.

```sh
make test
make build
make check
```

사이트를 로컬에서 확인하려면:

```sh
python3 -B -m http.server 8765 --bind 127.0.0.1 --directory docs
```

브라우저에서 `http://127.0.0.1:8765/`를 엽니다. 공개 홈의 단일 정본은 `site/index.html`이며 빌드는 이를 `docs/index.html`에 바이트 그대로 복사합니다.

## 자료 탐색

- `docs/lectures/` — 여섯 강의와 강의 목차
- `docs/wiki/` — 8개 참조 페이지와 검색 목차
- `docs/examples/` — 네 오프라인 예제 가이드
- `docs/code/` — 소스 열람 페이지
- `docs/downloads/` — 원본 코드·fixture·테스트와 `examples.zip`

네 예제는 portable-worker(공개 reference + 계약 테스트), image-pipeline, knowledge-context-check, integration-check입니다. 예제 입력은 합성 fixture이며 이 저장소는 전체 Hermes 운영 시스템이나 미디어 엔진을 설치·복제하지 않습니다.

## 정본과 빌드

```text
content/       공개 설명 원고
site/          디자이너 원본 HTML/CSS/JS/SVG와 정적 자산
examples/      네 개의 독립 offline 예제 및 fixture
reference/     portable-worker 공개 참조 구현
tests/         portable-worker 계약 테스트
publication/   공개 범위 메모
tools/         deckify, wikify, build_site, check_site
docs/          재현 가능한 공개 사이트 산출물
```

`tools/build_site.py`는 root-level source를 읽어 검증 후 `docs/`를 반복 생성합니다. `tools/check_site.py`는 6강 52장, 실제 질문 레일, 공개 HTML의 local href/src/fragment(같은 페이지 fragment 포함), 공개 배포 트리의 텍스트 자산·전체 경로 및 ZIP member 경로/텍스트 내용에 알려진 private path/credential 패턴이 있는지 검사합니다. 바이너리 자산의 내용은 텍스트로 디코딩하지 않습니다. 검사는 알려진 패턴을 찾는 보조 통제이며 공개 적합성을 보증하지 않습니다.

```sh
make test       # 네 오프라인 예제의 계약·성공·실패 테스트
make build      # docs/ 재생성
make check      # 사이트 검사
make verify     # test + build + check + git diff --check
```

예제별 테스트는 `make example NAME=portable-worker|image-pipeline|knowledge-context-check|integration-check`로 실행합니다. 문서와 예제는 합성 입력만 사용합니다. 운영 로그·사용자 대화·인증정보를 공개 입력으로 추가하지 않습니다.

## 공개 범위와 권리

`LICENSE`, `PRIVACY.md`, `THIRD_PARTY_NOTICES.md`의 공개·라이선스 조건을 확인하세요. 검사는 알려진 private path/credential 패턴을 찾는 보조 통제이며 임의 입력의 공개 적합성을 보증하지 않습니다. 외부 게시나 원격 Git 변경은 이 로컬 빌드에 포함되지 않습니다.
