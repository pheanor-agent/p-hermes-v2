# p-hermes v2

에이전트가 일을 이어가는 구조를 **작업·지식·카탈로그·이미지·영상**으로 배우는 한국어 위키, HTML 강의, 실행 가능한 Python 참고 구현입니다.

[사이트](https://pheanor-agent.github.io/p-hermes-v2/) · [위키 시작](https://pheanor-agent.github.io/p-hermes-v2/wiki/start.html) · [전체 강의](https://pheanor-agent.github.io/p-hermes-v2/learn/) · [API와 명령](https://pheanor-agent.github.io/p-hermes-v2/wiki/reference.html)

Hermes 운영 시스템을 해설하는 자료와, 그 계약을 작게 실험하는 **독립 공개 도구**를 함께 제공합니다. 운영 시스템 전체의 복제본·설치 패키지나 미디어 엔진 어댑터는 아닙니다. 예제는 단일 사용자 로컬 환경을 전제로 합니다.

| 영역 | 이 저장소에서 실행하는 것 |
|---|---|
| 작업 | SQLite revision 비교, 계획 digest에 묶인 승인, 원자적 상태·감사 기록 |
| 지식 | 공개·출처·라이선스 선언 필드 검사, 등록·문자열 검색·퇴역 |
| 카탈로그 | 정확한 버전과 작업·런타임 선택, 메타데이터·템플릿 digest 확인 |
| 이미지 | 선언된 네 입력 슬롯만 바꾸는 템플릿 컴파일 |
| 영상 | 이미지 파일 크기·해시와 컷 구간 검증, 선택적 ffprobe 검사 |

## 실행해 보기

Python 3.11 이상이 필요합니다.

```sh
git clone https://github.com/pheanor-agent/p-hermes-v2.git
cd p-hermes-v2
python -m venv .venv
```

가상 환경 활성화: macOS/Linux는 `source .venv/bin/activate`, Windows PowerShell은 `.venv\Scripts\Activate.ps1`을 사용합니다.

```sh
python -m pip install -e .
p-hermes demo --output demo-output
```

출력에는 작업 DB, 직접 작성한 고정 SVG, 컴파일된 이미지 계획, 5초짜리 타임라인 JSON, 검증 보고서가 있습니다. SVG는 이미지 계획을 렌더링한 결과가 아니며, 데모는 모델 추론이나 영상 인코딩을 수행하지 않습니다. 재실행할 때는 새로운 출력 폴더를 지정하세요.

```sh
p-hermes compile-image examples/image-request.json image-plan.json
p-hermes job --db demo-output/workspace.sqlite3 show studio-demo
p-hermes knowledge --db demo-output/workspace.sqlite3 search lamp
```

명령과 실제 입출력 파일명은 [API 참고](https://pheanor-agent.github.io/p-hermes-v2/wiki/reference.html)와 `p-hermes --help`에서 확인할 수 있습니다. 실제 영상 파일이 있다면 ffprobe를 별도로 설치한 뒤 `p-hermes inspect-video movie.mp4 --duration 5`로 스트림 정보와 길이를 검사합니다. 전체 프레임 디코딩이나 시각 품질 평가는 별도 검증입니다.

## 자료 읽기와 발표

위키 8개 페이지와 강의 7장·26개 슬라이드가 같은 LUMA 램프 사례를 이어 설명합니다. 개념 사례의 영상은 12초이며, 실행 데모의 5초 타임라인과 구분합니다. 강의는 본문을 읽거나 발표 모드로 볼 수 있습니다. 방향키·Page Up/Down으로 이동하면 다음 장으로 이어지고, 발표자 메모를 열 수 있습니다. Esc는 읽기 화면으로 돌아갑니다. JavaScript 없이도 본문과 링크를 읽을 수 있습니다.

## 구조와 검증

```text
src/p_hermes/     공개 Python 참고 구현
examples/        합성 입력 데이터
content/wiki/    위키 원고
content/slides/  강의 원고
site/            스타일·상호작용
tools/           정적 사이트 생성·검사
docs/            GitHub Pages 결과와 이전 미리보기
tests/           계약·실패 경로 검증
```

```sh
python -m unittest discover -s tests -p "test_core.py" -v
python tools/build_site.py
python tools/check_site.py
python -m http.server 8765 --bind 127.0.0.1 --directory docs
```

`http://127.0.0.1:8765/`에서 확인합니다. 새 한글이 추가되면 선택적 글꼴 빌드 도구로 서브셋을 갱신합니다.

```sh
python -m pip install -r requirements-assets.txt
python tools/build_site.py
python tools/subset_font.py
python tools/check_site.py
```

기존 강의 미리보기의 주소는 유지합니다. 최신 학습 경로는 `/wiki/`와 `/learn/`입니다.

## 공개 범위와 권리

신규 코드와 문서에는 MIT 라이선스를 적용하며 글꼴은 별도 SIL OFL 1.1입니다. 자세한 내용은 [LICENSE](LICENSE)와 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)를 참고하세요. 예제에는 합성 데이터만 사용하고 운영 로그·사용자 대화·내부 작업 기록·인증 정보를 배포하지 않습니다.

지식 입력의 `public: true`는 작성자의 공개 선언입니다. 개인정보 자동 탐지나 공개 권한의 증명을 제공하지 않습니다. 사이트 검사는 이 저장소의 알려진 비공개 형식을 찾는 보조 수단이며, 임의 데이터의 안전성을 보증하지 않습니다.
