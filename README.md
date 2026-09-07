# p-hermes v2

에이전트 시스템을 작업·지식·카탈로그·영상·이미지로 배우는 문서 및 강의 **로컬 프로토타입**입니다. 전체 시스템의 설치 패키지나 공개 배포본이 아닙니다.

- [문서 시작](docs/index.md)
- [전체 구조](docs/overview.md)
- [HTML 강의](docs/lectures/index.html)

## 로컬 열기
Python 3에서 `python3 -m http.server 8765 --bind 127.0.0.1 --directory docs` 실행 후 `http://127.0.0.1:8765/lectures/`를 여세요. 종료는 Ctrl+C입니다. 단순 서버에서 Markdown은 원문으로 제공됩니다. 정식 문서 렌더링·GitHub Pages는 후속 단계입니다.

## 검증
`python3 tests/check_prototype.py`와 `node --check docs/lectures/assets/slides.js`를 실행합니다. 정적 검사 성공은 브라우저 검수나 실제 미디어 생성 성공을 뜻하지 않습니다.

## 범위
자체 작성 도식과 합성 데이터만 포함합니다. 운영 코드·모델·개인 자료는 포함하지 않습니다. 문서에 관측/제안/실행 입증을 구분합니다. 공개 라이선스 기본안은 신규 자체 코드 MIT이며, 최종 권리 검토와 라이선스 파일 확정 전 재배포 완료본으로 취급하지 않습니다.
