# 20.3 모델 개발

기준선은 문자 n-gram TF-IDF와 cosine similarity입니다. 한국어 띄어쓰기와 일부 표현 변화에 견고하고 API 없이 재현할 수 있습니다.

```text
query → vectorize → top-k documents → threshold
→ evidence + source → optional LLM generation
```

향후 확장:

- embedding retriever
- lexical+vector hybrid와 RRF
- reranker
- metadata filter와 접근권한
- query rewriting

각 변경은 같은 평가셋에서 retrieval metric과 latency를 비교합니다. generation 개선으로 retrieval 실패를 숨기지 않습니다.

## 기준선 먼저 만들기

분류는 다수 클래스·TF-IDF, 검색은 키워드·TF-IDF, 생성은 고정 Prompt처럼 단순한 기준선을 만듭니다.

## 실험 계획

가설, 변경 한 가지, 고정 조건, 성공 기준을 실험 전에 씁니다. Test 결과를 보고 하이퍼파라미터를 선택하지 않습니다.

## 실험 기록

```text
experiment_id,git_commit,data_version,model,prompt,metric,latency,cost,conclusion
```

## 평가

전체 평균 외에 클래스·길이·언어 현상·권한별 하위 결과를 봅니다. 실제 실패 문장을 최소 20개 분류합니다.

## 모델 선택

품질이 약간 높지만 비용·지연이 크게 증가한 모델과 실용적인 작은 모델을 함께 비교합니다. 최종 선택 근거를 숫자로 작성합니다.

## 산출물

기준선, 실험표, 최고 모델, 재현 명령, 평가 결과, 오류 분석과 모델 카드를 제출합니다.
