# 요약과 퀴즈

## 요약

Tensor → Dataset → Model → compile → fit → evaluate → save 순서로 첫 학습 파이프라인을 구성합니다.

## 퀴즈

1. Tensor의 세 가지 핵심 속성은 무엇인가요?
2. 학습 Dataset에서 shuffle을 batch보다 먼저 적용하는 이유는 무엇인가요?
3. 다중 입력 모델에 적합한 Keras API는 무엇인가요?
4. loss와 metric의 역할 차이는 무엇인가요?
5. EarlyStopping의 `restore_best_weights=True`는 무엇을 보존하나요?

## 정답

1. shape, dtype, rank입니다.
2. batch마다 데이터가 충분히 섞이도록 하기 위해서입니다.
3. Functional API입니다.
4. loss는 최적화 대상이고 metric은 평가·보고 지표입니다.
5. 검증 성능이 가장 좋았던 epoch의 가중치입니다.
