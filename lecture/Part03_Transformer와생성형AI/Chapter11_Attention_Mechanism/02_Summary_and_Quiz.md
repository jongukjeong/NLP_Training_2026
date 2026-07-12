# 요약과 퀴즈

1. Attention이 완화한 Seq2Seq 병목은? **고정 context 압축**
2. Bahdanau 방식은 additive인가요? **예**
3. Luong의 대표 score는? **dot product 계열**
4. Self Attention의 Q/K/V는 어디서 오나요? **같은 sequence 표현**
5. `sqrt(d_k)`로 나누는 이유는? **큰 dot product와 softmax 포화 완화**
6. causal mask의 목적은? **미래 token 참조 차단**
7. attention weight를 인간 설명과 동일시해도 되나요? **아니요**

## 비전공자를 위한 핵심 정리

Attention은 긴 문장을 한 번에 외우는 대신, 답을 만들 때마다 원문에서 관련 부분을 다시 찾아보는 방법입니다. 번역 중 “그것”을 번역해야 한다면 원문의 여러 단어 중 무엇을 가리키는지 점수를 매겨 참고합니다.

### 세 가지 이름만 기억하기

- Query: 지금 알고 싶은 것, 즉 검색어
- Key: 각 정보에 붙은 색인표
- Value: 실제로 꺼내 사용할 내용

Query와 Key를 비교해 점수를 만들고, Softmax로 비율을 구한 뒤 Value를 비율만큼 섞습니다.

\[
문맥=0.2\times정보A+0.7\times정보B+0.1\times정보C
\]

이 예에서는 정보 B를 가장 많이 참고합니다. 비율의 합은 1이므로 “전체 관심을 어디에 얼마나 나누었나”로 이해할 수 있습니다.

## Attention과 사람의 주의력은 같은가?

이름은 비슷하지만 모델의 Attention은 행렬 계산입니다. 사람이 의식적으로 집중하는 현상과 동일하지 않습니다. heatmap에서 색이 진한 토큰은 계산상 가중치가 컸다는 뜻이며, 모델 판단의 모든 이유를 설명하지는 않습니다.

## Self-Attention과 일반 Attention

Self-Attention은 같은 문장 안에서 토큰끼리 서로 참고합니다. Cross-Attention은 번역문의 현재 상태가 원문 토큰을 참고합니다. “누가 누구를 보는가”를 확인하면 두 개념을 쉽게 구분할 수 있습니다.

## 자주 틀리는 지점

1. Attention 가중치와 모델의 최종 확률은 다릅니다.
2. padding 위치는 계산 전에 가려야 합니다.
3. Softmax를 적용하는 축이 Key 위치축인지 확인합니다.
4. 시각화할 때 subword 토큰을 원 단어와 혼동하지 않습니다.

## 짧은 확인 문제

1. Query를 인터넷 검색에 비유하면 무엇입니까?
2. 가중치 `[0.3, 0.7]`, 값 `[10, 20]`의 가중합은 얼마입니까?
3. Attention heatmap이 완전한 원인 설명이 아닌 이유는 무엇입니까?
4. Self-Attention과 Cross-Attention의 차이를 한 문장으로 말해 보세요.
5. padding 토큰의 가중치는 왜 0이어야 합니까?
