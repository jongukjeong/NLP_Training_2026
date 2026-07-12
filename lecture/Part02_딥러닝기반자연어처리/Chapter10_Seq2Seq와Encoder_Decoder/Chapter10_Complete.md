# Chapter 10. Seq2Seq와 Encoder-Decoder — 통합 원고

> 이 문서는 Chapter 10. Seq2Seq와 Encoder-Decoder 의 최상위 강의 마크다운을 학습 순서대로 합친 통합 원고입니다. 개별 원본 파일은 그대로 유지합니다.

## 통합 목차

- Chapter 10. Seq2Seq와 Encoder-Decoder — `README.md`
- 10.1 Seq2Seq · 10.2 Encoder · 10.3 Decoder — `01_Seq2Seq_Architecture.md`
- 10.4 Teacher Forcing — `02_Teacher_Forcing.md`
- 10.5 Beam Search — `03_Beam_Search.md`
- 번역 모델 설계와 평가 — `04_Translation_Evaluation.md`
- 요약과 퀴즈 — `05_Summary_and_Quiz.md`
- 실습: 번역 모델 구현 — `06_Practice.md`

---

<!-- SOURCE: README.md -->

# Chapter 10. Seq2Seq와 Encoder-Decoder

# Chapter 10. Seq2Seq와 Encoder-Decoder

1. [Seq2Seq·Encoder·Decoder](01_Seq2Seq_Architecture.md)
2. [Teacher Forcing](02_Teacher_Forcing.md)
3. [Beam Search](03_Beam_Search.md)
4. [번역 모델 설계와 평가](04_Translation_Evaluation.md)
5. [요약과 퀴즈](05_Summary_and_Quiz.md)
6. [실습: 번역 모델 구현](06_Practice.md)

이 장은 교육용 문자 단위 번역 모델로 입력/출력 tensor와 inference loop를 이해합니다. 실제 번역 품질을 위한 규모의 모델이 아닙니다.


---

<!-- SOURCE: 01_Seq2Seq_Architecture.md -->

# 10.1 Seq2Seq · 10.2 Encoder · 10.3 Decoder

# 10.1 Seq2Seq · 10.2 Encoder · 10.3 Decoder

Seq2Seq는 입력 sequence를 출력 sequence로 변환합니다.

```text
입력 문장 → Encoder → context/state → Decoder → 출력 문장
```

Encoder RNN은 입력을 읽고 마지막 hidden/cell state를 Decoder 초기 상태로 전달합니다. Decoder는 시작 token에서 출발해 다음 token 분포를 반복 예측합니다.

학습 tensor:

- encoder input: `(batch, source_timesteps)`
- decoder input: `<START>`부터 마지막 직전 token
- decoder target: 첫 target token부터 `<END>`까지 한 칸 이동
- output logits/probabilities: `(batch, target_timesteps, target_vocab)`

고정 길이 context 하나에 모든 입력을 압축하는 기본 Seq2Seq는 긴 문장에서 병목이 생깁니다. Chapter 11의 Attention이 이를 완화합니다.


---

<!-- SOURCE: 02_Teacher_Forcing.md -->

# 10.4 Teacher Forcing

# 10.4 Teacher Forcing

Teacher Forcing은 학습 중 Decoder의 다음 입력으로 모델의 이전 예측 대신 정답 token을 제공합니다.

```text
decoder input : <START> 나 는 학생
decoder target: 나       는 학생 <END>
```

학습을 안정화하지만 inference에서는 정답이 없으므로 이전 예측을 다시 입력합니다. 이 차이를 exposure bias라고 합니다.

대응 방법으로 scheduled sampling 등을 검토할 수 있지만 교육 실습에서는 학습과 inference 경로의 차이를 명시하고 오류 누적을 관찰합니다.

padding token의 loss를 제외하려면 sample weight 또는 mask를 적용합니다. 그렇지 않으면 긴 padding을 맞히는 능력이 loss를 지배할 수 있습니다.


---

<!-- SOURCE: 03_Beam_Search.md -->

# 10.5 Beam Search

# 10.5 Beam Search

Greedy decoding은 각 단계에서 확률이 가장 높은 token 하나를 선택합니다. 빠르지만 초기에 내린 선택을 되돌릴 수 없습니다.

Beam Search는 상위 `beam_width`개의 부분 sequence를 유지합니다.

```text
각 후보 확장 → 누적 log probability 계산 → 상위 beam 유지 → 종료 조건 확인
```

확률을 곱하면 underflow가 발생하므로 log probability를 더합니다. 긴 문장이 불리해지는 문제를 줄이기 위해 length normalization을 사용하기도 합니다.

beam을 넓히면 계산량과 메모리가 증가하며 품질이 항상 향상되는 것은 아닙니다. 반복, 종료 실패와 문장 길이를 함께 평가합니다.


---

<!-- SOURCE: 04_Translation_Evaluation.md -->

# 번역 모델 설계와 평가

# 번역 모델 설계와 평가

데이터 split 전에 동일·유사 번역쌍을 그룹화해 누수를 방지합니다. source와 target 언어의 vocabulary, 시작·종료·padding token ID를 저장해야 inference를 재현할 수 있습니다.

평가:

- validation loss
- exact match(교육용 짧은 문장)
- BLEU/chrF 같은 자동 지표
- 의미 보존, 유창성, 누락·추가에 대한 사람 평가

자동 지표 하나만으로 번역 품질을 결론 내리지 않습니다. 이름·숫자·부정 표현과 도메인 용어를 별도 검사합니다.

실무 번역은 Transformer와 사전학습 모델이 일반적이지만 Encoder-Decoder와 decoding 개념은 이후 구조의 기반입니다.


---

<!-- SOURCE: 05_Summary_and_Quiz.md -->

# 요약과 퀴즈

# 요약과 퀴즈

1. Encoder의 출력 state는 어디에 사용되나요? **Decoder 초기 상태**
2. Decoder input과 target은 어떻게 다른가요? **한 timestep 이동**
3. Teacher Forcing은 학습 중 무엇을 다음 입력으로 사용하나요? **정답 token**
4. exposure bias란? **학습과 inference의 decoder 입력 차이로 인한 오류 누적 문제**
5. Greedy와 Beam Search의 차이는? **하나의 후보 대 여러 상위 후보 유지**
6. Beam Search에서 log probability를 쓰는 이유는? **곱셈 underflow 방지**
7. 기본 Seq2Seq의 고정 context 병목을 완화하는 다음 기술은? **Attention**


---

<!-- SOURCE: 06_Practice.md -->

# 실습: 번역 모델 구현

# 실습: 번역 모델 구현

짧은 영어-한국어 문자 단위 번역쌍으로 Encoder-Decoder를 학습하고 greedy inference 예제를 실행합니다.

- [안내](examples/06_translation_solution/README.md)
- [완성 코드](examples/06_translation_solution/seq2seq_translation.py)
- [데이터셋](examples/06_translation_solution/translations.csv)

실습 완료 후 tensor shape, teacher forcing용 shift, 시작·종료 token과 inference loop를 설명할 수 있어야 합니다.

