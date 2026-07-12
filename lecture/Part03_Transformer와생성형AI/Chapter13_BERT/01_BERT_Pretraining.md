# 13.1 Bidirectional Encoder · 13.2 MLM · 13.3 NSP

BERT는 Transformer encoder를 쌓아 왼쪽과 오른쪽 문맥을 함께 사용하는 표현을 학습합니다.

- MLM(Masked Language Modeling): 일부 token을 가리고 원래 token 예측
- NSP(Next Sentence Prediction): 두 문장의 연속 관계 예측(원 BERT 학습 목표)

현대 BERT 계열은 NSP를 생략하거나 다른 목표를 사용하기도 하므로 “모든 encoder 모델이 NSP를 사용한다”고 일반화하지 않습니다.

입력에는 보통 `input_ids`, `attention_mask`, 모델에 따라 `token_type_ids`가 포함됩니다. `[CLS]`, `[SEP]`, `[MASK]` 같은 special token과 ID는 반드시 해당 모델 tokenizer에서 가져옵니다.
