# Chapter 13 통합 강의 원고

---

<!-- SOURCE: README.md -->

# Chapter 13. BERT

<!-- BEGIN: BEGINNER_LEARNING_PATH -->
## 권장 학습 순서

```text
Step by Step → Basic Practice → Practice·Assignment → 피드백 → Solution
```

비전공자와 입문자는 [단계별 학습 경로](LEARNING_PATH.md)를 먼저 확인합니다. 완성형 solution의 고급 구조는 선택 학습입니다.
<!-- END: BEGINNER_LEARNING_PATH -->

## 핵심 용어 미리보기

본문을 읽기 전에 다음 용어의 뜻과 영어 원어를 먼저 확인합니다. 전체 정의는 [교육과정 핵심 용어집](../../TERMINOLOGY.md)에서 확인할 수 있습니다.

- **양방향 인코더(Bidirectional Encoder): 토큰의 앞뒤 문맥을 함께 참고하는 Encoder**
- **마스크 언어 모델링(Masked Language Modeling, MLM): 가린 토큰을 맞히는 사전학습 방법**
- **미세조정(Fine-tuning): 사전학습 모델을 특정 과제로 추가 학습하는 과정**
- **로짓(Logit): 확률 변환 전 클래스별 원점수**

1. [Bidirectional Encoder·MLM·NSP](01_BERT_Pretraining.md)
2. [Fine-tuning과 Sentence Classification](02_Fine_Tuning.md)
3. [퀴즈](03_Summary_and_Quiz.md)
4. [실습: 한국어 BERT 활용](04_Practice.md)

## 먼저 읽을 상세 가이드

- [비전공자용 BERT 분류 워크북](00_비전공자_BERT_분류워크북.md): MLM부터 Logit, Fine-tuning과 분류 평가까지 단계별로 확인합니다.

- [원리·수학·실습 연결 가이드](00_원리_수학_실습_가이드.md): 직관, 핵심 공식, 수치 예, 구현 점검을 한 흐름으로 학습합니다.

---

<!-- SOURCE: LEARNING_PATH.md -->

# Chapter 13 비전공자 학습 경로

## 기본 도달 목표

한국어 문장을 토큰화하고 BERT 표현 shape 확인

완성형 코드를 처음부터 모두 이해하거나 다시 작성하는 것은 기본 목표가 아닙니다.

## 1. Step by Step — 강사와 함께

1. 문장 두 개를 준비한다
2. Tokenizer 출력을 읽는다
3. 모델 출력 shape를 확인한다
4. 두 문장의 표현을 비교한다

각 단계가 끝날 때 입력, 출력 또는 중간 결과를 화면에서 확인합니다. 설명할 수 없는 줄은 다음 단계로 넘어가기 전에 질문합니다.

## 2. Basic Practice — 짧은 흐름 연결

Step by Step의 네 단계를 한 흐름으로 연결합니다. 처음에는 함수 분리, 타입 힌트, 복잡한 예외 처리와 자동 보고서를 요구하지 않습니다.

완료 확인:

- 입력이 무엇인지 설명한다.
- 핵심 처리 한 단계를 찾아 수정한다.
- 출력이 예상과 다른 이유를 한 가지 찾는다.
- 실행 결과를 짧게 기록한다.

## 실행 코드 위치

- [Step by Step](examples/01_step_by_step/README.md)
- [Basic Practice](examples/02_basic_practice/README.md)
- [Practice Starter](examples/03_practice_starter/README.md)

세 자료는 외부 모델이나 API 없이 핵심 흐름을 먼저 이해하도록 구성했습니다. 실제 라이브러리와 완성형 구조는 기존 solution에서 비교합니다.

## 3. Practice·Assignment — 먼저 시도

[04_Practice.md](04_Practice.md)의 기본 요구사항을 먼저 수행합니다. 막히면 전체 solution 대신 필요한 단계의 힌트만 확인합니다.

## 4. Solution — 피드백 후 공개

[examples/04_korean_bert_solution/README.md](examples/04_korean_bert_solution/README.md)은 다수의 수강생이 기본 요구사항을 시도하고 공통 오류를 함께 확인한 뒤 공개합니다. 자신의 코드와 다음 항목을 비교합니다.

1. 반복되는 처리를 어떻게 묶었는가
2. 잘못된 입력을 어디에서 검사하는가
3. 결과를 어떻게 검증하고 기록하는가

## 선택 확장

- fine-tuning
- 평가 함수
- 오류 분석
- 배포 점검

선택 확장은 기본 완료 기준에 포함하지 않습니다.

---

<!-- SOURCE: 00_BERT_분류_실습_따라가기.md -->

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

---

<!-- SOURCE: 00_BERT_평가와_배포점검.md -->

# Chapter 13 BERT 평가와 배포 점검

## 모델 크기와 품질 비교

작은 BERT와 기본 크기 모델을 같은 평가셋에서 비교합니다.

