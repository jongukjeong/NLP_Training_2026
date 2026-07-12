# 번역 모델 설계와 평가

데이터 split 전에 동일·유사 번역쌍을 그룹화해 누수를 방지합니다. source와 target 언어의 vocabulary, 시작·종료·padding token ID를 저장해야 inference를 재현할 수 있습니다.

평가:

- validation loss
- exact match(교육용 짧은 문장)
- BLEU/chrF 같은 자동 지표
- 의미 보존, 유창성, 누락·추가에 대한 사람 평가

자동 지표 하나만으로 번역 품질을 결론 내리지 않습니다. 이름·숫자·부정 표현과 도메인 용어를 별도 검사합니다.

실무 번역은 Transformer와 사전학습 모델이 일반적이지만 Encoder-Decoder와 decoding 개념은 이후 구조의 기반입니다.
