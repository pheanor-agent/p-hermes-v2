# 실행 예제

이 디렉터리는 공개 요청과 실행 예제를 보관합니다. 예시는 사용 흐름을 확인하기 위한 자료이며, 공개 사이트의 기술 명세 본문을 복제하지 않습니다.

Python 3.11 이상에서 저장소 루트에서 설치합니다. 실행 의존성은 Python 표준 라이브러리뿐입니다.

```sh
python -m pip install -e .
p-hermes demo --output demo-output
p-hermes compile-image examples/image-request.json image-plan.json
p-hermes verify-artifact demo-output/artifact.json --root demo-output
python -m unittest discover -s tests -p 'test_core*.py' -v
```

`demo-output`은 새 경로여야 합니다. 실습은 SQLite 작업/지식, 감사 이력,
이미지 입력을 변환한 실행계획, 직접 작성한 SVG 스토리보드, 파일 해시와
5초 타임라인을 저장합니다. `report.json`에서 실행한 부분을 확인할 수 있습니다.
SVG는 코드로 그린 구성 예시이며 이미지 모델의 생성 결과가 아닙니다.

`compile-image`는 JSON의 catalog와 pin을 대조한 뒤 template의 명시된
입력 위치에 spec을 연결합니다. 네 필수 필드를 모두 연결하고 입력을
변경하지 않으며, 존재하지 않는 입력 위치와 중복 연결은 거부합니다.
카탈로그의 `template_digest`는 변환 전 템플릿 전체를 고정합니다. 바인딩
위치 외의 노드만 달라져도 다른 릴리스로 검토하기 전에는 컴파일을 거부합니다.
이 예제 그래프는 바인딩 계약 설명용입니다. 특정 이미지 엔진에 바로
제출할 수 있는 워크플로우라고 주장하지 않습니다.

실제 영상 파일이 있으면 설치된 ffprobe로 컨테이너를 검사할 수 있습니다.

```sh
p-hermes inspect-video your-video.mp4 --duration 5
```

영상 스트림, 크기, 실제 길이와 파일 해시를 검사합니다. 기대 길이는 ±0.1초를
허용합니다. ffprobe는 따로 설치해야 합니다. 영상 생성이나 업로드는 하지 않으며
인물 일관성, 미감, 사실성은 이 검사로 판정할 수 없습니다.

`compile-timeline INPUT --root DIR --output FILE`의 INPUT은 `shots`와
`artifacts`를 가진 JSON입니다. shot은 `id`, `duration_seconds`, `image_ref`,
`purpose`를 가지며, artifact 구조는 실습의 `artifact.json`과 같습니다.
참조 파일의 바이트를 다시 검사한 후 각 샷의 시작·끝·총 길이를 계산합니다.
결과는 편집 계획이며 영상 파일은 아닙니다.

데모의 영속 기록을 별도로 조회하거나 지식을 검색할 수 있습니다.

```sh
p-hermes job --db demo-output/workspace.sqlite3 show studio-demo
p-hermes knowledge --db demo-output/workspace.sqlite3 search lamp
p-hermes knowledge --db demo-output/workspace.sqlite3 retire composition-note
```

새 작업은 `job --db FILE create ID PLAN.json`, 새 지식은
`knowledge --db FILE register INPUT.json`으로 등록합니다. PLAN은 비어 있지
않은 `purpose`를 포함한 객체입니다. 지식 INPUT은 `id`, `title`, `body`,
`source_ref`, `license_ref`, `public: true`를 포함합니다. `job act`는 ID,
현재 revision, action을 필수로 받습니다. `approve`에는 `--approved-digest`,
`revise`에는 `--plan`, 완료/실패/결과불명에는 `--evidence`를 지정합니다.
`--db`가 새 파일이면 테이블을 만듭니다. 부모 디렉터리는 미리 존재해야 합니다.
승인 기록은 로컬 호출자가 제공한 결정이며 사용자를 인증하는 서비스는 아닙니다.

실행 시 선택한 경로에 로컬 파일이 작성됩니다. 원격 서비스 호출·자동 Git
커밋·개인 작업 디렉터리 탐색은 없습니다. public 선언은 작성자의 책임이며
자유 서술문에 민감한 내용이 없는지 자동으로 증명하지 않습니다.

## 강의의 실행 근거

`python tools/build_lecture_evidence.py`는 합성 입력으로 충돌·승인 변경·롤백·검색·퇴역·고정·바인딩과 참조 변경을 실제 실행합니다. 결과는 `content/slides/evidence.json`에 기록합니다. GitHub Pages의 [강의](https://pheanor-agent.github.io/p-hermes-v2/lectures/)에서 같은 값을 도해와 녹화로 확인할 수 있습니다. `tools/lecture_worker.py`는 각 녹화 단계의 실제 함수를 실행합니다.

12초 편집 MP4와 2초 규격 검사 파일은 `site/slides/media/`에 있습니다. 실제 검사 명령은 `p-hermes inspect-video site/slides/media/probe-2s.mp4 --duration 2`입니다. ffprobe가 필요하며, 이 파일은 공개 5초 시간선 JSON과 별도입니다.
