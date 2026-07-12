# Chapter 13 BERT 분류 실습 따라가기

## 전체 흐름

```text
문장 → Tokenizer → input_ids/attention_mask
→ BERT Encoder → CLS 벡터 → 분류층 → logits → loss
```

한글 문장이 바로 BERT로 들어가는 것이 아니라 tokenizer가 checkpoint의 어휘 규칙에 따라 ID로 바꿉니다.

## Tokenizer 출력 읽기

```python
batch = tokenizer(
    ["배송이 늦어요", "환불하고 싶어요"],
    padding=True,
    truncation=True,
    return_tensors="pt",
)
print(batch["input_ids"].shape)
print(batch["attention_mask"])
```

두 문장을 batch로 묶었으므로 첫 차원은 2입니다. Attention mask에서 1은 실제 토큰, 0은 padding입니다.

## Logits

3분류 모델의 출력이 `[2.4,0.7,-0.2]`라면 Softmax 확률은 첫 클래스가 가장 큽니다. Logits는 합이 1일 필요가 없으며 손실함수 내부에서 안정적으로 Softmax가 계산될 수 있습니다.

## Label mapping

```python
id2label = {0: "배송", 1: "환불", 2: "계정"}
label2id = {v: k for k, v in id2label.items()}
```

학습·평가·저장·서비스에서 mapping이 같아야 합니다. 숫자 0을 임의로 긍정이나 배송이라고 가정하지 않습니다.

## Freeze 실험

첫 실험은 BERT 전체를 고정하고 분류층만 학습해 빠른 기준선을 만들 수 있습니다. 이후 전체 Fine-tuning과 비교합니다.

```python
for parameter in model.base_model.parameters():
    parameter.requires_grad = False
```

모델마다 base model 속성 이름이 다를 수 있으므로 학습 가능한 파라미터 수를 출력합니다.

## 학습률과 epoch

BERT 전체 Fine-tuning은 작은 학습률에서 시작하고 validation 성능이 나빠지기 전 중단합니다. 큰 학습률로 빠르게 loss가 내려가도 기존 표현이 손상될 수 있습니다.

## 최대 길이 분석

Tokenizer로 모든 문장의 토큰 길이를 측정합니다. 최대 길이 128에서 10%가 잘리고, 중요한 결론이 문장 끝에 있다면 256 또는 긴 문서 분할을 검토합니다.

## 불균형 평가

Accuracy와 macro F1을 함께 봅니다. 희소 클래스 Recall이 0이라면 전체 Accuracy가 높아도 실무에서는 해당 문의를 전혀 찾지 못합니다.

## 대표 오류

- tokenizer와 model checkpoint 불일치
- label ID 범위 오류
- attention mask 누락
- test를 보며 학습률과 threshold 선택
- 중복 문장 누수
- 저장 후 id2label 누락

## 결과 설명 예

“Macro F1 0.82”에 더해 “배송 90건 중 84건, 환불 30건 중 21건을 찾았고 환불 Recall이 상대적으로 낮았다”고 실제 건수로 설명합니다.
