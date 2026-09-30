# 작업 흐름 계약 점검 예제

## 전체 흐름 속 위치

지휘 에이전트는 합성 요청과 조건을 제시하고, 작업 에이전트는 제출물·단계 계약을 읽어 PASS/FAIL과 근거 경로를 돌려줍니다.

```text
합성 요청 + 계약 fixture → 검사기 → PASS/FAIL + 근거 경로
```

로컬 실행만 사용합니다. 한 줄 명령: `make example NAME=workflow-contract-check`.

`make test`는 정상 fixture가 통과하고 필수 제출물 누락 fixture가 실패하는지 확인합니다. Python 표준 라이브러리만 필요하며 GPU·외부 서비스·실제 작업 기록을 사용하지 않습니다. 먼저 저장소를 복제하고, 이미 사용 중인 코딩 에이전트에서 폴더를 연 뒤 `PROMPT.md`의 과제를 수행하세요.
