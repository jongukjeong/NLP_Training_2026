# 12. 미니 프로젝트: 텍스트 데이터 탐색기

## 프로젝트 목표

CSV 파일을 읽어 텍스트를 정제하고, 정제 결과와 간단한 요약을 저장합니다. 처음에는 함수, CLI, JSON 보고서 없이 기본 흐름을 완성합니다.

```text
입력 → 확인 → 정제 → 요약 → 저장
```

## 시작 전 확인

다음 항목 중 네 가지 이상을 설명할 수 있으면 시작합니다.

- `pd.read_csv()`로 CSV를 읽는 방법
- `dropna()`로 결측 문장을 제거하는 방법
- `.str.strip()`으로 앞뒤 공백을 제거하는 방법
- 빈 문자열을 조건으로 제외하는 방법
- `drop_duplicates()`로 중복을 제거하는 방법
- `to_csv()`로 결과를 저장하는 방법

설명이 어렵다면 [Basic Practice](examples/02_basic_practice/README.md)를 한 번 더 실행합니다.

## 입력 데이터

`reviews.csv`는 `id`, `text`, `label` 열을 가집니다.

```csv
id,text,label
1,배송이 빨라요,positive
2,  환불하고 싶어요  ,negative
3,,unknown
4,배송이 빨라요,positive
```

## 시작 코드

다음 폴더에는 단계별 주석과 입력 데이터가 있습니다.

- [시작 안내](examples/12_mini_project_starter/README.md)
- [시작 코드](examples/12_mini_project_starter/text_data_explorer_starter.py)
- [입력 데이터](examples/12_mini_project_starter/reviews.csv)

```powershell
cd examples\12_mini_project_starter
python text_data_explorer_starter.py
```

## 1단계: 기본 요구사항

1. `reviews.csv`를 읽습니다.
2. 처리 전 행 수를 저장합니다.
3. `text`가 결측인 행을 제거합니다.
4. `text`의 앞뒤 공백과 연속 공백을 정리합니다.
5. 정제 후 빈 문자열인 행을 제거합니다.
6. `label`을 소문자로 통일합니다.
7. 정제된 `text` 기준으로 중복을 제거합니다.
8. `text_length` 열을 추가합니다.
9. 처리 전후 행 수와 레이블 분포를 출력합니다.
10. `reviews_clean.csv`로 저장합니다.

처음부터 열 항목을 모두 작성하지 말고 2~3개씩 구현한 뒤 실행합니다.

## 중간 점검

solution을 보기 전에 다음을 확인합니다.

- 프로그램이 오류 없이 끝까지 실행되는가?
- 결측 행과 공백뿐인 행이 제거됐는가?
- 공백만 다른 중복 문장이 하나로 줄었는가?
- `Positive`가 `positive`로 바뀌었는가?
- 처리 전후 행 수 차이를 설명할 수 있는가?
- 생성된 CSV를 다시 읽을 수 있는가?

## 막혔을 때 사용하는 힌트

### 힌트 1: 결측 제거

```python
df = df.dropna(subset=["text"])
```

### 힌트 2: 공백 정리

```python
df["text"] = df["text"].str.strip()
df["text"] = df["text"].str.replace(r"\s+", " ", regex=True)
```

### 힌트 3: 중복 제거

```python
df = df.drop_duplicates(subset=["text"])
```

힌트는 위에서부터 필요한 만큼만 확인합니다.

## 2단계: 선택 도전

기본 요구사항을 완성한 학습자만 진행합니다.

- 필수 열 `id`, `text`, `label`이 있는지 검사
- 허용되지 않은 레이블 탐지
- 정제 로직을 함수로 분리
- `assert`로 결과 검증
- 입력·출력 경로를 명령행에서 받기
- 처리 결과를 JSON 보고서로 저장
- 입력 파일이 없을 때 이해하기 쉬운 오류 출력

선택 도전을 모두 구현할 필요는 없습니다. 한 가지를 골라 기존 코드에 추가합니다.

## 테스트 시나리오

| 번호 | 입력 | 기본 기대 결과 |
|---|---|---|
| 1 | 정상 CSV | 정제 CSV 생성 |
| 2 | 결측 문장 | 해당 행 제거 |
| 3 | 공백 문장 | 해당 행 제거 |
| 4 | 공백만 다른 중복 | 하나만 유지 |
| 5 | 대문자 레이블 | 소문자로 통일 |

파일 없음, 필수 열 누락, 잘못된 레이블 검사는 선택 도전에서 확인합니다.

## Solution 공개 및 해설

> **강사용 공개 시점:** 수강생이 기본 요구사항을 충분히 시도하고, 공통 오류에 대한 피드백을 받은 뒤 공개합니다.

완성형 solution에는 함수, 타입 힌트, CLI, 오류 검사와 JSON 보고서가 포함되어 있습니다. 수강생의 기본 코드보다 복잡한 것이 정상이며, 처음부터 동일하게 작성하는 것이 목표가 아닙니다.

- [완성형 solution 안내](examples/12_mini_project_solution/README.md)
- [완성형 solution 코드](examples/12_mini_project_solution/text_data_explorer.py)
- [solution 입력 데이터](examples/12_mini_project_solution/reviews.csv)

해설에서는 전체 코드를 다시 입력하기보다 다음 순서로 수강생 코드와 비교합니다.

1. 반복되는 처리를 함수로 분리한 부분
2. 잘못된 입력을 미리 검사한 부분
3. 처리 결과를 보고서로 만든 부분
4. 실행할 때 파일 경로를 바꿀 수 있게 만든 부분

## 완료 기준

- 기본 요구사항 10개 중 8개 이상 구현
- 처리 전후 결과가 달라진 이유 설명
- 자신의 코드에서 정제 단계 하나를 찾아 수정
- solution과 자신의 코드 차이 한 가지 설명

선택 도전 구현 여부는 기본 완료 기준에 포함하지 않습니다.
