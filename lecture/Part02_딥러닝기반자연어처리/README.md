# Part 2. 딥러닝 기반 자연어처리

Part 2는 TensorFlow와 Keras로 신경망의 학습 원리를 익히고, MLP에서 RNN·LSTM/GRU·Encoder-Decoder로 확장합니다.

## 구성

- [Chapter 6. TensorFlow와 Keras](Chapter06_TensorFlow와Keras/README.md)
- [Chapter 7. 딥러닝 기초](Chapter07_딥러닝기초/README.md)
- [Chapter 8. 순환신경망(RNN)](Chapter08_순환신경망_RNN/README.md)
- [Chapter 9. LSTM과 GRU](Chapter09_LSTM과GRU/README.md)
- [Chapter 10. Seq2Seq와 Encoder-Decoder](Chapter10_Seq2Seq와Encoder_Decoder/README.md)

## 환경

Python 3.11 가상환경에서 Part 2 전용 패키지를 설치합니다.

```powershell
python -m pip install -r lecture\Part02_딥러닝기반자연어처리\requirements.txt
```

교육용 데이터셋은 각 실습 코드와 같은 폴더에 있습니다. 학습 결과는 해당 폴더의 `output/`에 생성됩니다.

## 공통 원칙

- 학습·검증·테스트 데이터를 분리한다.
- 전처리 계층은 학습 데이터에만 `adapt()`한다.
- 시드, 라이브러리 버전, 모델 설정과 평가 결과를 기록한다.
- 정확도 하나만 보지 않고 손실, 클래스 분포와 오분류를 확인한다.
- 작은 교육 데이터의 성능을 운영 품질로 해석하지 않는다.