| 모델 | Params | Macro F1 | P95 | 메모리 |
|---|---:|---:|---:|---:|
| small | 기록 | 기록 | 기록 | 기록 |
| base | 기록 | 기록 | 기록 | 기록 |

성능 차이가 작고 지연 차이가 크면 작은 모델이 서비스에 유리할 수 있습니다.

## 신뢰도 구간

최대 확률이 낮은 예측을 사람 검토로 보낼 수 있습니다. 임계값은 test가 아니라 validation에서 정하고, 검토율과 오류 감소를 함께 계산합니다.

## 도메인·시간 변화

신제품명이나 정책 용어가 등장하면 tokenizer 조각과 오류율이 변할 수 있습니다. 월별 F1을 항상 알 수 없다면 확률 분포, 입력 길이, OOV에 가까운 과도한 subword 분할을 관찰합니다.

## 배포 전 검증

- tokenizer와 model 같은 경로/리비전
- max length와 truncation 정책
- id2label과 업무 레이블 일치
- batch 1 및 batch 추론 결과
- CPU/GPU 수치 차이 허용 범위
- 저장 후 대표 입력 회귀 테스트

## 개인정보

문장 분류 로그에 고객 원문이 포함될 수 있습니다. 필요한 필드만 보존하고 ID를 가명화하며 접근·삭제 정책을 둡니다.

---

<!-- SOURCE: 00_비전공자_BERT_분류워크북.md -->

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

## Fine-tuning을 전학생 교육으로 비유하기

BERT는 이미 많은 글을 읽고 언어 감각을 익힌 전학생과 같습니다. Fine-tuning은 처음부터 글자를 가르치는 것이 아니라 “우리 회사 문의를 배송·환불·계정으로 구분하는 법”을 짧게 추가 교육하는 과정입니다.

## 분류 헤드의 계산

`[CLS]` 위치의 벡터를 문장 요약으로 사용하고 클래스별 점수를 만듭니다.

\[
z=h_{CLS}W+b,\qquad p=softmax(z)
\]

`h_CLS`가 768차원, 클래스가 3개면 `W`는 `(768,3)`, 로짓은 샘플마다 3개입니다. 로짓 `[2,1,0]`을 Softmax로 바꾸면 약 `[0.67,0.24,0.09]`입니다.

## 낮은 학습률을 쓰는 이유

사전학습 가중치를 너무 크게 바꾸면 이미 배운 언어 표현이 손상될 수 있습니다. 그래서 새로 만든 작은 모델보다 낮은 학습률에서 시작합니다. 정확한 값은 데이터와 모델에 따라 validation으로 결정합니다.

## 전체 층을 학습할까?

- 전체 Fine-tuning: 모든 BERT 가중치와 분류층을 갱신
- 일부 freeze: 아래쪽 층을 고정하고 위쪽만 갱신
- 분류층만 학습: 빠르지만 업무 표현 적응이 제한될 수 있음

데이터가 매우 작을 때 일부 고정이 안정적일 수 있지만 항상 성능이 좋아지는 것은 아닙니다.

## 데이터 누수 방지

같은 뉴스의 제목과 본문, 동일 고객의 반복 문의, 문구 일부만 바뀐 중복 문장이 train과 test에 나뉘지 않게 합니다. 랜덤 분할보다 문서·고객·시간 단위 분할이 필요한지 검토합니다.

## 최대 길이 결정

무조건 512를 쓰면 짧은 문장 데이터에서 메모리를 낭비합니다. 토큰 길이 분포를 보고 95~99백분위 후보를 정합니다. 잘린 샘플 중 중요한 정보가 뒤에 있는지 직접 확인합니다.

## 평가에서 볼 것

전체 Accuracy뿐 아니라 클래스별 Precision, Recall, F1, 혼동 행렬을 봅니다. 클래스가 불균형하면 macro F1이 모든 클래스를 동일한 비중으로 보여 줍니다.

## 오류 분석 예

“배송은 빨랐지만 환불하고 싶어요”가 배송으로 분류됐다면 첫 키워드에 과도하게 의존했을 수 있습니다. 반전·복합 의도·긴 문장·고유명사로 오류 유형을 나눠 다음 데이터 수집 방향을 정합니다.

---

<!-- SOURCE: 03_Summary_and_Quiz.md -->

# 퀴즈
1. BERT의 기본 backbone은? **Transformer encoder**
2. MLM의 목표는? **가려진 token 예측**
3. 모든 BERT 계열이 NSP를 쓰나요? **아니요**
4. tokenizer와 model checkpoint를 맞춰야 하는 이유는? **어휘·special token ID 불일치 방지**
5. 긴 문장 처리 시 기록할 값은? **truncation 비율과 max_length**
6. Fine-tuning에서 보통 작은 learning rate를 쓰는 이유는? **사전학습 표현의 급격한 손상 완화**

---

<!-- SOURCE: 04_Practice.md -->

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
