# 08. 미니 프로젝트: 도메인 용어 탐색기

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
