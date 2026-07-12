# 실습 환경 구축

> **Chapter 1. 인공지능과 자연어처리의 이해**  
> 문서: `07_Lab_Setup.md`

---

## 시작 질문

이제 우리는 인공지능, 머신러닝, 자연어처리, 생성형 AI, LLM의 큰 그림을 살펴보았습니다.

하지만 AI를 제대로 배우려면 설명을 듣는 것만으로는 부족합니다.

직접 코드를 실행하고,  
오류를 만나고,  
수정하고,  
다시 실행해 보아야 합니다.

이번 문서에서는 앞으로의 실습을 위한 개발환경을 준비합니다.

여기서 중요한 질문은 이것입니다.

> **AI와 자연어처리 실습을 안정적으로 따라가기 위해 어떤 환경이 필요할까?**

---

## 개발환경이 중요한 이유

AI 실습에서는 개발환경이 매우 중요합니다.

일반적인 Python 코드보다 AI 관련 코드는 라이브러리 의존성이 복잡한 경우가 많습니다.

예를 들어 다음 요소들이 서로 영향을 줍니다.

- Python 버전
- 패키지 버전
- 운영체제
- GPU 사용 여부
- CUDA 버전
- 딥러닝 프레임워크 버전
- Jupyter 실행 환경
- 데이터 파일 경로
- API Key 관리 방식
- 문서 저장 방식
- 벡터 검색 도구

환경이 맞지 않으면 같은 코드도 어떤 컴퓨터에서는 실행되고, 어떤 컴퓨터에서는 실행되지 않을 수 있습니다.

그래서 이 과정에서는 처음부터 다음 원칙을 가지고 진행합니다.

> **최신 기술보다 검증된 기술을 우선한다.**  
> **학생이 검색 가능한 환경을 우선한다.**  
> **재현 가능한 실습 환경을 만든다.**

---

## 이번 과정의 표준 환경

이번 과정에서는 다음 환경을 기본으로 사용합니다.

| 항목 | 표준 |
|---|---|
| Python | Python 3.11 |
| 패키지 관리 | venv + pip |
| 코드 편집기 | Visual Studio Code |
| 버전 관리 | Git |
| 실습 노트북 | Jupyter Notebook / JupyterLab |
| 클라우드 실습 | Google Colab |
| 딥러닝 프레임워크 | PyTorch 중심 |
| NLP 라이브러리 | Hugging Face Transformers |
| 웹 API | FastAPI |
| 데모 UI | Streamlit |
| 기본 데이터 저장 | SQLite |
| 일반 관계형 DB 비교 | MySQL은 비교 설명용 |
| 벡터 검색 | ChromaDB 중심 |
| 고급 벡터 검색 | FAISS 소개 |
| 배포/재현성 | Docker |
| 문서화 | MkDocs Material |

모든 도구를 처음부터 한꺼번에 사용하지는 않습니다.

초반에는 Python, VS Code, Git, Jupyter 정도만 사용합니다.

SQLite는 간단한 데이터 저장과 키워드 검색의 한계를 이해할 때 사용합니다.

ChromaDB는 후반부 RAG 실습에서 의미 기반 검색을 구현할 때 사용합니다.

Docker, FastAPI, Streamlit, Vector DB는 후반부 프로젝트에서 단계적으로 사용합니다.

---

## 왜 Python 3.11인가?

Python은 AI와 데이터 분석 분야에서 가장 널리 사용되는 언어입니다.

그중에서도 이 과정에서는 **Python 3.11**을 기준으로 합니다.

이유는 다음과 같습니다.

| 이유 | 설명 |
|---|---|
| 안정성 | 많은 AI 라이브러리와 호환성이 좋다 |
| 검색 가능성 | 오류 해결 자료를 찾기 쉽다 |
| 성능 | 이전 버전보다 성능 개선이 있다 |
| 교육 재현성 | 학생들이 비슷한 환경을 구성하기 쉽다 |
| 실무 적합성 | 너무 오래된 버전도 아니고, 너무 최신 실험 버전도 아니다 |

Python 3.13처럼 더 최신 버전이 있을 수 있습니다.

하지만 AI 라이브러리는 최신 Python 버전을 바로 완벽히 지원하지 않는 경우가 있습니다.

반대로 Python 3.7처럼 오래된 버전은 현재 AI 생태계에서는 호환성 문제가 생길 수 있습니다.

따라서 이번 과정에서는 Python 3.11을 표준으로 사용합니다.

---

## 전체 설치 흐름

앞으로 실습 환경은 다음 순서로 준비합니다.

```text
Python 설치
    ↓
VS Code 설치
    ↓
Git 설치
    ↓
프로젝트 폴더 생성
    ↓
가상환경 생성
    ↓
필수 패키지 설치
    ↓
Jupyter 실행
    ↓
Colab 사용법 확인
    ↓
SQLite로 간단한 데이터 저장 실습
    ↓
후반부에서 ChromaDB 기반 벡터 검색 도입
    ↓
Docker는 후반부 프로젝트에서 도입
```

이 순서를 따르면 처음부터 너무 많은 도구에 압도되지 않고 차근차근 실습 환경을 준비할 수 있습니다.

---

## 로컬 환경과 Colab 환경

AI 실습은 크게 두 가지 환경에서 진행할 수 있습니다.

| 환경 | 장점 | 단점 |
|---|---|---|
| 로컬 환경 | 내 컴퓨터에서 자유롭게 작업 가능 | 설치와 환경 문제가 생길 수 있음 |
| Colab 환경 | 설치 부담이 적고 GPU 사용 가능 | 파일 관리와 장기 프로젝트에는 불편할 수 있음 |

이 과정에서는 두 환경을 모두 사용합니다.

초반에는 로컬 환경에서 Python과 Git에 익숙해지고,  
GPU가 필요한 실습이나 빠른 데모는 Colab을 활용합니다.

