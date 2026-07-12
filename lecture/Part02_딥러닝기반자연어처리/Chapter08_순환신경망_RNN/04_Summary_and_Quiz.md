# 요약과 퀴즈

1. RNN의 state는 무엇을 요약하나요? **이전 timestep까지의 정보**
2. Embedding 입력 shape는? **batch, timesteps**
3. `mask_zero=True`의 목적은? **0 padding 무시 지원**
4. BPTT는 어느 방향으로 gradient를 계산하나요? **시간축을 거슬러 역전파**
5. clipnorm이 주로 완화하는 문제는? **exploding gradient**
6. `return_sequences=True`가 필요한 경우는? **후속 layer가 전체 timestep 출력을 사용할 때**
