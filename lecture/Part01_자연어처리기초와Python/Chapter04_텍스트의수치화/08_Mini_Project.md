# 08. 미니 프로젝트: 평가 가능한 FAQ 검색기

## 목표

FAQ 검색기와 평가 질의셋을 함께 제공해 설정 변화가 검색 품질에 미치는 영향을 측정합니다.

## 필수 기능

- FAQ와 평가 CSV의 스키마 검사
- TF-IDF 기반 상위 k개 검색
- 0 벡터 처리
- 결과 CSV 저장
- Hit@1, Hit@3과 MRR 계산
- 설정과 평가 결과 JSON 저장

## 실행

```powershell
cd lecture\Part01_자연어처리기초와Python\Chapter04_텍스트의수치화\examples\08_mini_project_solution
python faq_search_evaluator.py
```

## 배포용 예제

- [안내](examples/08_mini_project_solution/README.md)
- [코드](examples/08_mini_project_solution/faq_search_evaluator.py)
- [FAQ](examples/08_mini_project_solution/faq.csv)
- [평가 질의](examples/08_mini_project_solution/evaluation.csv)
