# 예제 작업 안내

## 목표
합성 요청의 필수 단계 제출물이 있는지 로컬에서 검사합니다.

## 입력·출력
`fixtures/`만 읽고 `src/contract_check.py`를 사용합니다. 보고는 PASS/FAIL과 누락된 상대 경로입니다.

## 안전 경계
- fixture는 읽기 전용입니다. 실제 사용자 요청·작업 폴더를 사용하지 않습니다.
- 외부 송신, 네트워크, GPU, 자격 증명 접근을 하지 않습니다.
- 정책 메타데이터만으로 파일시스템 격리가 된다고 주장하지 않습니다.

## 자체 확인
저장소 루트에서 `make test`, `make example NAME=workflow-contract-check`을 실행합니다. Python 표준 라이브러리만 사용합니다.
