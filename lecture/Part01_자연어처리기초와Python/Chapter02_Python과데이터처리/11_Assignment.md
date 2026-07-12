# 11. 실습 과제

## 과제: 고객 문의 데이터 정제

다음 원본 데이터를 Python과 pandas로 정제합니다.

```python
raw_records = [
    {"id": 1, "text": "  배송이 빨라요 ", "label": "Positive"},
    {"id": 2, "text": None, "label": "unknown"},
    {"id": 3, "text": "환불하고   싶어요", "label": "NEGATIVE"},
    {"id": 4, "text": "배송이 빨라요", "label": "positive"},
    {"id": 5, "text": "   ", "label": "neutral"},
]
```

## 필수 요구사항

1. DataFrame으로 변환합니다.
2. 원본 행 수와 열 이름을 출력합니다.
3. `text`가 `None`이거나 공백뿐인 행을 제거합니다.
4. 앞뒤 공백과 내부 연속 공백을 정리합니다.
5. `label`을 소문자로 통일합니다.
6. 정제된 `text` 기준 중복을 제거합니다.
7. `text_length` 열을 추가합니다.
8. 레이블별 문장 수를 계산합니다.
9. 결과를 `customer_inquiries_clean.csv`에 UTF-8 계열 인코딩으로 저장합니다.
10. 처리 전후 행 수와 제거 건수를 딕셔너리로 출력합니다.

## 추가 도전

- 허용 레이블 집합을 만들고 잘못된 레이블을 탐지합니다.
- 입력과 출력 경로를 `pathlib.Path`로 관리합니다.
- 정제 로직을 `clean_dataframe()` 함수로 분리합니다.
- 빈 DataFrame이 입력되어도 이해하기 쉬운 결과를 반환합니다.
- 결과 검증용 `assert`를 네 개 이상 작성합니다.

## 제출물

사용자가 “마크다운 문서만” 범위를 선택했으므로 이 저장소 단계에서는 실행 파일을 만들지 않습니다. 과제를 수행할 때는 다음을 별도 제출합니다.

- 작성한 Python 코드 또는 노트북
- 생성된 CSV
- 처리 결과 요약 5줄 이내
- 검증 결과

코드와 원본 데이터셋은 하나의 과제 폴더에 함께 두고, 생성된 CSV는 그 폴더의 `output/`에 저장합니다.

## 배포용 완성 답안

강의 시간이 부족할 때 바로 배포할 수 있는 실행 코드와 입력 데이터셋은 이 문서와 같은 Chapter 디렉터리 아래에 있습니다.

- [완성 답안 안내](examples/11_assignment_solution/README.md)
- [완성 답안 코드](examples/11_assignment_solution/assignment_solution.py)
- [입력 데이터셋](examples/11_assignment_solution/customer_inquiries.csv)

## 평가 기준

| 항목 | 배점 |
|---|---:|
| 필수 정제 규칙 구현 | 40 |
| 함수 구조와 가독성 | 20 |
| 파일 입출력·인코딩 | 15 |
| 처리 통계와 검증 | 15 |
| 추가 도전 | 10 |