후반 프로젝트에서는 로컬 환경과 Docker를 사용해 실제 서비스 구조에 가깝게 구성합니다.

---

## Python 설치 확인

Python을 설치한 뒤 터미널에서 다음 명령어를 실행합니다.

### macOS / Linux

```bash
python3 --version
```

### Windows

```bash
python --version
```

또는 다음 명령어를 사용할 수도 있습니다.

```bash
py --version
```

정상적으로 설치되었다면 다음과 비슷한 결과가 나옵니다.

```text
Python 3.11.x
```

여기서 `x`는 세부 패치 버전입니다.

중요한 것은 앞의 두 숫자가 `3.11`인지 확인하는 것입니다.

---

## pip 확인

pip는 Python 패키지를 설치하는 도구입니다.

다음 명령어로 확인할 수 있습니다.

### macOS / Linux

```bash
python3 -m pip --version
```

### Windows

```bash
python -m pip --version
```

pip는 단독으로 실행하기보다 `python -m pip` 형태로 실행하는 것이 안전합니다.

이 방식은 현재 사용 중인 Python 환경에 연결된 pip를 실행하기 때문입니다.

---

## VS Code 설치

VS Code는 이번 과정에서 사용할 기본 코드 편집기입니다.

VS Code를 사용하는 이유는 다음과 같습니다.

- 무료로 사용할 수 있다.
- Python 개발에 필요한 확장 기능이 많다.
- Jupyter Notebook도 열 수 있다.
- Git 연동이 편리하다.
- 학생들이 오류 해결 자료를 검색하기 쉽다.

VS Code를 설치한 뒤 다음 확장을 설치합니다.

| 확장 | 용도 |
|---|---|
| Python | Python 코드 실행 |
| Jupyter | Notebook 실행 |
| Pylance | Python 코드 분석 |
| GitLens | Git 작업 보조 |
| Markdown All in One | Markdown 작성 보조 |

모든 확장을 한꺼번에 완벽히 이해할 필요는 없습니다.

처음에는 Python과 Jupyter 확장만 있어도 충분합니다.

---

## Git 설치

Git은 코드와 문서를 버전 관리하기 위한 도구입니다.

이번 과정에서는 Git을 사용해 실습 파일과 강의 자료의 변경 이력을 관리합니다.

Git을 사용하는 이유는 다음과 같습니다.

- 실습 코드의 변경 이력을 남길 수 있다.
- 실수했을 때 이전 상태로 되돌릴 수 있다.
- 프로젝트를 체계적으로 관리할 수 있다.
- 나중에 GitHub에 업로드하기 쉽다.
- 협업 프로젝트의 기본 도구이다.

설치 후 다음 명령어로 확인합니다.

```bash
git --version
```

정상적으로 설치되었다면 다음과 비슷한 결과가 나옵니다.

```text
git version 2.x.x
```

---

## Git 기본 설정

Git 설치 후 처음 한 번은 사용자 이름과 이메일을 설정합니다.

```bash
git config --global user.name "Your Name"
git config --global user.email "your_email@example.com"
```

설정이 잘 되었는지 확인하려면 다음 명령어를 사용합니다.

```bash
git config --global --list
```

예시는 다음과 같습니다.

```text
user.name=Your Name
user.email=your_email@example.com
```

이 정보는 커밋 기록에 사용됩니다.

---

## 프로젝트 폴더 생성

이번 과정의 로컬 프로젝트 이름은 다음과 같이 사용합니다.

```text
NLP-Training-2026
```

터미널에서 원하는 위치로 이동한 뒤 폴더를 만듭니다.

```bash
mkdir NLP-Training-2026
cd NLP-Training-2026
```

Git 저장소로 초기화합니다.

```bash
git init
```

이제 이 폴더는 Git으로 관리되는 프로젝트 폴더가 됩니다.

---

## 권장 디렉터리 구조

이번 과정의 기본 디렉터리 구조는 다음과 같습니다.

```text
NLP-Training-2026/
├── README.md
├── requirements.txt
├── environment.yml
├── pyproject.toml
├── mkdocs.yml
├── lecture/
│   └── Part01_자연어처리기초와Python/
│       └── Chapter01_인공지능과자연어처리의이해/
│           ├── README.md
│           ├── 01_Opening.md
│           ├── 02_AI_History.md
│           ├── 03_Machine_Learning.md
│           ├── 04_NLP.md
│           ├── 05_Generative_AI_and_LLM.md
│           ├── 06_NLP_Cases.md
│           ├── 07_Lab_Setup.md
│           ├── images/
│           ├── examples/
│           ├── notebooks/
│           └── slides/
├── notebooks/
├── examples/
├── datasets/
├── exercises/
├── quizzes/
├── assignments/
├── projects/
└── assets/
```

강의 본문은 `lecture/` 아래에 둡니다.

실습 코드는 `examples/`, 노트북은 `notebooks/`, 데이터는 `datasets/`에 둡니다.

---

## 가상환경이란 무엇인가?

Python 프로젝트를 진행할 때는 가상환경을 사용하는 것이 좋습니다.

가상환경은 프로젝트마다 독립된 Python 패키지 공간을 만들어 주는 기능입니다.

예를 들어 A 프로젝트에서는 `numpy 1.x`가 필요하고,  
B 프로젝트에서는 `numpy 2.x`가 필요할 수 있습니다.

하나의 전역 환경에 모두 설치하면 충돌이 생길 수 있습니다.

가상환경을 사용하면 프로젝트마다 필요한 패키지를 따로 관리할 수 있습니다.

```text
프로젝트 A
    └── 전용 Python 패키지 환경

프로젝트 B
    └── 전용 Python 패키지 환경
```

이번 과정에서는 Python 기본 가상환경 도구인 `venv`를 먼저 사용합니다.

---

## 가상환경 생성

