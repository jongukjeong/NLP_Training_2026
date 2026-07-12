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
