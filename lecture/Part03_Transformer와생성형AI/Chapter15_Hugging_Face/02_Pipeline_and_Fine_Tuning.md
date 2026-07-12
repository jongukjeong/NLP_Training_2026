# 15.4 Pipeline · 15.5 Fine-tuning

Pipeline은 tokenizer, model 전처리와 후처리를 task별 API로 묶어 빠른 inference 기준선을 만듭니다.

```python
classifier = pipeline("text-classification", model=model_id)
classifier(["좋아요", "아쉬워요"])
```

명시적인 제어가 필요하면 tokenizer와 model을 직접 호출합니다. batching이 항상 빠른 것은 아니므로 sequence 길이와 device에서 측정합니다.

Fine-tuning 절차:

1. train/validation/test 분리
2. tokenizer로 truncation과 padding
3. task-specific AutoModel 로드
4. TrainingArguments와 Trainer 또는 직접 loop
5. metric과 checkpoint 선택
6. 모델·tokenizer·label mapping 저장

Hub에 push하기 전에 데이터·weight 라이선스, 개인정보와 공개 범위를 확인합니다.

## Pipeline을 자동 조리 기계로 비유하기

Pipeline은 재료 손질(tokenizer), 조리(model), 접시에 담기(post-processing)를 한 번에 수행합니다. 빠르게 모델을 시험하기 좋지만 내부 기본값을 모르면 최대 길이, 장치, label 의미를 잘못 해석할 수 있습니다.

```python
from transformers import pipeline
classifier = pipeline(
    "text-classification",
    model="사용할-checkpoint",
    device=-1,
)
print(classifier("배송이 너무 늦어요"))
```

`device=-1`은 일반적으로 CPU, GPU는 환경에 맞는 장치 번호를 지정합니다. 모델 카드의 label mapping을 확인하지 않고 `LABEL_0`을 긍정으로 가정하지 않습니다.

## Batch 추론

한 문장씩 반복 호출하는 것보다 리스트 또는 Dataset으로 batch 처리하면 장치를 효율적으로 사용할 수 있습니다. batch를 너무 크게 하면 메모리 부족이 생기므로 길이 분포와 GPU 메모리로 정합니다.

## Fine-tuning 데이터 흐름

```text
원본 데이터
 → tokenize(map)
 → train/validation Dataset
 → Data Collator로 batch padding
 → Model forward/loss
 → optimizer update
 → validation metric
```

Dynamic padding은 배치 안의 가장 긴 문장까지만 맞춰 고정 최대 길이 padding보다 계산을 줄일 수 있습니다.

## Data Collator의 역할

Tokenizer 결과를 같은 길이의 텐서 batch로 묶습니다. 토큰 분류에서는 subword와 원래 레이블 정렬이 필요하고, 언어모델 학습에서는 causal 또는 MLM용 레이블을 구성합니다. 과제마다 collator가 다릅니다.

## Trainer가 대신하는 것

Trainer는 학습 루프, evaluation, checkpoint, logging을 묶습니다. 데이터와 metric 정의를 대신 판단해 주는 것은 아닙니다. `TrainingArguments`의 evaluation/save 전략, batch, epoch, learning rate를 명시하고 버전에 따른 이름 변화를 확인합니다.

## metric 함수 주의

로짓에서 `argmax`로 예측 클래스를 만들고 정답과 비교합니다. padding label `-100`을 제외해야 하는 토큰 분류에서는 마스크 처리가 필요합니다. Accuracy 하나만 반환하지 말고 문제에 맞는 F1을 추가합니다.

## 저장 산출물

모델 가중치, config, tokenizer 파일, label mapping, 학습 파라미터, 평가 결과를 함께 저장합니다. 새 환경에서 `from_pretrained()`로 불러와 대표 입력의 결과를 비교합니다.

## 실무 점검

- 모델 라이선스와 상업적 사용 조건
- 입력 언어와 학습 언어 일치 여부
- 원격 코드 실행 옵션
- 개인정보가 외부 Hub로 업로드되지 않는지
- revision과 라이브러리 버전 고정
