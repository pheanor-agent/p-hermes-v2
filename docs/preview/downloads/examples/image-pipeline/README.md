# image-pipeline · 합성 파이프라인 실습

## 무엇을 확인하나요?
주제·행동 등 장면 의도를 읽고, 이름이 지정된 합성 카탈로그를 선택해 프롬프트로 구성한 뒤, 네트워크와 GPU 없이 fake runtime 결과를 검증합니다. 실제 이미지 파일은 만들지 않습니다.

## 빠른 시작
저장소 루트에서 실행합니다.

```sh
make example NAME=image-pipeline
```

예제 디렉터리에서 직접 실행하려면 표준 라이브러리와 `src/`를 사용합니다.

```sh
cd examples/image-pipeline
PYTHONPATH=src python3 -m image_pipeline_demo
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

## 기대 결과
JSON 응답의 `status`는 `simulated`, `request_id`는 fixture의 식별자이며, `output_marker`는 합성 표식입니다. `prompt_sha256`은 프롬프트를 SHA-256으로 계산한 값입니다. 이 결과는 실제 이미지 생성·품질 평가·게시를 뜻하지 않습니다.

## 파일 구조
- `src/image_pipeline_demo/`: 공개 인터페이스·fake runtime
- `fixtures/`: 공개용 합성 카탈로그, 요청, 기대 메타데이터
- `tests/`: 프롬프트·선택·결과 계약 테스트
- `PROMPT.md`: 에이전트에게 맡길 안전한 과제

외부 패키지 설치, 네트워크, GPU, 모델 가중치가 필요하지 않습니다. 오류를 숨기거나 입력을 바꾸지 않습니다.
