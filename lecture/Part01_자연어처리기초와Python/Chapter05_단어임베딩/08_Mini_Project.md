# 08. 미니 프로젝트: 도메인 용어 탐색기

<!-- BEGIN: BEGINNER_LEARNING_PATH -->
## 난이도와 Solution 공개 원칙

- 기본 요구사항을 먼저 작은 단계로 나누어 실행합니다.
- 함수화, 타입 힌트, 복합 평가와 운영 기능은 선택 확장입니다.
- solution은 직접 시도하고 공통 오류 피드백을 받은 뒤 공개합니다.
- 처음부터 solution과 같은 구조로 작성하는 것은 목표가 아닙니다.
<!-- END: BEGINNER_LEARNING_PATH -->

## 목표

고객지원 말뭉치에서 작은 임베딩을 만들고 입력 단어의 유사 단어를 검색하는 배포용 프로그램을 완성합니다.

## 필수 기능

- UTF-8 말뭉치 입력
- 최소 빈도·문맥 창·차원 설정
- 동시출현 희소 행렬과 SVD
- 미등록어 안내
- 유사 단어 결과 CSV
- 설정·어휘·설명된 분산 비율 JSON
- 고정 시드를 통한 재현성

## 실행

```powershell
cd lecture\Part01_자연어처리기초와Python\Chapter05_단어임베딩\examples\08_mini_project_solution
python domain_term_explorer.py 배송
```

## 배포용 예제

- [안내](examples/08_mini_project_solution/README.md)
- [코드](examples/08_mini_project_solution/domain_term_explorer.py)
- [말뭉치](examples/08_mini_project_solution/support_corpus.txt)

이 장을 마치면 희소한 단어 빈도 표현에서 의미 관계를 반영하는 밀집 벡터까지의 흐름을 설명할 수 있습니다.
