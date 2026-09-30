# 에이전트 과제: 요청 근거 확인

이 예제의 목적은 작업 에이전트가 합성 후보 자료의 출처·날짜·검토 상태를 나눠 보고하는 것입니다.

먼저 저장소 루트 `AGENTS.md`, 이 예제의 `README.md`, 이 프롬프트, `fixtures/`, `src/knowledge_check.py`, `tests/`를 읽습니다.

1. 표준 라이브러리만 사용합니다. GPU·외부 서비스·네트워크·실제 홈 경로·비밀값은 사용하지 않습니다.
2. 후보가 있다는 이유만으로 내용을 검증된 사실로 표시하지 않습니다.
3. `source`, `updated_at`, `validation_status`, `review_status`를 각각 보존합니다. 모르면 `unknown`입니다.
4. 사람 검토 전에는 `pending`으로 유지하고 자동으로 수용·승격하지 않습니다.
5. 일치 후보가 없으면 `no_candidate`를 반환합니다. 이는 fixture 범위의 결과입니다.
6. 테스트를 추가한 뒤 다음을 실행합니다.

```bash
make example NAME=knowledge-context-check
make test
```

완료 조건: 테스트 통과, 미확인 값 추정 없음, 자동 승격 없음, fixtures 외 파일 접근 없음, 제한 사항 요약.
