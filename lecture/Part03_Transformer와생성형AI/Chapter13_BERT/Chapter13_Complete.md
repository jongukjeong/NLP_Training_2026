# Chapter 13. BERT — 통합 원고

> 이 문서는 Chapter 13. BERT 의 최상위 강의 마크다운을 학습 순서대로 합친 통합 원고입니다. 개별 원본 파일은 그대로 유지합니다.

## 통합 목차

- Chapter 13. BERT — `README.md`
- 13.1 Bidirectional Encoder · 13.2 MLM · 13.3 NSP — `01_BERT_Pretraining.md`
- 13.4 Fine-tuning · 13.5 Sentence Classification — `02_Fine_Tuning.md`
- 요약과 퀴즈 — `03_Summary_and_Quiz.md`
- 실습: 한국어 BERT 활용 — `04_Practice.md`

---

<!-- SOURCE: README.md -->

# Chapter 13. BERT

# Chapter 13. BERT

1. [Bidirectional Encoder·MLM·NSP](01_BERT_Pretraining.md)
2. [Fine-tuning과 Sentence Classification](02_Fine_Tuning.md)
3. [요약과 퀴즈](03_Summary_and_Quiz.md)
4. [실습: 한국어 BERT 활용](04_Practice.md)


---

<!-- SOURCE: 01_BERT_Pretraining.md -->

# 13.1 Bidirectional Encoder · 13.2 MLM · 13.3 NSP

# 13.1 Bidirectional Encoder · 13.2 MLM · 13.3 NSP

BERT는 Transformer encoder를 쌓아 왼쪽과 오른쪽 문맥을 함께 사용하는 표현을 학습합니다.

- MLM(Masked Language Modeling): 일부 token을 가리고 원래 token 예측
- NSP(Next Sentence Prediction): 두 문장의 연속 관계 예측(원 BERT 학습 목표)

현대 BERT 계열은 NSP를 생략하거나 다른 목표를 사용하기도 하므로 “모든 encoder 모델이 NSP를 사용한다”고 일반화하지 않습니다.

입력에는 보통 `input_ids`, `attention_mask`, 모델에 따라 `token_type_ids`가 포함됩니다. `[CLS]`, `[SEP]`, `[MASK]` 같은 special token과 ID는 반드시 해당 모델 tokenizer에서 가져옵니다.


---

<!-- SOURCE: 02_Fine_Tuning.md -->

# 13.4 Fine-tuning · 13.5 Sentence Classification

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

# 실습: 한국어 BERT 활용

한국어 BERT tokenizer와 encoder를 내려받아 문장 embedding과 cosine similarity를 계산합니다.

- [안내](examples/04_korean_bert_solution/README.md)
- [코드](examples/04_korean_bert_solution/korean_bert_embeddings.py)
- [문장 데이터](examples/04_korean_bert_solution/sentences.csv)

