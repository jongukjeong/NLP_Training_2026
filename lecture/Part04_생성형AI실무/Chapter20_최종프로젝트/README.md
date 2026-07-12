# Chapter 20. 최종 프로젝트


## 핵심 용어 미리보기

본문을 읽기 전에 다음 용어의 뜻과 영어 원어를 먼저 확인합니다. 전체 정의는 [교육과정 핵심 용어집](../../TERMINOLOGY.md)에서 확인할 수 있습니다.

- **기준선(Baseline): 새 시스템의 개선 여부를 비교하는 단순한 기준 방법**
- **데이터 누수(Data Leakage): 평가에만 있어야 할 정보가 학습 과정에 들어가는 문제**
- **서비스 수준 목표(Service Level Objective, SLO): 응답 시간·오류율 등 서비스가 달성할 운영 기준**
- **회귀 시험(Regression Test): 변경 후 기존 기능과 품질이 나빠지지 않았는지 확인하는 시험**

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

## 먼저 읽을 상세 가이드

- [비전공자용 최종 프로젝트 완성 워크북](00_비전공자_최종프로젝트_완성워크북.md): 문제 정의, 기준선, 비용·지연 계산, 평가와 발표를 하나의 흐름으로 정리합니다.

- [원리·수학·실습 연결 가이드](00_원리_수학_실습_가이드.md): 직관, 핵심 공식, 수치 예, 구현 점검을 한 흐름으로 학습합니다.
