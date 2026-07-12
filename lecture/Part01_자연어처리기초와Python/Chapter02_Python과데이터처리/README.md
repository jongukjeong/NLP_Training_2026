# Chapter 2. Python과 데이터 처리

자연어 처리에서는 모델 학습 전에 **데이터를 읽고, 구조를 진단하고, 정제하고, 검증하여 다시 저장하는 과정**이 필요합니다. 이 장은 Python 기본 문법을 이미 알고 있다는 전제에서 실제 텍스트 데이터 처리에 집중합니다.

## 학습 목표

이 장을 마치면 다음을 할 수 있습니다.

- 텍스트, CSV, JSON 파일을 UTF-8로 안전하게 읽고 쓴다.
- pandas로 표 데이터를 탐색하고 결측값·중복·문자열을 정제한다.
- 데이터 스키마와 정제 결과를 검증한다.
- 처리 전후 통계를 기록하는 작은 데이터 처리 프로그램을 완성한다.

## 선수 지식

변수, 기본 자료형, 조건문, 반복문, 함수 등 Python 기본 문법은 이 장에서 별도로 설명하지 않습니다. 필요한 코드는 데이터 처리 맥락의 완성 예제로 제공합니다.

## 문서 구성

1. [학습 안내](01_Opening.md)
2. [파일·CSV·JSON 처리](06_File_IO.md)
3. [pandas로 표 데이터 다루기](07_Pandas.md)
4. [텍스트 데이터 정제와 검증](08_Data_Cleaning.md)
5. [핵심 정리](09_Summary.md)
6. [퀴즈](10_Quiz.md)
7. [실습 과제](11_Assignment.md)
8. [미니 프로젝트: 텍스트 데이터 탐색기](12_Mini_Project.md)

## 실습 환경

- Python 3.11.x
- VS Code 또는 JupyterLab
- pandas 2.x
- 모든 텍스트 파일의 기본 인코딩: UTF-8

## 예제 파일 배치 규칙

각 예제의 Python 코드와 그 코드가 사용하는 데이터셋은 **동일한 예제 폴더**에 둡니다.

```text
Chapter02_Python과데이터처리/
├── 11_Assignment.md
├── 12_Mini_Project.md
└── examples/
    ├── 11_assignment_solution/
    │   ├── assignment_solution.py
    │   └── customer_inquiries.csv
    └── 12_mini_project_solution/
        ├── text_data_explorer.py
        └── reviews.csv
```

실행 결과는 원본과 섞이지 않도록 같은 폴더 아래 `output/`에 저장합니다.

> 예제는 Windows PowerShell 기준 명령도 함께 제시하지만, Python 코드는 운영체제와 무관하게 실행되도록 작성합니다.

## 완료 기준

- 퀴즈 8문항 중 6문항 이상 정답
- 실습 과제의 필수 항목 완료
- 미니 프로젝트가 정상 데이터와 잘못된 입력 모두를 처리
- 출력 결과에 원본 행 수, 정제 행 수, 결측·중복 제거 수가 기록됨

다음 장에서는 이 장에서 준비한 텍스트 데이터를 바탕으로 정규표현식과 형태소 분석 등 본격적인 텍스트 전처리를 학습합니다.
