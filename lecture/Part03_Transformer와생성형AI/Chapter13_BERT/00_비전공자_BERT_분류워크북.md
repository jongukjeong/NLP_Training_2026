# Chapter 13 비전공자용 BERT 분류 워크북

## BERT는 빈칸의 양쪽 문맥을 함께 본다

“오늘은 날씨가 [MASK] 산책을 했다”에서 빈칸을 맞히려면 앞뒤 단어가 모두 필요합니다. BERT는 Transformer Encoder를 사용해 각 토큰이 양쪽 문맥을 참고하도록 사전학습합니다.

## MLM은 일부 토큰을 가리고 맞히는 학습이다

가려진 위치 집합을 (M)이라고 할 때 손실은 다음과 같이 볼 수 있습니다.

\[
L_{MLM}=-\sum_{i\in M}\log P(x_i\mid x_{\setminus M})
\]

정답 토큰의 확률이 높으면 손실이 작고, 낮으면 손실이 커집니다. 모든 토큰이 아니라 선택된 Mask 위치의 예측을 평가한다는 점이 중요합니다.

## 입력 하나에는 세 종류의 정보가 더해진다

\[
E=E_{token}+E_{position}+E_{segment}
\]

- Token embedding: 어떤 토큰인가?
- Position embedding: 몇 번째 위치인가?
- Segment embedding: 첫 번째 문장인가, 두 번째 문장인가?

## 특수 토큰의 역할

- `[CLS]`: 문장 전체 분류에 사용할 대표 위치
- `[SEP]`: 문장 또는 구간의 경계
- `[PAD]`: Batch 길이를 맞추는 빈 위치
- `[MASK]`: MLM에서 맞힐 위치

Tokenizer마다 토큰과 ID가 다르므로 모델과 Tokenizer는 같은 Checkpoint에서 불러와야 합니다.

## 문장 분류는 대표 벡터에 작은 분류기를 붙인다

클래스가 세 개라면 분류 Head는 세 개의 Logit을 만듭니다.

\[
z=h_{CLS}W+b
\]

\[
P(y=k)=\frac{e^{z_k}}{\sum_j e^{z_j}}
\]

Logit은 아직 확률이 아닌 점수입니다. Softmax를 적용한 뒤 가장 큰 확률의 Label을 선택합니다.

## Fine-tuning은 이미 배운 표현을 조금 조정한다

처음부터 언어를 다시 배우는 것이 아니라, 사전학습된 표현을 현재 분류 과제에 맞게 조정합니다. 너무 큰 학습률은 기존 표현을 급격히 바꿀 수 있어 일반적인 신경망 학습보다 작은 학습률을 사용합니다.

## 최대 길이는 데이터로 정한다

무조건 512를 선택하면 Padding과 계산 낭비가 커질 수 있습니다. 문장 토큰 길이의 90·95·99 분위수를 보고 최대 길이를 정하고, 잘리는 데이터 비율을 기록합니다.

## 평가에서는 클래스별 오류를 본다

전체 Accuracy 외에 클래스별 Precision, Recall, F1과 Confusion Matrix를 확인합니다. 데이터가 불균형하면 Macro F1을 함께 보고, 틀린 문장을 직접 읽어 Tokenization·Label·문맥 문제로 나눕니다.

## 실습 전 확인 순서

1. Label과 숫자 ID 매핑을 고정합니다.
2. 학습·검증·테스트 중복을 제거합니다.
3. Tokenizer 출력의 `input_ids`, `attention_mask` shape를 확인합니다.
4. 한 Batch의 Logit shape가 `(batch, class_count)`인지 확인합니다.
5. 저장 후 다시 불러와 같은 입력의 결과를 비교합니다.

