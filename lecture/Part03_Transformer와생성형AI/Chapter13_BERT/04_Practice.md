# 실습: 한국어 BERT 활용

<!-- BEGIN: BEGINNER_LEARNING_PATH -->
## 난이도와 Solution 공개 원칙

- 기본 요구사항을 먼저 작은 단계로 나누어 실행합니다.
- 함수화, 타입 힌트, 복합 평가와 운영 기능은 선택 확장입니다.
- solution은 직접 시도하고 공통 오류 피드백을 받은 뒤 공개합니다.
- 처음부터 solution과 같은 구조로 작성하는 것은 목표가 아닙니다.
<!-- END: BEGINNER_LEARNING_PATH -->

한국어 BERT tokenizer와 encoder를 내려받아 문장 embedding과 cosine similarity를 계산합니다.

- [안내](examples/04_korean_bert_solution/README.md)
- [코드](examples/04_korean_bert_solution/korean_bert_embeddings.py)
- [문장 데이터](examples/04_korean_bert_solution/sentences.csv)

## 실습 목표

한국어 문장을 입력해 클래스별 logits와 확률을 얻고, 작은 데이터셋으로 Fine-tuning한 뒤 클래스별 성능을 평가합니다.

## 데이터 형식

```csv
text,label
배송이 너무 늦어요,0
환불하고 싶습니다,1
비밀번호를 잊었어요,2
```

레이블 정의와 `id2label`을 README에 기록합니다.

## Tokenize

```python
def tokenize(batch):
    return tokenizer(
        batch["text"],
        truncation=True,
        max_length=128,
    )
```

전체 데이터 토큰 길이 분포를 먼저 확인해 128에서 잘리는 비율을 계산합니다.

## 모델 로딩

```python
model = AutoModelForSequenceClassification.from_pretrained(
    checkpoint,
    num_labels=3,
    id2label={0: "배송", 1: "환불", 2: "계정"},
    label2id={"배송": 0, "환불": 1, "계정": 2},
)
```

Checkpoint와 tokenizer를 같은 이름에서 불러옵니다.

## 평가 함수

```python
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = logits.argmax(axis=-1)
    return {
        "accuracy": accuracy_score(labels, predictions),
        "macro_f1": f1_score(labels, predictions, average="macro"),
    }
```

클래스별 Precision·Recall도 최종 보고서에 추가합니다.

## 오류 분석

확신하며 틀린 문장, 최대 길이로 잘린 문장, 두 의도가 있는 문장, 미등록 제품명을 분리해 읽습니다.

## 재현성

Checkpoint revision, tokenizer, split seed, learning rate, epoch, batch, 최고 checkpoint와 라이브러리 버전을 기록합니다.

## 실습 완료 기준

기준선, 전체/클래스별 지표, 혼동 행렬, 10개 이상의 오분류, 저장 모델 재로딩 결과를 제출합니다.
