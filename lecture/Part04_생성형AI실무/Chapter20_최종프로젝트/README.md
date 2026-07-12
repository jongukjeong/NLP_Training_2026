# Chapter 20. 최종 프로젝트

## 프로젝트: 근거 기반 고객지원 AI Assistant

내부 정책 지식에서 관련 문서를 검색하고 출처와 함께 답변합니다. API 키가 있으면 검색 근거만 사용하는 생성 답변을 만들고, 없으면 검색된 정책 문장을 그대로 제공하는 안전한 기준선으로 동작합니다.

## 학습 단계

1. [프로젝트 기획](01_Project_Planning.md)
2. [데이터 수집](02_Data_Collection.md)
3. [모델 개발](03_Model_Development.md)
4. [서비스 구현](04_Service_Implementation.md)
5. [발표 및 피드백](05_Presentation_and_Feedback.md)

## 완성 예제

[final_project_solution](final_project_solution/README.md)에 다음을 포함합니다.

- versioned knowledge/evaluation CSV
- TF-IDF hybrid-ready retriever
- 출처 포함 CLI assistant
- 선택형 OpenAI Responses API 생성
- Hit@1·Hit@3·MRR 평가
- 단위 테스트
- 프로젝트 보고서·발표 템플릿

## 완료 기준

- `pytest` 통과
- 평가셋 Hit@3 목표 달성
- 근거 없는 질문의 low-score 처리
- 모든 답변에 source 표시
- API key 없이도 실행
- 개인정보·권한·비용·실패 대응 설명
