# 08. 실습 과제

## 과제: 고객 리뷰 전처리

`reviews_raw.csv`의 `text` 열을 다음 규칙으로 처리합니다.

1. 원본 `text`를 보존합니다.
2. Unicode NFC 정규화를 적용합니다.
3. zero-width space와 연속 공백을 정리합니다.
4. URL, 이메일, 휴대전화 번호를 각각 `<URL>`, `<EMAIL>`, `<PHONE>`으로 마스킹합니다.
5. 정제 결과를 `clean_text` 열에 저장합니다.
6. 공백 기준 토큰 수를 `token_count`에 저장합니다.
7. 빈 결과가 생기지 않았는지 검증합니다.
8. 결과 CSV와 처리 보고서 JSON을 `output/`에 저장합니다.

## 평가 기준

| 항목 | 배점 |
|---|---:|
| 정규화와 마스킹 | 40 |
| 원본 보존과 파생 열 | 20 |
| 전후 통계와 검증 | 20 |
| 경로·인코딩·가독성 | 20 |

## 배포용 완성 답안

- [답안 안내](examples/08_assignment_solution/README.md)
- [답안 코드](examples/08_assignment_solution/preprocess_reviews.py)
- [입력 데이터셋](examples/08_assignment_solution/reviews_raw.csv)

> 다음: [미니 프로젝트](09_Mini_Project.md)
