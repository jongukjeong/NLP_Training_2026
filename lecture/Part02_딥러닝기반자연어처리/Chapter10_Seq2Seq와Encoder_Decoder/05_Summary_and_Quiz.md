# 요약과 퀴즈

1. Encoder의 출력 state는 어디에 사용되나요? **Decoder 초기 상태**
2. Decoder input과 target은 어떻게 다른가요? **한 timestep 이동**
3. Teacher Forcing은 학습 중 무엇을 다음 입력으로 사용하나요? **정답 token**
4. exposure bias란? **학습과 inference의 decoder 입력 차이로 인한 오류 누적 문제**
5. Greedy와 Beam Search의 차이는? **하나의 후보 대 여러 상위 후보 유지**
6. Beam Search에서 log probability를 쓰는 이유는? **곱셈 underflow 방지**
7. 기본 Seq2Seq의 고정 context 병목을 완화하는 다음 기술은? **Attention**
