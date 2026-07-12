# Chapter 15 비전공자용 Hugging Face 실행 워크북

## Hugging Face는 모델만 제공하는 곳이 아니다

실습에서는 모델 가중치, 설정, Tokenizer, 모델 카드와 실행 라이브러리를 함께 사용합니다. 같은 이름처럼 보여도 과제, 언어, 라이선스와 입력 형식이 다를 수 있으므로 다운로드 전에 모델 카드를 읽습니다.

## 다섯 구성 요소를 구분하기

- Checkpoint: 학습된 가중치가 저장된 버전
- Config: 층 수, 차원, Label 수 같은 구조 정보
- Tokenizer: 문자열을 토큰 ID로 바꾸는 규칙
- Model class: 가중치를 실행할 신경망 구조
- Task head: 분류·질의응답 등 특정 출력층

## Auto Class는 설정에 맞는 구현을 선택한다

```python
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForSequenceClassification.from_pretrained(model_id)
```

`AutoModel`은 기본 표현을 출력하고, `AutoModelForSequenceClassification`은 분류 Head까지 포함합니다. 과제에 맞지 않는 클래스를 선택하면 출력 shape가 예상과 달라집니다.

## Tokenizer 결과를 읽기

```text
input_ids      : 토큰을 나타내는 정수 ID
attention_mask : 실제 토큰은 1, Padding은 0
token_type_ids : 모델에 따라 문장 구간 표시
```

문자열을 눈으로 보는 것만으로는 부족합니다. 토큰 목록, ID, 잘림 여부와 `[UNK]` 비율을 함께 확인합니다.

## Logit을 확률로 바꾸기

모델 출력이 `[-0.4, 1.2, 0.1]`이라면 아직 확률이 아닙니다.

\[
p_i=\frac{e^{z_i}}{\sum_j e^{z_j}}
\]

Softmax 후 가장 큰 위치를 Label ID와 연결합니다. `id2label` 설정이 실제 데이터 Label 순서와 일치하는지 반드시 확인합니다.

## Pipeline은 편리하지만 중간 과정을 숨긴다

```python
classifier = pipeline("text-classification", model=model_id)
result = classifier("배송이 아직 오지 않았어요")
```

빠른 시연에는 좋지만 Tokenizer 옵션, 최대 길이, Batch 처리와 Label 매핑을 확인하기 위해 직접 추론 코드도 한 번 실행합니다.

## Padding은 Batch에서 가장 긴 문장에 맞춘다

모든 데이터를 고정 최대 길이로 채우면 계산 낭비가 큽니다. Dynamic padding은 현재 Batch의 최장 문장에 맞춰 길이를 정합니다. 길이가 비슷한 문장을 묶으면 효율이 더 좋아질 수 있습니다.

## 모델 선택 기록표

| 항목 | 기록할 내용 |
|---|---|
| 목적 | 분류, 임베딩, 생성 등 |
| 언어·도메인 | 한국어, 뉴스, 상담 등 |
| 라이선스 | 상업적 사용과 재배포 조건 |
| 크기 | 파라미터, 파일 용량, 메모리 |
| 입력 제한 | 최대 토큰 길이 |
| 평가 | 사용 데이터와 지표 |
| Revision | 재현할 Commit 또는 Tag |

## 저장 후 다시 불러오는 것까지가 실습이다

Tokenizer와 Model을 같은 출력 폴더에 저장하고 새 프로세스에서 다시 불러옵니다. 대표 입력의 Label과 점수가 허용 범위 안에서 같은지 확인해야 배포 가능한 산출물입니다.

