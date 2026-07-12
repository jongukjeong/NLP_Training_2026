# NLP Training 2026

자연어 처리를 실무 중심으로 학습하는 교육과정 저장소입니다.

## 저장소 원칙

- 강의 자료의 단일 원본은 `lecture/`에서 관리합니다.
- 각 Part 아래에 Chapter 디렉터리를 둡니다.
- 실습·미니 프로젝트 코드와 데이터셋은 해당 Chapter의 `examples/`에 둡니다.
- 실행 결과는 각 예제의 `output/`에 생성하며 Git에는 포함하지 않습니다.

## 현재 구성

```text
lecture/
└── Part01_자연어처리기초와Python/
    ├── Chapter01_인공지능과자연어처리의이해/
    │   ├── examples/
    │   ├── notebooks/
    │   ├── projects/
    │   └── images/
    ├── Chapter02_Python과데이터처리/
    │   └── examples/
    ├── Chapter03_텍스트전처리/
    │   └── examples/
    ├── Chapter04_텍스트의수치화/
    │   └── examples/
    └── Chapter05_단어임베딩/
        └── examples/
```

```text
lecture/
└── Part02_딥러닝기반자연어처리/
    ├── Chapter06_TensorFlow와Keras/
    ├── Chapter07_딥러닝기초/
    ├── Chapter08_순환신경망_RNN/
    ├── Chapter09_LSTM과GRU/
    └── Chapter10_Seq2Seq와Encoder_Decoder/
```

## 환경 준비

Python 3.11 가상환경에서 다음을 실행합니다.

```powershell
python -m pip install -r requirements.txt
```

각 Chapter의 `README.md`에서 학습 순서와 배포 자료 위치를 확인할 수 있습니다.