프로젝트 폴더 안에서 다음 명령어를 실행합니다.

### macOS / Linux

```bash
python3.11 -m venv .venv
```

또는 Python 명령어가 3.11을 가리키고 있다면 다음처럼 실행할 수 있습니다.

```bash
python3 -m venv .venv
```

### Windows

```bash
python -m venv .venv
```

명령어를 실행하면 `.venv` 폴더가 생성됩니다.

이 폴더 안에는 현재 프로젝트에서 사용할 Python 실행 환경과 패키지들이 들어갑니다.

---

## 가상환경 활성화

가상환경을 생성한 뒤에는 활성화해야 합니다.

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

### Windows Command Prompt

```cmd
.venv\Scripts\activate.bat
```

활성화되면 터미널 앞에 다음과 같이 표시될 수 있습니다.

```text
(.venv)
```

이 표시가 보이면 현재 프로젝트의 가상환경 안에서 작업하고 있다는 뜻입니다.

---

## 가상환경 비활성화

가상환경을 종료하려면 다음 명령어를 사용합니다.

```bash
deactivate
```

실습 중에는 가상환경이 활성화된 상태에서 패키지를 설치하고 코드를 실행하는 습관을 들이는 것이 좋습니다.

---

## requirements.txt

`requirements.txt`는 프로젝트에 필요한 Python 패키지 목록을 적어두는 파일입니다.

예를 들어 다음과 같이 작성할 수 있습니다.

```text
numpy
pandas
matplotlib
scikit-learn
jupyterlab
```

설치할 때는 다음 명령어를 사용합니다.

```bash
python -m pip install -r requirements.txt
```

이 파일이 있으면 다른 사람도 같은 패키지를 쉽게 설치할 수 있습니다.

---

## 초반 실습용 패키지

Chapter 1과 Part 1 초반에서는 너무 무거운 딥러닝 패키지를 바로 설치하지 않아도 됩니다.

초반에는 다음 정도면 충분합니다.

```text
numpy
pandas
matplotlib
scikit-learn
jupyterlab
ipykernel
```

설치 명령어는 다음과 같습니다.

```bash
python -m pip install numpy pandas matplotlib scikit-learn jupyterlab ipykernel
```

나중에 딥러닝과 Transformer를 다룰 때 PyTorch, Transformers 등을 추가로 설치합니다.

---

## 후반 RAG 실습용 패키지

RAG 프로젝트 단계에서는 다음 패키지들이 추가될 수 있습니다.

```text
chromadb
sentence-transformers
faiss-cpu
fastapi
uvicorn
streamlit
python-dotenv
```

다만 이 패키지들은 처음부터 설치하지 않습니다.

교육 초반에는 환경 구성을 단순하게 유지하고,  
RAG를 구현하는 시점에 필요한 패키지만 추가합니다.

---

## pip 업그레이드

가상환경을 만든 뒤 pip를 업그레이드할 수 있습니다.

```bash
python -m pip install --upgrade pip
```

다만 교육 현장에서는 모든 학생의 환경이 다르기 때문에,  
무조건 최신으로 올리는 것보다 오류가 적은 안정적인 조합을 유지하는 것이 중요합니다.

---

## SQLite, MySQL, Vector DB의 역할

이번 과정에서는 MySQL을 직접 실습 도구로 사용하지 않습니다.

SQL과 관계형 데이터베이스의 기본 개념은 다른 강의에서 이미 다루었다고 가정합니다.

다만 RAG를 이해하려면 일반 데이터베이스와 Vector DB의 차이를 알아야 하므로,  
MySQL은 비교 대상으로만 언급합니다.

---

## SQLite를 사용하는 이유

SQLite는 별도의 서버 설치 없이 사용할 수 있는 가벼운 데이터베이스입니다.

Python에도 기본적으로 `sqlite3` 모듈이 포함되어 있어 간단한 실습에 적합합니다.

이번 과정에서 SQLite는 다음 용도로 사용할 수 있습니다.

| 용도 | 설명 |
|---|---|
| 문서 목록 저장 | 업로드한 문서 파일명, 경로, 생성일 저장 |
| 메타데이터 저장 | 문서 제목, 작성자, 카테고리 등 저장 |
| 키워드 검색 실습 | SQL `LIKE`를 이용한 간단한 검색 |
| 검색 한계 확인 | 문자열 검색이 의미 검색과 다르다는 점 확인 |
| 최종 프로젝트 보조 저장소 | 사용자 질문 로그, 문서 메타데이터 저장 |

SQLite는 학습 부담이 적고 설치가 간단하기 때문에 초반 실습에 적합합니다.

---

## MySQL은 왜 직접 사용하지 않을까?

MySQL은 실무에서 많이 사용하는 관계형 데이터베이스입니다.

사용자, 권한, 주문, 게시글, 로그 같은 구조화된 데이터를 안정적으로 관리하는 데 적합합니다.

하지만 이번 과정은 SQL 강의가 아니라 자연어처리와 생성형 AI 실습 과정입니다.

따라서 MySQL을 설치하고 운영하는 데 시간을 많이 쓰면 강의의 초점이 흐려질 수 있습니다.

이 과정에서는 MySQL을 다음처럼만 다룹니다.

```text
MySQL
    ↓
실습 도구가 아니라 비교 설명용
    ↓
일반 관계형 데이터베이스의 대표 예시
```

즉, 학생들이 이미 알고 있는 관계형 DB와 새로 배울 Vector DB를 비교하기 위한 기준으로 사용합니다.

---

## 일반 DB 검색과 Vector DB 검색의 차이

SQLite나 MySQL 같은 일반 관계형 데이터베이스는 정확한 값 검색, 조건 검색, 문자열 검색에 강합니다.

예를 들어 다음과 같은 검색입니다.

```sql
SELECT *
FROM documents
WHERE content LIKE '%연차%';
```

