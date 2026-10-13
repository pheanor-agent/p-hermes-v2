# Loop Engineering (Addy Osmani)

- 원문: https://addyo.substack.com/p/loop-engineering
- 출처 시점: 내부 knowledge reference에 2026-06-11 기록; 직접 재수집·전문 최신성 미확인.
- 주제: orchestration/workflow · skills/tools · context/memory · evaluation
- 상태: `knowledge/references/addyo-loop-engineering.md` 등록; reference는 loop design에 관한 관점이며, 별도 운영 실험/채택 증거 아님.
- 권리: 원문 조건 확인 안 됨; 내부 reference의 텍스트를 복사하지 않고 공개본은 링크와 자체 요약만.

## 자체 요약

에이전트를 사람이 매번 prompting하기보다 목표를 반복 실행하는 loop를 설계하는 관점으로 자동화·worktree·skills·connectors·subagents·memory를 논한다. unattended loop에는 검증 필요, 토큰 비용, 인간 검토 용량과 이해도 저하 위험이 남는다고 경고한다.

## Hermes 관련성

반복 실행과 state file의 역할 및 병렬 격리의 trade-off를 비교할 수 있다. 인용된 사례와 수치는 외부 저자 관찰이며 Hermes에서의 효과를 증명하지 않습니다.
