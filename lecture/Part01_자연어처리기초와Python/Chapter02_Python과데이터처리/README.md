# Chapter 2. Python과 데이터 처리


## 핵심 용어 미리보기

본문을 읽기 전에 다음 용어의 뜻과 영어 원어를 먼저 확인합니다. 전체 정의는 [교육과정 핵심 용어집](../../TERMINOLOGY.md)에서 확인할 수 있습니다.

- **데이터셋(Dataset): 분석·학습에 사용하는 데이터 묶음**
- **데이터프레임(DataFrame): 행과 열로 구성된 표 형태의 데이터 구조**
- **스키마(Schema): 열 이름·자료형·필수 여부처럼 데이터가 지켜야 할 구조**
- **결측값(Missing Value): 값이 없거나 관측되지 않은 상태**

자연어 처리에서는 모델 학습 전에 **데이터를 읽고, 구조를 진단하고, 정제하고, 검증하여 다시 저장하는 과정**이 필요합니다. 이 장은 비전공자도 따라올 수 있도록 짧은 코드부터 시작하고, 같은 작업을 점차 실무적인 구조로 확장합니다.

## 학습 목표

이 장을 마치면 다음을 할 수 있습니다.

- 텍스트, CSV, JSON 파일을 UTF-8로 안전하게 읽고 쓴다.
- pandas로 표 데이터를 탐색하고 결측값·중복·문자열을 정제한다.
- 데이터 스키마와 정제 결과를 검증한다.
- 처리 전후 통계를 기록하는 작은 데이터 처리 프로그램을 완성한다.

## 선수 지식

별도의 Python 선수 지식 없이 시작할 수 있습니다. 변수, 문자열, 리스트, 조건문, 반복문과 간단한 함수는 이 Chapter의 `02~05` 문서에서 다시 학습합니다. 타입 힌트, 예외 처리와 CLI는 선택 확장입니다.

## 권장 학습 순서

```text
Python 기초 복습(02~05)
  → Step by Step(함께 따라 하기)
  → Basic Practice(짧은 전체 코드)
  → Assignment(개별 과제)
  → Assignment Solution(시도 후 해설)
  → Mini Project(종합 적용)
  → Mini Project Solution(피드백 후 공개)
```

solution은 정답 복사용 자료가 아니라 수강생 코드와 비교하는 해설 자료입니다. 강사는 다수의 수강생이 기본 요구사항을 시도한 뒤 공개합니다.

## 문서 구성

1. [학습 안내](01_Opening.md)
2. [Python 실행과 기본 문법](02_Python_Basics.md)
3. [문자열과 컬렉션](03_Strings_and_Collections.md)
4. [조건문과 반복문](04_Control_Flow.md)
5. [함수와 모듈](05_Functions_and_Modules.md)
6. [파일·CSV·JSON 처리](06_File_IO.md)
7. [pandas로 표 데이터 다루기](07_Pandas.md)
8. [텍스트 데이터 정제와 검증](08_Data_Cleaning.md)
9. [Step by Step](examples/01_step_by_step/README.md)
10. [Basic Practice](examples/02_basic_practice/README.md)
11. [핵심 정리](09_Summary.md)
12. [퀴즈](10_Quiz.md)
13. [실습 과제](11_Assignment.md)
14. [미니 프로젝트: 텍스트 데이터 탐색기](12_Mini_Project.md)

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
    ├── 01_step_by_step/             # 강사와 함께 실행
    ├── 02_basic_practice/            # 입문용 통합 실습
    ├── 11_assignment_solution/
    │   ├── assignment_solution.py
    │   └── customer_inquiries.csv
    ├── 12_mini_project_starter/      # 수강생 시작 코드
    └── 12_mini_project_solution/     # 피드백 후 공개
        ├── text_data_explorer.py
        └── reviews.csv
```

실행 결과는 원본과 섞이지 않도록 같은 폴더 아래 `output/`에 저장합니다.

> 예제는 Windows PowerShell 기준 명령도 함께 제시하지만, Python 코드는 운영체제와 무관하게 실행되도록 작성합니다.

## 완료 기준

- 변수·리스트·조건문·반복문·간단한 함수 예제를 직접 수정
- Step by Step에서 각 단계 후 행 수가 달라진 이유를 설명
- Basic Practice의 입력 파일과 저장 파일을 바꿔 실행
- 퀴즈 8문항 중 6문항 이상 정답
- 실습 과제의 기본 요구사항 완료
- 미니 프로젝트에서 읽기·정제·저장 흐름 완료

파일 검사, 사용자 정의 오류, CLI, JSON 보고서는 빠른 학습자를 위한 선택 목표입니다.

다음 장에서는 이 장에서 준비한 텍스트 데이터를 바탕으로 정규표현식과 형태소 분석 등 본격적인 텍스트 전처리를 학습합니다.
