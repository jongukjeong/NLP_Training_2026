# Chapter 13 통합 강의 원고

> 이 문서는 Chapter  원본 강의 문서를 학습 순서대로 합친 통합본입니다. 개별 원본 파일은 그대로 유지합니다.

---

<!-- SOURCE: README.md -->

# Chapter 13. BERT

1. [Bidirectional Encoder·MLM·NSP](01_BERT_Pretraining.md)
2. [Fine-tuning과 Sentence Classification](02_Fine_Tuning.md)
3. [요약과 퀴즈](03_Summary_and_Quiz.md)
4. [실습: 한국어 BERT 활용](04_Practice.md)

## 먼저 읽을 상세 가이드

- [원리·수학·실습 연결 가이드](00_원리_수학_실습_가이드.md): 직관, 핵심 공식, 수치 예, 구현 점검을 한 흐름으로 학습합니다.

---

<!-- SOURCE: 00_원리_수학_실습_가이드.md -->

# Chapter 13 원리·수학·실습 가이드

## 1. BERT의 방향성

BERT는 Transformer Encoder를 사용해 한 토큰이 왼쪽과 오른쪽 문맥을 모두 본다. 문장 분류·개체명 인식처럼 전체 입력이 이미 주어진 이해 과제에 적합하다.

## 2. MLM

일부 토큰을 가리고 원래 토큰을 맞힌다.

\[
L_{MLM}=-\sum_{t\in M}\log P(x_t\mid x_{\setminus M})
\]

`M`은 예측 대상 위치다. 모든 위치가 아니라 마스킹된 위치에서만 손실을 계산한다. “나는 [MASK]에 간다”에서 양쪽 문맥으로 “학교”를 예측한다.

NSP는 두 문장이 이어지는지 예측하는 초기 BERT 목적이다. 후속 모델은 NSP를 변경하거나 제거하기도 하므로 “BERT 계열 모두의 필수 요소”로 일반화하지 않는다.

## 3. 입력과 Fine-tuning

입력은 token embedding, position embedding, segment embedding의 합이다. `[CLS] 문장 [SEP]` 형태에서 `[CLS]` 표현 `[B,H]`에 분류층 `[H,C]`를 붙인다.

\[
p=softmax(h_{CLS}W+b),\quad L=-\log p_y
\]

```python
batch = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
outputs = model(**batch, labels=labels)
print(outputs.logits.shape)  # [B, C]
```

작은 데이터에서는 낮은 학습률, 짧은 epoch, 검증 기반 early stopping이 중요하다. tokenizer와 model checkpoint는 반드시 짝을 맞춘다.

## 4. 평가

데이터를 무작위로만 나누면 동일 작성자·중복 문장이 누수될 수 있다. 시간·고객·문서 단위 분할을 검토하고, 클래스별 F1과 혼동 행렬, 최대 길이로 잘린 비율을 기록한다.

1. MLM 손실을 모든 토큰에 계산하지 않는 이유는?
2. `[CLS]` 기반 3분류 로짓 shape는?
3. tokenizer와 model을 같은 checkpoint에서 불러야 하는 이유는?

---

<!-- SOURCE: 01_BERT_Pretraining.md -->

# 13.1 Bidirectional Encoder · 13.2 MLM · 13.3 NSP

BERT는 Transformer encoder를 쌓아 왼쪽과 오른쪽 문맥을 함께 사용하는 표현을 학습합니다.

- MLM(Masked Language Modeling): 일부 token을 가리고 원래 token 예측
- NSP(Next Sentence Prediction): 두 문장의 연속 관계 예측(원 BERT 학습 목표)

현대 BERT 계열은 NSP를 생략하거나 다른 목표를 사용하기도 하므로 “모든 encoder 모델이 NSP를 사용한다”고 일반화하지 않습니다.

입력에는 보통 `input_ids`, `attention_mask`, 모델에 따라 `token_type_ids`가 포함됩니다. `[CLS]`, `[SEP]`, `[MASK]` 같은 special token과 ID는 반드시 해당 모델 tokenizer에서 가져옵니다.

---

<!-- SOURCE: 02_Fine_Tuning.md -->

# 13.4 Fine-tuning · 13.5 Sentence Classification

Fine-tuning은 사전학습 encoder 위에 task head를 추가하고 작은 learning rate로 전체 또는 일부 파라미터를 학습합니다.

```text
text → tokenizer → BERT encoder → pooled/CLS representation → classifier
```

검증 항목:

- tokenizer와 model ID/revision 일치
- max_length와 truncation 비율
- label mapping 저장
- class imbalance와 macro F1
- seed별 성능 분산
- 사전학습 데이터와 평가 데이터의 중복 가능성

작은 데이터에서는 먼저 encoder를 고정한 linear probe를 기준선으로 만들고 전체 fine-tuning과 비교할 수 있습니다.

---

<!-- SOURCE: 03_Summary_and_Quiz.md -->

# 요약과 퀴즈

1. BERT의 기본 backbone은? **Transformer encoder**
2. MLM의 목표는? **가려진 token 예측**
3. 모든 BERT 계열이 NSP를 쓰나요? **아니요**
4. tokenizer와 model checkpoint를 맞춰야 하는 이유는? **어휘·special token ID 불일치 방지**
5. 긴 문장 처리 시 기록할 값은? **truncation 비율과 max_length**
6. Fine-tuning에서 보통 작은 learning rate를 쓰는 이유는? **사전학습 표현의 급격한 손상 완화**

---

<!-- SOURCE: 04_Practice.md -->

# 실습: 한국어 BERT 활용

한국어 BERT tokenizer와 encoder를 내려받아 문장 embedding과 cosine similarity를 계산합니다.

- [안내](examples/04_korean_bert_solution/README.md)
- [코드](examples/04_korean_bert_solution/korean_bert_embeddings.py)
- [문장 데이터](examples/04_korean_bert_solution/sentences.csv)

