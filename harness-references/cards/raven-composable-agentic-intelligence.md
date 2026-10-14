# Raven: The Harness of Harnesses for Composable Agentic Intelligence

- 원문: https://arxiv.org/abs/2609.33439
- 출처 시점: arXiv page v1; retrieved 2026-10-14. 사용자 제공 링크 확인 2026-10-02 (KST).
- 주제: overview · orchestration/workflow · case/implementation
- 상태: 사용자 제공 논문 링크; current knowledge reference 등록·활용 여부 확인되지 않음.
- 권리: arXiv page displays CC BY 4.0; no source text copied.
- 정리 근거: 원문 일부 확인

## 자체 요약

arXiv에 등록된 “harness of harnesses” composable agentic intelligence 연구다. 이 카드에서는 초록·서지 페이지 수준만 확인했으며, 구현·평가·성능 주장에 대한 전문 검토는 수행하지 않았습니다.

## 상세 정리

### 핵심 주장
1. 에이전트가 긴 작업과 여러 영역을 오가게 되면서, 하네스를 사람이 손으로 설계하는 방식은 확장되기 어렵다고 주장한다.
2. 질문을 "더 강한 하네스를 어떻게 만들까"에서 "하네스를 자동으로 만들고, 경험으로 개선하고, 여러 영역에 걸쳐 조합하는 방법"으로 옮긴다.
3. 모델과 하네스의 실행 가능한 짝을 조합 가능한 단위로 본다.

### 구조와 패턴
- 호스트 에이전트가 목표를 나누고, 하위 작업을 전문 에이전트에 맞추고, 실행 의존 관계를 조정하고, 결과를 합친다.
- 호스트 아카이브와 경험 저장소가 여러 작업에 걸친 경험을 보존한다.
- 스킬 단조(Skill Forge)는 쌓인 경험을 재사용 가능한 절차로 바꾼다고 설명된다.
- 제한된 공유 자원 예산 아래에서 조합이 신뢰할 수 있는 작업 범위를 넓힌다는 이론적 충분 조건을 제시한다.

### 적용 방법
- Hermes의 JOB 조율, 경험 저장, 스킬 생성 구조와 대응시켜 볼 수 있다. 특히 경험을 절차로 바꾸는 단계가 Hermes의 스킬 갱신과 가깝다.
- 여러 전문 에이전트에 나눠 맡길 때는 자원 예산과 의존 관계를 함께 정해야 한다는 점이 실무 참고점이다.

### 근거와 한계
- 이 정리는 초록만 확인했다. 본문의 실험 과제, 기준선, 이론 조건의 세부는 확인하지 못했다.
- "크게 앞선다"는 주장은 저자들의 비교이며, 기준 시스템 선택에 따라 달라질 수 있다.
- 오픈소스 생태계를 표방하지만, 이 정리에서 구현과 재현은 확인하지 않았다.

### 연결
- [Meta-harness](meta-harness.md) — 하네스를 자동 탐색하는 또 다른 연구
- [JAZ harness as a language](jaz-harness-language.md) — 최소 하네스라는 반대 방향
- [Multi-agent orchestration patterns](multi-agent-orchestration-patterns.md) — 감독과 워커를 나누는 실무 구성

## Hermes 관련성

하네스들을 조립하는 상위 계층이라는 주제로 독립 탐색 가치가 있어 목록에 포함했다. 전문 검토 전에는 개념 및 결과를 사실로 일반화하지 않습니다.
