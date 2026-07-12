# Chapter 3. 텍스트 전처리


## 핵심 용어 미리보기

본문을 읽기 전에 다음 용어의 뜻과 영어 원어를 먼저 확인합니다. 전체 정의는 [교육과정 핵심 용어집](../../TERMINOLOGY.md)에서 확인할 수 있습니다.

- **정규표현식(Regular Expression): 문자열 패턴을 찾고 바꾸기 위한 표현 규칙**
- **유니코드(Unicode): 여러 언어의 문자를 일관된 번호로 표현하는 표준**
- **정규화(Normalization): 서로 다른 문자·공백 표기를 일정한 기준으로 맞추는 처리**
- **토큰화(Tokenization): 문장을 모델이 처리할 작은 단위로 나누는 과정**

텍스트 전처리는 원문을 무조건 짧고 단순하게 만드는 작업이 아니라, **분석 목적에 맞는 정보를 보존하면서 표현의 불일치를 줄이는 과정**입니다. 이 장은 Python 기본 문법을 전제로 정규표현식, Unicode 정규화, 토큰화, 한국어 처리와 품질 검증을 다룹니다.

## 학습 목표

- 전처리 목적과 정보 손실 위험을 설명한다.
- 정규표현식으로 URL, 이메일, 전화번호와 반복 문자를 탐지·치환한다.
- Unicode와 공백을 일관된 형식으로 정규화한다.
- 어절·문장·형태소·서브워드 토큰화의 차이를 구분한다.
- 한국어 조사·어미·띄어쓰기 특성을 고려해 도구를 선택한다.
- 처리 전후 통계와 표본 비교로 전처리 품질을 검증한다.

## 선수 지식

변수, 조건문, 반복문, 함수 등 Python 기본 문법과 Chapter 2의 CSV·pandas 처리를 알고 있다고 가정합니다.

## 문서 구성

1. [전처리 설계 원칙](01_Opening.md)
2. [정규표현식 기반 정제](02_Regular_Expressions.md)
3. [Unicode와 텍스트 정규화](03_Normalization.md)
4. [토큰화](04_Tokenization.md)
5. [한국어 전처리와 형태소 분석](05_Korean_Preprocessing.md)
6. [핵심 정리](06_Summary.md)
7. [퀴즈](07_Quiz.md)
8. [실습 과제](08_Assignment.md)
9. [미니 프로젝트](09_Mini_Project.md)

## 배포 자료 구조

```text
Chapter03_텍스트전처리/
├── 08_Assignment.md
├── 09_Mini_Project.md
└── examples/
    ├── 08_assignment_solution/
    └── 09_mini_project_solution/
```

각 솔루션의 코드와 입력 데이터셋은 같은 폴더에 있으며, 실행 결과만 `output/`에 생성됩니다.