이 방식은 문서 안에 특정 단어가 포함되어 있는지 찾는 데는 유용합니다.

하지만 RAG에서는 사용자의 질문과 의미가 비슷한 문서 조각을 찾아야 합니다.

예를 들어 사용자가 이렇게 질문했다고 해봅시다.

```text
입사 후 휴가는 언제부터 쓸 수 있나요?
```

문서에는 다음과 같이 적혀 있을 수 있습니다.

```text
연차휴가는 입사일 기준으로 산정한다.
```

사람은 두 문장이 관련 있다는 것을 알 수 있습니다.

하지만 단순 문자열 검색만으로는 이런 의미적 관련성을 찾기 어렵습니다.

그래서 RAG에서는 문장을 벡터로 바꾸고, 의미가 가까운 문서를 찾는 Vector DB를 사용합니다.

---

## ChromaDB를 사용하는 이유

ChromaDB는 RAG 입문 실습에 적합한 Vector DB입니다.

문서 조각과 임베딩 벡터를 저장하고,  
사용자 질문과 의미가 가까운 문서를 검색하는 데 사용할 수 있습니다.

ChromaDB를 사용하는 이유는 다음과 같습니다.

| 이유 | 설명 |
|---|---|
| 입문 난이도 | Python 코드로 비교적 쉽게 사용할 수 있음 |
| RAG 예제 | LangChain, LlamaIndex 등 여러 예제에서 자주 사용 |
| 메타데이터 관리 | 문서 출처, 페이지, 제목 등을 함께 저장하기 쉬움 |
| 로컬 실습 | 별도 서버 없이 로컬에서 실습하기 좋음 |
| 교육 적합성 | 의미 기반 검색 개념을 설명하기 좋음 |

따라서 이번 과정에서는 RAG 입문 실습의 기본 Vector DB로 ChromaDB를 사용합니다.

---

## FAISS는 언제 사용할까?

FAISS는 Meta에서 공개한 고성능 벡터 유사도 검색 라이브러리입니다.

대량의 벡터를 빠르게 검색하는 데 강점이 있습니다.

하지만 입문 단계에서는 ChromaDB보다 조금 더 저수준으로 느껴질 수 있습니다.

| 구분 | ChromaDB | FAISS |
|---|---|---|
| 교육 난이도 | 쉬움 | 상대적으로 어려움 |
| 메타데이터 저장 | 편리함 | 별도 관리 필요 |
| 로컬 RAG 실습 | 적합 | 가능하지만 구조 설명 필요 |
| 대규모 검색 성능 | 보통 | 강함 |
| 입문 추천 | 적합 | 고급 선택지 |

이 과정에서는 FAISS를 다음 위치로 둡니다.

```text
ChromaDB
    ↓
RAG 입문 실습 기본 도구

FAISS
    ↓
고급 벡터 검색과 대용량 검색 선택지
```

---

## 데이터 저장과 벡터 검색의 역할 분리

실무 RAG 시스템에서는 일반 데이터 저장소와 벡터 검색 저장소를 함께 사용하는 경우가 많습니다.

역할을 나누면 다음과 같습니다.

| 역할 | 적합한 도구 | 예시 |
|---|---|---|
| 문서 메타데이터 저장 | SQLite, MySQL, PostgreSQL | 파일명, 업로드 시간, 사용자 ID |
| 업무 데이터 저장 | MySQL, PostgreSQL | 주문, 회원, 권한, 로그 |
| 벡터 검색 | ChromaDB, FAISS, pgvector | 의미가 비슷한 문서 chunk 검색 |
| 실무 통합형 | PostgreSQL + pgvector | 일반 데이터와 벡터 검색 통합 |

이번 과정에서는 처음부터 복잡한 DB 구조를 사용하지 않습니다.

교육 흐름은 다음처럼 단계적으로 진행합니다.

```text
SQLite로 문서와 메타데이터 저장
    ↓
키워드 검색의 한계 확인
    ↓
Embedding 개념 학습
    ↓
ChromaDB로 의미 기반 검색 구현
    ↓
FAISS는 고급 벡터 검색 도구로 소개
```

이 흐름을 통해 학생들은 왜 Vector DB가 필요한지 자연스럽게 이해할 수 있습니다.

---

## Jupyter Notebook과 JupyterLab

Jupyter는 Python 코드를 셀 단위로 실행하면서 결과를 바로 확인할 수 있는 도구입니다.

AI와 데이터 분석 교육에서 매우 많이 사용됩니다.

Jupyter를 사용하는 이유는 다음과 같습니다.

- 코드와 설명을 함께 작성할 수 있다.
- 실행 결과를 바로 확인할 수 있다.
- 그래프와 표를 쉽게 확인할 수 있다.
- 실험 과정을 기록하기 좋다.

JupyterLab 실행 명령어는 다음과 같습니다.

```bash
jupyter lab
```

브라우저가 열리면 Notebook을 만들고 코드를 실행할 수 있습니다.

---

## VS Code에서 Jupyter 사용하기

VS Code에서도 `.ipynb` 파일을 열어 Jupyter Notebook처럼 사용할 수 있습니다.

기본 흐름은 다음과 같습니다.

```text
VS Code 실행
    ↓
프로젝트 폴더 열기
    ↓
Python Interpreter 선택
    ↓
.ipynb 파일 열기
    ↓
셀 단위 실행
```

여기서 중요한 것은 Python Interpreter입니다.

반드시 프로젝트의 `.venv` 환경을 선택해야 합니다.

VS Code 오른쪽 아래 또는 명령 팔레트에서 Python Interpreter를 선택할 수 있습니다.

---

## Google Colab

Google Colab은 브라우저에서 Python Notebook을 실행할 수 있는 환경입니다.

설치 부담이 적고, GPU를 사용할 수 있다는 장점이 있습니다.

Colab은 다음 상황에서 유용합니다.

