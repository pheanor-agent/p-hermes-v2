# p-hermes — 공개 학습 자료

p-hermes는 에이전트 시스템을 세 층으로 설명하는 한국어 강의와 참조 위키입니다. 강의는 에이전트, 누구에게나 같은 작업 흐름 궤도, 모든 동작의 바탕인 지식을 전체 그림에서 통합까지 연결합니다. 사이트는 개념과 참조 정보에 집중하고, 원본 구현·테스트·교육용 합성 자료는 [GitHub 저장소](https://github.com/pheanor-agent/p-hermes-v2)에서 확인합니다.

## 공개 사이트

- `docs/` — GitHub Pages 배포 산출물
- `site/index.html` — 홈 원본
- `site/lectures/` — 다섯 강의의 원고
- `site/wiki/` — 계약·용어·작업 흐름·지식 참조 원고
- `site/assets/` — 스타일·글꼴·강의 플레이어

## 저장소 자료

- `reference/` — 파일 handoff 공개 참조 구현
- `tests/` — 참조 구현의 계약 테스트
- `examples/` — 합성 입력을 사용하는 독립 교육 자료
- `content/`, `publication/` — 공개 설명 원고와 범위 메모

저장소 자료는 사이트 페이지에 복제하지 않습니다. 공개 구현은 전체 Hermes 운영 시스템을 설치하거나 복제하지 않으며, 예제의 결과를 실제 운영 결과로 해석해서는 안 됩니다.

## 빌드와 검사

Python 3.11 이상이 필요합니다. 외부 서비스, GPU, API key는 사용하지 않습니다.

```sh
make test
make build
make check
make verify
```

`make build`는 `site/`의 원고를 검증 가능한 후보 디렉터리에 빌드한 뒤 `docs/`에 반영합니다. `make check`는 공개 페이지의 내부 링크·강의 구성·민감정보 패턴을 검사합니다. 알려진 패턴 검사는 공개 적합성 전체를 보증하지 않습니다. 사이트를 로컬에서 확인하려면 빌드 후 `python3 -B -m http.server 8765 --bind 127.0.0.1 --directory docs`를 실행합니다.

## 공개 범위와 권리

`LICENSE`, `PRIVACY.md`, `THIRD_PARTY_NOTICES.md`의 공개·라이선스 조건을 확인하세요. 외부 게시나 원격 Git 변경은 로컬 빌드에 포함되지 않습니다.
