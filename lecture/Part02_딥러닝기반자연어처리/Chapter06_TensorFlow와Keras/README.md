# Chapter 6. TensorFlow와 Keras


## 핵심 용어 미리보기

본문을 읽기 전에 다음 용어의 뜻과 영어 원어를 먼저 확인합니다. 전체 정의는 [교육과정 핵심 용어집](../../TERMINOLOGY.md)에서 확인할 수 있습니다.

- **텐서(Tensor): 딥러닝 계산에 사용하는 다차원 숫자 배열**
- **배치(Batch): 한 번의 계산에서 함께 처리하는 데이터 묶음**
- **로짓(Logit): Sigmoid·Softmax로 확률을 만들기 전 클래스별 원점수**
- **잔차 연결(Residual Connection): 원래 입력을 변환 결과에 다시 더하는 연결**
- **에포크(Epoch): 전체 학습 데이터를 한 번 모두 사용한 단위**

## 학습 목표

- Tensor의 shape, dtype, axis를 해석한다.
- `tf.data.Dataset`으로 shuffle, batch, prefetch 파이프라인을 만든다.
- Sequential API와 Functional API의 선택 기준을 설명한다.
- `compile`, `fit`, `evaluate`, `predict`의 역할을 구분한다.
- callback과 `.keras` 형식으로 학습 결과를 관리한다.

## 구성

1. [Tensor와 Dataset](01_Tensor_and_Dataset.md)
2. [Sequential과 Functional API](02_Keras_APIs.md)
3. [모델 학습](03_Model_Training.md)
4. [퀴즈](04_Summary_and_Quiz.md)
5. [실습: 첫 번째 딥러닝 모델](05_Practice.md)

> 공식 기준: Keras의 내장 학습 루프는 Sequential, Functional, subclass 모델에서 같은 방식으로 사용할 수 있습니다.

## 먼저 읽을 상세 가이드

- [원리·수학·실습 연결 가이드](00_원리_수학_실습_가이드.md): 직관, 핵심 공식, 수치 예, 구현 점검을 한 흐름으로 학습합니다.