- 학생 컴퓨터 환경이 제각각일 때
- GPU가 필요한 딥러닝 실습을 할 때
- 빠르게 Notebook을 공유하고 실행할 때
- 로컬 설치 오류를 피하고 싶을 때

하지만 Colab에도 단점이 있습니다.

| 장점 | 단점 |
|---|---|
| 설치 부담이 적다 | 파일 경로 관리가 불편할 수 있다 |
| GPU 사용 가능 | 세션이 끊길 수 있다 |
| 공유가 쉽다 | 장기 프로젝트 관리에는 불편할 수 있다 |
| 브라우저만 있으면 실행 가능 | 로컬 서비스 실행에는 제한이 있다 |

따라서 초반에는 로컬 환경과 Colab을 모두 경험해 보는 것이 좋습니다.

---

## Docker는 언제 사용할까?

Docker는 실행 환경을 컨테이너로 묶어 재현 가능하게 만드는 도구입니다.

하지만 처음부터 Docker를 사용하면 초보 학습자에게 부담이 될 수 있습니다.

그래서 이번 과정에서는 Docker를 후반부에 도입합니다.

초반에는 다음 도구에 먼저 익숙해집니다.

```text
Python
venv
pip
VS Code
Git
Jupyter
SQLite
```

이후 프로젝트가 커지면 Docker를 사용합니다.

예를 들어 최종 RAG 챗봇 프로젝트에서는 다음 구성 요소가 필요할 수 있습니다.

```text
FastAPI 서버
Streamlit UI
SQLite 메타데이터 저장소
ChromaDB 벡터 저장소
LLM API 연결
문서 저장소
```

이런 구조를 안정적으로 실행하려면 Docker가 도움이 됩니다.

---

## Docker를 사용하는 이유

Docker를 사용하는 이유는 다음과 같습니다.

| 이유 | 설명 |
|---|---|
| 재현성 | 다른 컴퓨터에서도 같은 환경으로 실행 가능 |
| 배포 준비 | 실제 서비스 배포 구조와 비슷하게 구성 가능 |
| 의존성 관리 | Python, OS 패키지, 서비스 환경을 함께 관리 |
| 협업 | 팀원 간 환경 차이를 줄일 수 있음 |
| 실무성 | 현업 프로젝트에서 자주 사용됨 |

다만 Docker는 처음 배우면 개념이 낯설 수 있습니다.

따라서 이 과정에서는 프로젝트 후반부에 자연스럽게 도입합니다.

---

## uv는 언제 다룰까?

최근 Python 생태계에서는 `uv`라는 도구도 많이 사용되고 있습니다.

`uv`는 빠른 패키지 설치와 프로젝트 관리를 지원하는 최신 도구입니다.

하지만 이번 과정의 초반 표준은 `venv + pip`입니다.

이유는 다음과 같습니다.

- 대부분의 학생이 검색하기 쉽다.
- Python 공식 문서와 자료가 많다.
- 오류가 발생했을 때 해결 사례를 찾기 쉽다.
- 교육 초반에는 도구보다 개념 이해가 중요하다.

`uv`는 후반부에서 최신 Python 프로젝트 관리 도구로 소개할 수 있습니다.

---

## Git으로 첫 커밋 만들기

프로젝트 폴더를 만들고 파일을 작성했다면 Git으로 첫 커밋을 만들어 봅니다.

```bash
git status
```

변경된 파일을 확인한 뒤 추가합니다.

```bash
git add .
```

커밋을 만듭니다.

```bash
git commit -m "Initial project setup"
```

Git은 실습 코드와 강의 자료의 변경 이력을 남기는 중요한 도구입니다.

처음에는 어렵게 느껴질 수 있지만, 자주 쓰다 보면 자연스러워집니다.

---

## .gitignore

Git 저장소에는 모든 파일을 다 넣으면 안 됩니다.

예를 들어 가상환경 폴더나 캐시 파일은 Git에 올리지 않는 것이 좋습니다.

이를 위해 `.gitignore` 파일을 사용합니다.

예시는 다음과 같습니다.

```gitignore
# Python
__pycache__/
*.py[cod]
.ipynb_checkpoints/

# Virtual environment
.venv/
venv/

# OS files
.DS_Store
Thumbs.db

# Environment variables
.env

# Data
datasets/raw/

# Local databases
*.db
*.sqlite
*.sqlite3

# Vector DB local files
chroma/
chroma_db/
faiss_index/
```

`.venv`는 각자의 컴퓨터에서 다시 만들 수 있으므로 Git에 올리지 않습니다.

SQLite DB 파일이나 ChromaDB 로컬 저장소도 실습 상황에 따라 Git에 올리지 않는 것이 좋습니다.

---

## 환경 변수와 API Key

후반부에서 LLM API를 사용할 때 API Key가 필요할 수 있습니다.

API Key는 비밀번호와 비슷하게 다루어야 합니다.

절대로 코드 안에 직접 적어 Git에 올리면 안 됩니다.

나쁜 예시는 다음과 같습니다.

```python
api_key = "sk-..."
```

대신 `.env` 파일이나 환경 변수를 사용합니다.

```text
OPENAI_API_KEY=your_api_key_here
```

그리고 `.env` 파일은 `.gitignore`에 포함해야 합니다.

```gitignore
.env
```

API Key 관리는 AI 실무에서 매우 중요한 보안 습관입니다.

---

## 실습 환경 점검 코드

가상환경을 활성화한 뒤 다음 코드를 실행해 봅니다.

```python
import sys
import platform

print("Python version:", sys.version)
print("Platform:", platform.platform())
```

추가로 주요 패키지가 설치되었는지 확인합니다.

```python
import numpy as np
import pandas as pd
import sklearn

print("numpy:", np.__version__)
print("pandas:", pd.__version__)
print("scikit-learn:", sklearn.__version__)
```

