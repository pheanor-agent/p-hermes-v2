# p-hermes 강의 개념 일러스트 생성 기록

판정: 완료 — ChatGPT 이미지 6/6장 생성. 모두 PNG 원본 및 WebP 배포본, 6장 대조 시트 작성.
사용: A — ChatGPT 이미지 생성(CDP), 2026-09-29. 한 번에 한 장씩 요청. C(SVG 직접 제작)는 사용하지 않았고 게시·강의 편집도 하지 않음.
목표 캔버스: 1600×900, 16:9. PNG는 규격 크기로 저장, WebP는 약 55–138KB.

## REVIEW
- 이 기록은 강의 일러스트 여섯 장의 생성 프롬프트와 공개 가능한 결과 설명만 담습니다.
- 동일 화풍이 중요하므로 6장 contact sheet를 확인하고, 다른 컷보다 평면적으로 보이던 forgetting만 허용된 1회 재생성으로 세트의 둥근 음영 3D-vector 스타일에 맞췄습니다.
- 시각 확인상 읽을 수 있는 글자·숫자·로고는 발견되지 않았습니다. 일부 도식 아이콘/장식 기호는 그림 요소로 쓰였습니다.

## LESSONS APPLIED
- 생성 화면의 연결 여부와 이미지 생성 완료 여부를 따로 확인하고, 실제 파일을 다시 열어 점검했습니다.
- 브라우저의 동적 선택자와 버튼 상태를 확인하며, 시간 초과를 성공으로 추정하지 않았습니다.

## KNOWLEDGE SEARCH
- 검색어: ChatGPT, CDP, 이미지 생성.
- 이미지 생성 도구 사용과 브라우저 확인 절차를 설명하는 관련 교훈 원문을 확인했습니다.
- 요청이 이미지 생성이므로 외부 참조·프로젝트 지식 계층은 생략했습니다.

## 장별 프롬프트와 결과

### forgetting — 완료 (A, 1회 재생성)
최종 프롬프트: `Create one 16:9 landscape illustration in the same polished, rounded, softly shaded 3D-vector lecture-art style as a friendly robot-agent series. Deep navy background, mint and amber accents, warm rim lighting, expressive small white-and-navy robot with mint face and tool details. Concept: forgetting — a trail of blank empty speech bubbles loses its connecting segments and dissolves into small abstract fragments; the robot looks puzzled and searches for the missing context. Clean clear silhouette, no writing, no letters, no numbers, no punctuation, no logos, no watermark.`
시각 확인: 로봇이 돋보기로 분절되어 사라지는 빈 말풍선 흔적을 살피는 장면. 글자·숫자·로고 없음. 최종 파일 `forgetting.png`, `forgetting.webp`; 생성 원본 `forgetting-regenerated.png`.

### handoff — 완료
프롬프트: `Create exactly one single 16:9 landscape flat-vector illustration, lecture-ready. Deep navy background, mint and amber accents. Two cute friendly robot agents: commander holding a baton and clipboard inserts a blank sealed envelope into an inbox mailbox; worker robot with a tool belt and laptop takes it, works at laptop, then puts a second blank sealed envelope into a separate outbox mailbox. Clear sequential left-to-right flow with arrows only as simple shapes, no text/letters/numbers/logos/watermark and no symbols printed on objects. clean consistent vector style.`
시각 확인: 지휘 로봇, 작업 로봇, 요청·결과 봉투가 서로 다른 우편함으로 전달되는 흐름. 읽을 수 있는 표기 없음. 최종 파일 `handoff.png`, `handoff.webp`; 원본 `handoff-source.png`.

### verify — 완료
프롬프트: `Create exactly one 16:9 landscape flat-vector illustration for a technical lecture. Deep navy background, mint and amber accents. A friendly commander robot with baton and clipboard compares a report (blank paper with plain round ink stamp mark only, no writing) against a real open box of completed items using a magnifying glass. Make report and physical result visibly distinct and under inspection. Polished simple vector composition, no text, letters, numbers, logos or watermark.`
시각 확인: 로봇이 돋보기로 빈 보고서와 실제 상자 속 결과물을 대조. 글자·숫자·로고 없음. 최종 파일 `verify.png`, `verify.webp`; 원본 `verify-source.png`.

### workflow — 완료
프롬프트: `Create exactly one 16:9 landscape flat-vector illustration, deep navy background with mint and amber accents, same friendly robot-agent style. A small task card rides on a rail-like track and passes four distinct stations represented only by icons: planning (compass/blueprint), approval (raised hand/check seal), execution (gear/tool), verification (magnifying glass/check). The track clearly flows left to right; no station words. Clean lecture-ready infographic illustration with no text, letters, numbers, logos or watermark.`
시각 확인: 작업 카드가 네 아이콘 역을 통과하는 흐름. 역 이름 텍스트·숫자·로고 없음. 최종 파일 `workflow.png`, `workflow.webp`; 원본 `workflow-source.png`.

### knowledge — 완료
프롬프트: `Create exactly one 16:9 landscape flat-vector illustration for a technical lecture, deep navy background, mint and amber accents, consistent friendly robot visual style. Show a clear left-to-right chain of layers: source books on a shelf, index cards in a small card cabinet, a magnifying glass searching those cards, then a friendly robot with a glowing lightbulb above its head. Connect the layers with subtle arrows or flow lines. No text, letters, numbers, logos or watermark. Clean polished composition.`
시각 확인: 서가 → 색인 카드함 → 검색 돋보기 → 전구가 켜진 로봇의 레이어 흐름. 읽을 수 있는 글자·숫자·로고 없음. 최종 파일 `knowledge.png`, `knowledge.webp`; 원본 `knowledge-source.png`.

### image-pipeline — 완료
프롬프트: `Create exactly one 16:9 landscape flat-vector illustration for a technical lecture, deep navy background with mint and amber accents, consistent friendly robot-agent style. Show a left-to-right image pipeline: a catalog drawer with several blank style cards, one card selected; a long prompt scroll being carefully refined by a hand/tool; a canvas receiving a newly created illustration; and a final quality inspection with magnifying glass and check mark. Keep every card and paper completely blank, no text, letters, numbers, logos or watermark. Polished simple clear composition.`
시각 확인: 스타일 카드 선택 → 프롬프트 정리 → 캔버스 생성 → 돋보기 검수 단계. 읽을 수 있는 글자·숫자·로고 없음. 최종 파일 `image-pipeline.png`, `image-pipeline.webp`; 원본 `image-pipeline-source.png`.

## 최종 검증
- 여섯 PNG/WebP 쌍 모두 실제 파일 존재, 1600×900 규격 확인.
- WebP 크기: forgetting 65,454B; handoff 55,818B; verify 109,818B; workflow 137,640B; knowledge 108,882B; image-pipeline 120,994B.
- `contact.png`: 여섯 장 3×2 대조 시트, 1599×600. 세트 전체에서 남색 배경과 민트·호박색 포인트가 유지됨. 생성형 차이로 렌더링 질감은 완전히 동일하지 않으나 1회 재생성 후 주 캐릭터 스타일이 더 가까워졌습니다.
- 게시/외부 채널 전송 없음.
