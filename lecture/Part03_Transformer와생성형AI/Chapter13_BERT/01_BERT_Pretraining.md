# 13.1 Bidirectional Encoder · 13.2 MLM · 13.3 NSP

BERT는 Transformer encoder를 쌓아 왼쪽과 오른쪽 문맥을 함께 사용하는 표현을 학습합니다.

- MLM(Masked Language Modeling): 일부 token을 가리고 원래 token 예측
- NSP(Next Sentence Prediction): 두 문장의 연속 관계 예측(원 BERT 학습 목표)

현대 BERT 계열은 NSP를 생략하거나 다른 목표를 사용하기도 하므로 “모든 encoder 모델이 NSP를 사용한다”고 일반화하지 않습니다.

입력에는 보통 `input_ids`, `attention_mask`, 모델에 따라 `token_type_ids`가 포함됩니다. `[CLS]`, `[SEP]`, `[MASK]` 같은 special token과 ID는 반드시 해당 모델 tokenizer에서 가져옵니다.

## BERT가 양쪽 문맥을 보는 이유

“배를 탔다”와 “배를 먹었다”에서 ‘배’의 의미는 뒤 단어를 봐야 구분됩니다. BERT Encoder는 현재 토큰이 왼쪽과 오른쪽 전체를 참고하도록 학습합니다. 따라서 전체 문장이 주어진 분류·추출 작업에 적합합니다.

## MLM 손실을 쉽게 읽기

\[
L_{MLM}=-\sum_{t\in M}\log P(x_t|x_{\setminus M})
\]

`M`은 가린 위치 집합, `x_t`는 원래 정답 토큰입니다. “오늘 날씨가 [MASK]”에서 정답 ‘좋다’ 확률이 0.8이면 손실은 `-log(0.8)≈0.223`, 확률 0.1이면 약 2.303입니다. 가린 위치가 아닌 토큰에는 MLM 손실을 계산하지 않습니다.

## 입력 임베딩의 세 요소

토큰 임베딩은 단어, 위치 임베딩은 순서, segment 임베딩은 문장 A/B 구분을 표현합니다. 세 벡터는 모두 같은 `hidden_size`라서 원소별로 더할 수 있습니다.

## 특수 토큰

- `[CLS]`: 문장 전체 분류에 주로 사용하는 첫 위치
- `[SEP]`: 문장 또는 문장 쌍의 경계
- `[PAD]`: 배치 길이 맞춤, Attention mask 0
- `[MASK]`: 사전학습에서 예측할 위치

Tokenizer마다 실제 표기와 ID가 다르므로 직접 문자열을 조합하기보다 tokenizer API를 사용합니다.

## NSP를 과장하지 않기

NSP는 두 문장이 실제로 이어지는지 예측하는 초기 BERT 목적입니다. 모든 후속 BERT 계열이 NSP를 사용하는 것은 아닙니다. 핵심은 특정 과제를 외우는 것이 아니라 양방향 Encoder 표현을 대규모 텍스트로 사전학습한다는 점입니다.

## 사전학습과 Fine-tuning의 차이

사전학습은 큰 일반 말뭉치에서 언어 표현을 배우고, Fine-tuning은 작은 업무 데이터에서 분류 헤드와 본체를 함께 조금씩 조정합니다. 처음부터 BERT 전체를 학습하는 것과 다릅니다.