오류 없이 버전이 출력되면 기본 환경이 준비된 것입니다.

---

## SQLite 점검 코드

SQLite는 Python 기본 라이브러리로 사용할 수 있습니다.

간단히 다음 코드를 실행해 봅니다.

```python
import sqlite3

conn = sqlite3.connect(":memory:")
cur = conn.cursor()

cur.execute("CREATE TABLE documents (id INTEGER PRIMARY KEY, title TEXT, content TEXT)")
cur.execute(
    "INSERT INTO documents (title, content) VALUES (?, ?)",
    ("휴가 규정", "연차휴가는 입사일 기준으로 산정합니다.")
)

cur.execute("SELECT title, content FROM documents WHERE content LIKE ?", ("%연차%",))
rows = cur.fetchall()

print(rows)

conn.close()
```

이 코드는 메모리 안에 임시 SQLite DB를 만들고,  
간단한 문서를 저장한 뒤 키워드 검색을 수행합니다.

이후 RAG 실습에서는 이 키워드 검색의 한계를 확인하고,  
ChromaDB 기반 의미 검색으로 확장합니다.

---

## 첫 번째 Python 실습

아주 간단한 자연어처리 느낌의 코드를 실행해 봅시다.

```python
sentence = "나는 자연어처리를 공부하고 있습니다."

tokens = sentence.replace(".", "").split()

print(tokens)
```

예상 결과는 다음과 같습니다.

```text
['나는', '자연어처리를', '공부하고', '있습니다']
```

이 코드는 매우 단순한 공백 기준 토큰화입니다.

하지만 여기서 중요한 개념이 등장합니다.

```text
문장
    ↓
토큰
    ↓
모델 입력 준비
```

앞으로 우리는 이 단순한 과정을 훨씬 정교하게 확장하게 됩니다.

---

## 자주 발생하는 오류

실습 환경을 만들 때 자주 발생하는 오류를 미리 알아봅시다.

| 오류 상황 | 가능한 원인 |
|---|---|
| `python` 명령어가 동작하지 않음 | Python PATH 설정 문제 |
| `pip` 설치가 안 됨 | 가상환경 미활성화 또는 pip 문제 |
| VS Code에서 패키지를 못 찾음 | Interpreter가 `.venv`가 아님 |
| Jupyter에서 import 오류 | Notebook Kernel이 다른 환경을 사용 |
| Git 명령어가 안 됨 | Git 미설치 또는 PATH 문제 |
| 한글 경로 문제 | 프로젝트 경로에 공백/특수문자가 있음 |
| SQLite 파일 경로 오류 | DB 파일 위치 또는 상대 경로 문제 |
| ChromaDB 저장소 오류 | 로컬 저장 경로 또는 패키지 버전 문제 |

오류가 발생하면 당황하지 않아도 됩니다.

개발환경 오류는 실습 과정에서 자연스럽게 만나는 문제입니다.

중요한 것은 오류 메시지를 읽고, 현재 어떤 환경에서 실행 중인지 확인하는 습관입니다.

---

## 환경 문제를 해결하는 기본 순서

문제가 생기면 다음 순서로 확인합니다.

```text
1. 현재 폴더가 맞는가?
2. 가상환경이 활성화되어 있는가?
3. Python 버전이 맞는가?
4. pip가 현재 Python과 연결되어 있는가?
5. 패키지가 설치되어 있는가?
6. VS Code Interpreter가 맞는가?
7. Jupyter Kernel이 맞는가?
8. 데이터 파일 경로가 맞는가?
9. 로컬 DB 또는 Vector DB 저장 경로가 맞는가?
```

명령어로 확인할 수 있습니다.

```bash
python --version
python -m pip --version
python -m pip list
```

macOS나 Linux에서 Python 명령어가 다르면 다음도 확인합니다.

```bash
python3 --version
python3 -m pip --version
```

---

## 강의에서 사용할 환경 전략

이번 과정에서는 다음 전략을 사용합니다.

### 초반

```text
Python
venv
pip
VS Code
Git
Jupyter
SQLite
```

기본 개발 습관, 실습 흐름, 간단한 데이터 저장을 익힙니다.

### 중반

```text
scikit-learn
PyTorch
Hugging Face
Notebook 실습
```

머신러닝, 딥러닝, Transformer 실습을 진행합니다.

### 후반

```text
FastAPI
Streamlit
SQLite
ChromaDB
FAISS 소개
Docker
RAG 프로젝트
```

실제 서비스 구조에 가까운 프로젝트를 만듭니다.

이렇게 단계적으로 진행하면 처음부터 너무 많은 도구에 부담을 느끼지 않고 학습할 수 있습니다.

---

## 이번 문서의 핵심 정리

이번 문서에서는 앞으로의 실습을 위한 개발환경을 살펴보았습니다.

핵심은 다음과 같습니다.

- AI 실습에서는 Python 버전과 패키지 환경이 중요하다.
- 이번 과정의 표준 Python 버전은 Python 3.11이다.
- 초반에는 `venv + pip`를 사용해 기본 환경을 구성한다.
- VS Code는 코드 편집과 Jupyter 실행에 사용한다.
- Git은 실습 코드와 강의 자료의 변경 이력을 관리하는 도구이다.
- Jupyter는 코드와 설명을 함께 실험하기 좋은 환경이다.
- Colab은 설치 부담을 줄이고 GPU 실습에 유용하다.
- SQLite는 초반 문서/메타데이터 저장과 키워드 검색 실습에 적합하다.
- MySQL은 직접 실습하지 않고 일반 관계형 DB 비교 대상으로만 언급한다.
- ChromaDB는 RAG의 의미 기반 검색 실습에 사용할 기본 Vector DB이다.
- FAISS는 고급/대용량 벡터 검색 선택지로 소개한다.
- Docker는 초반이 아니라 후반 프로젝트에서 도입한다.
- API Key는 코드에 직접 적지 않고 환경 변수로 관리해야 한다.
- 개발환경 오류는 자연스러운 학습 과정이며, 확인 순서를 가지고 접근해야 한다.

---

## 잠깐 복습하기

다음 질문에 스스로 답해 봅시다.

1. AI 실습에서 개발환경이 중요한 이유는 무엇인가?
2. 이번 과정에서 Python 3.11을 기준으로 사용하는 이유는 무엇인가?
3. 가상환경은 왜 필요한가?
4. `venv`와 `pip`는 각각 어떤 역할을 하는가?
5. VS Code에서 Python Interpreter를 올바르게 선택해야 하는 이유는 무엇인가?
6. Jupyter Notebook은 어떤 실습에 유용한가?
7. Colab의 장점과 단점은 무엇인가?
8. SQLite를 초반 실습에서 사용하는 이유는 무엇인가?
9. MySQL을 직접 실습하지 않고 비교 대상으로만 언급하는 이유는 무엇인가?
10. 일반 DB 검색과 Vector DB 검색의 차이는 무엇인가?
11. ChromaDB가 RAG 입문 실습에 적합한 이유는 무엇인가?
12. FAISS는 어떤 경우에 유용한가?
13. Docker를 초반이 아니라 후반에 도입하는 이유는 무엇인가?
14. API Key를 코드에 직접 적으면 왜 위험한가?
15. 환경 오류가 발생했을 때 어떤 순서로 확인해야 하는가?

---

## 강의 중 실습

이번 문서의 내용은 설명만 듣고 끝내지 않습니다.

강의 중에는 다음 작업을 직접 진행합니다.

```text
1. Python 버전 확인
2. Git 버전 확인
3. 프로젝트 폴더 생성
4. 가상환경 생성
5. 가상환경 활성화
6. 기본 패키지 설치
7. VS Code에서 프로젝트 열기
8. Jupyter Notebook 실행
9. 간단한 토큰화 코드 실행
10. SQLite 메모리 DB 실습
11. Git 첫 커밋 만들기
```

---

## 실습 체크리스트

아래 항목을 하나씩 확인합니다.

| 체크 | 항목 |
|---|---|
| ☐ | Python 3.11 설치 확인 |
| ☐ | pip 확인 |
| ☐ | VS Code 설치 |
| ☐ | Python 확장 설치 |
| ☐ | Jupyter 확장 설치 |
| ☐ | Git 설치 |
| ☐ | 프로젝트 폴더 생성 |
| ☐ | `.venv` 가상환경 생성 |
| ☐ | 가상환경 활성화 |
| ☐ | 기본 패키지 설치 |
| ☐ | JupyterLab 실행 |
| ☐ | VS Code Interpreter 설정 |
| ☐ | SQLite 기본 코드 실행 |
| ☐ | `.gitignore` 작성 |
| ☐ | 첫 커밋 생성 |

---

## 다음 문서

다음 문서에서는 Chapter 1에서 배운 내용을 정리합니다.

AI, 머신러닝, 딥러닝, 자연어처리, 생성형 AI, LLM, RAG의 관계를 한 번에 정리하고,  
앞으로 이어질 Part 1 학습으로 연결합니다.

## 키워드 검색과 벡터 검색 비교

![SQLite 키워드 검색과 ChromaDB 벡터 검색 비교](images/06_keyword_vs_vector_search.svg)

> 일반 키워드 검색은 단어 일치에 강하고, 벡터 검색은 표현이 달라도 의미가 비슷한 문서를 찾는 데 유리합니다.

> 다음: `08_Summary.md`

---

# 부록. 실행 환경 점검과 문제 해결

이번 과정에서는 같은 예제를 여러 환경에서 실행할 수 있습니다.

권장 확인 순서는 다음과 같습니다.

```text
콘솔에서 Python 파일 실행
    ↓
VS Code에서 Python 파일 실행
    ↓
VS Code에서 Notebook 실행
    ↓
JupyterLab에서 Notebook 실행
    ↓
Google Colab에서 Notebook 실행
```

이 순서로 확인하면 문제가 발생했을 때 어느 환경에서 문제가 생겼는지 쉽게 찾을 수 있습니다.

---

## 콘솔에서 예제 코드 실행 확인

먼저 프로젝트 루트에서 Python 파일이 정상 실행되는지 확인합니다.

```bash
cd /Users/jeongjonguk/Documents/GitHub/NLP-Training-2026
source .venv/bin/activate

python examples/chapter01/01_simple_tokenization.py
python examples/chapter01/02_rule_based_intent.py
python examples/chapter01/03_sqlite_keyword_search.py
```

`04_faq_chatbot.py`는 대화형 입력을 받는 예제입니다.

```bash
python examples/chapter01/04_faq_chatbot.py
```

종료하려면 다음을 입력합니다.

```text
q
```

콘솔에서 실행이 정상이라면 코드 자체와 Python 가상환경은 대부분 정상입니다.

---

## VS Code에서 Python 파일 실행 확인

VS Code는 프로젝트 폴더 전체를 열어야 합니다.

```bash
cd /Users/jeongjonguk/Documents/GitHub/NLP-Training-2026
code .
```

VS Code 왼쪽 Explorer 최상단이 `NLP-Training-2026`인지 확인합니다.

그 다음 Python Interpreter를 선택합니다.

```text
Cmd + Shift + P
→ Python: Select Interpreter
→ .venv 선택
```

선택해야 할 Python 경로는 보통 다음과 비슷합니다.

```text
/Users/jeongjonguk/Documents/GitHub/NLP-Training-2026/.venv/bin/python
```

VS Code에서 Python 파일을 실행했을 때 콘솔과 같은 결과가 나오면 정상입니다.

---

## VS Code에서 Notebook 실행이 안 될 때

VS Code에서 `.ipynb` 파일 실행이 실패하거나, 개발자 도구를 확인하라는 메시지가 나올 수 있습니다.

이 경우 대부분 Python 가상환경은 준비되어 있지만, Jupyter Kernel이 VS Code에 제대로 등록되지 않은 상태입니다.

프로젝트 루트에서 다음 명령어를 실행합니다.

```bash
cd /Users/jeongjonguk/Documents/GitHub/NLP-Training-2026

source .venv/bin/activate

python -m pip install ipykernel jupyterlab notebook

python -m ipykernel install --user \
  --name nlp-training-2026 \
  --display-name "Python 3.11 (NLP Training 2026)"
```

그 다음 VS Code에서 Notebook을 열고 오른쪽 위의 Kernel을 선택합니다.

```text
Select Kernel
→ Python 3.11 (NLP Training 2026)
```

또는 `.venv` 경로의 Python을 선택합니다.

그래도 안 되면 VS Code를 다시 로드합니다.

```text
Cmd + Shift + P
→ Developer: Reload Window
```

---

## JupyterLab에서 Notebook 실행 확인

VS Code 문제가 아니라 Notebook 자체가 정상인지 확인하려면 JupyterLab에서 실행해 볼 수 있습니다.

```bash
cd /Users/jeongjonguk/Documents/GitHub/NLP-Training-2026
source .venv/bin/activate
jupyter lab
```

브라우저가 열리면 다음 파일을 실행합니다.

```text
notebooks/chapter01/01_chapter01_quick_demo.ipynb
notebooks/chapter01/02_rule_based_faq_chatbot.ipynb
```

JupyterLab에서는 정상인데 VS Code에서만 실패한다면, 대부분 VS Code의 Kernel 선택 또는 Jupyter 확장 문제입니다.

---

## Google Colab 사용 안내

Google Colab은 브라우저에서 Python Notebook을 실행할 수 있는 환경입니다.

별도 설치 부담이 적고, GPU가 필요한 실습에서도 유용합니다.

다만 Colab을 안정적으로 사용하려면 Google 계정 로그인이 필요합니다.

수강생은 강의 전에 다음을 준비합니다.

- Google 계정
- Chrome 브라우저 권장
- Google Drive 사용 가능 상태
- Colab 접속 확인

접속 주소는 다음과 같습니다.

```text
https://colab.research.google.com/
```

Notebook을 Colab에서 실행하는 방법은 다음과 같습니다.

```text
Colab 접속
    ↓
Google 계정 로그인
    ↓
파일 업로드 또는 Google Drive에서 Notebook 열기
    ↓
런타임 연결
    ↓
셀 실행
```

Chapter 1 Notebook은 기본 Python 기능을 중심으로 구성되어 있습니다.

주로 다음 기능을 사용합니다.

```text
문자열 처리
list / dict
함수
sqlite3
간단한 출력
```

`sqlite3`는 Python 표준 라이브러리이므로 Colab에서도 바로 사용할 수 있습니다.

따라서 Chapter 1 Notebook은 별도 패키지 설치 없이 Colab에서 실행 가능합니다.

---

## Colab 사용 시 주의할 점

Colab은 편리하지만 로컬 환경과 다른 점이 있습니다.

| 항목 | 로컬 환경 | Google Colab |
|---|---|---|
| 파일 저장 | 내 컴퓨터 폴더 | 런타임 또는 Google Drive |
| 패키지 설치 | 가상환경에 설치 | 런타임마다 설치 필요할 수 있음 |
| 세션 유지 | 직접 종료 전까지 유지 | 일정 시간 후 끊길 수 있음 |
| Git 작업 | 로컬 저장소 사용 | 별도 clone 또는 업로드 필요 |
| 장기 프로젝트 | 적합 | 파일 관리에 주의 필요 |

따라서 Colab은 초반 실습과 GPU 실습에는 유용하지만, 최종 프로젝트처럼 파일 구조가 중요한 작업은 로컬 환경에서 진행하는 것이 더 좋습니다.

---

## 강의 전 환경 점검 체크리스트

| 체크 | 항목 |
|---|---|
| ☐ | 콘솔에서 Python 예제 실행 확인 |
| ☐ | VS Code에서 프로젝트 폴더 열기 확인 |
| ☐ | VS Code Python Interpreter가 `.venv`인지 확인 |
| ☐ | VS Code에서 Python 파일 실행 확인 |
| ☐ | `ipykernel` 설치 및 Kernel 등록 확인 |
| ☐ | VS Code에서 Notebook 실행 확인 |
| ☐ | JupyterLab에서 Notebook 실행 확인 |
| ☐ | Google Colab 접속 확인 |
| ☐ | Colab에서 Notebook 업로드 후 실행 확인 |
| ☐ | MkDocs `mkdocs serve` 실행 확인 |

---

## 수강생 안내용 빠른 해결 명령어

VS Code Notebook 실행이 되지 않는 경우, 수강생에게 다음 명령어를 안내할 수 있습니다.

```bash
cd /Users/jeongjonguk/Documents/GitHub/NLP-Training-2026

source .venv/bin/activate

python -m pip install ipykernel jupyterlab notebook

python -m ipykernel install --user \
  --name nlp-training-2026 \
  --display-name "Python 3.11 (NLP Training 2026)"
```

이후 VS Code에서 Kernel을 다시 선택합니다.

```text
Python 3.11 (NLP Training 2026)
```

---

## 이번 문서에 추가된 운영 메모

이번 부록의 핵심은 다음과 같습니다.

```text
콘솔 실행이 되면 코드와 Python 환경은 대체로 정상이다.
VS Code Notebook 문제는 대부분 Kernel 등록 문제이다.
ipykernel을 설치하고 명시적으로 Kernel을 등록하면 해결되는 경우가 많다.
Colab은 Chapter 1 Notebook 실행에 적합하지만 Google 계정 로그인이 필요하다.
```
