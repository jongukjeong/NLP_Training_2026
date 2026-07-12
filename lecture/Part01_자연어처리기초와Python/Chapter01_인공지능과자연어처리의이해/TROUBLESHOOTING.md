# Chapter 1 Troubleshooting

> **Chapter 1. 인공지능과 자연어처리의 이해**  
> 문서: `TROUBLESHOOTING.md`

---

## 이 문서의 목적

이 문서는 Chapter 1 실습 중 자주 발생할 수 있는 환경 문제를 정리한 문서입니다.

강의 중 문제가 발생했을 때 다음 순서로 확인합니다.

```text
콘솔 실행 확인
    ↓
VS Code Python Interpreter 확인
    ↓
VS Code Notebook Kernel 확인
    ↓
JupyterLab 실행 확인
    ↓
Google Colab 실행 확인
```

---

## 1. 콘솔에서 Python 예제 실행 확인

프로젝트 루트로 이동합니다.

```bash
cd /Users/jeongjonguk/Documents/GitHub/NLP-Training-2026
```

가상환경을 활성화합니다.

```bash
source .venv/bin/activate
```

Python 버전을 확인합니다.

```bash
python --version
```

권장 버전은 다음과 같습니다.

```text
Python 3.11.x
```

Chapter 1 예제 파일을 실행합니다.

```bash
python examples/01_simple_tokenization.py
python examples/02_rule_based_intent.py
python examples/03_sqlite_keyword_search.py
```

FAQ 챗봇 예제는 대화형입니다.

```bash
python examples/04_faq_chatbot.py
```

종료하려면 다음을 입력합니다.

```text
q
```

---

## 2. `sqlite3` 오류가 발생할 때

Chapter 1의 SQLite 예제는 Python 표준 라이브러리인 `sqlite3`를 사용합니다.

별도 설치는 필요 없습니다.

다음 명령어로 확인합니다.

```bash
python -c "import sqlite3; print(sqlite3.sqlite_version)"
```

SQLite 버전이 출력되면 정상입니다.

Chapter 1의 `03_sqlite_keyword_search.py`는 파일 DB가 아니라 메모리 DB를 사용합니다.

```python
sqlite3.connect(":memory:")
```

따라서 파일 권한 문제나 DB 파일 경로 문제가 없어야 합니다.

만약 실행이 되지 않는다면 대부분 다음 중 하나입니다.

- 프로젝트 루트가 아닌 다른 위치에서 실행
- 파일 경로를 잘못 입력
- `examples/chapter01` 폴더 복사 누락
- VS Code가 다른 Python Interpreter를 사용

---

## 3. VS Code에서 프로젝트 폴더 열기

VS Code는 파일 하나만 여는 것보다 프로젝트 폴더 전체를 여는 것이 좋습니다.

```bash
cd /Users/jeongjonguk/Documents/GitHub/NLP-Training-2026
code .
```

왼쪽 Explorer 최상단이 `NLP-Training-2026`인지 확인합니다.

---

## 4. VS Code Python Interpreter 선택

VS Code에서 다음 명령을 실행합니다.

```text
Cmd + Shift + P
→ Python: Select Interpreter
```

다음 경로의 Python을 선택합니다.

```text
/Users/jeongjonguk/Documents/GitHub/NLP-Training-2026/.venv/bin/python
```

하단 상태바에 `.venv`가 표시되면 정상입니다.

---

## 5. VS Code에서 Notebook 실행이 안 될 때

VS Code에서 `.ipynb` 파일 실행이 실패하거나 개발자 도구를 확인하라는 메시지가 나올 수 있습니다.

이 경우 대부분 Jupyter Kernel 등록 문제입니다.

아래 명령어를 실행합니다.

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

그래도 안 되면 VS Code를 다시 로드합니다.

```text
Cmd + Shift + P
→ Developer: Reload Window
```

---

## 6. JupyterLab에서 Notebook 실행 확인

VS Code 문제가 아니라 Notebook 자체가 정상인지 확인하려면 JupyterLab을 사용합니다.

```bash
cd /Users/jeongjonguk/Documents/GitHub/NLP-Training-2026

source .venv/bin/activate

jupyter lab
```

브라우저에서 다음 파일을 엽니다.

```text
notebooks/01_chapter01_quick_demo.ipynb
notebooks/02_rule_based_faq_chatbot.ipynb
```

JupyterLab에서는 정상인데 VS Code에서만 실패한다면, VS Code의 Python Interpreter 또는 Notebook Kernel 문제일 가능성이 큽니다.

---

## 7. Google Colab에서 실행하기

Google Colab은 브라우저에서 Python Notebook을 실행할 수 있는 환경입니다.

접속 주소:

```text
https://colab.research.google.com/
```

Colab을 안정적으로 사용하려면 Google 계정 로그인이 필요합니다.

수강생 준비물:

- Google 계정
- Chrome 브라우저 권장
- Google Drive 사용 가능 상태
- Colab 접속 확인

Chapter 1 Notebook은 기본 Python 기능 중심이므로 Colab에서도 실행 가능합니다.

사용 기능:

```text
문자열 처리
list / dict
함수
sqlite3
간단한 출력
```

`sqlite3`는 Python 표준 라이브러리라 Colab에서도 바로 사용할 수 있습니다.

---

## 8. Colab과 로컬 환경의 차이

| 항목 | 로컬 환경 | Google Colab |
|---|---|---|
| 파일 저장 | 내 컴퓨터 폴더 | 런타임 또는 Google Drive |
| 패키지 설치 | 가상환경에 설치 | 런타임마다 설치 필요할 수 있음 |
| 세션 유지 | 직접 종료 전까지 유지 | 일정 시간 후 끊길 수 있음 |
| Git 작업 | 로컬 저장소 사용 | 별도 clone 또는 업로드 필요 |
| 장기 프로젝트 | 적합 | 파일 관리에 주의 필요 |

Colab은 초반 실습과 GPU 실습에는 유용합니다.

하지만 최종 프로젝트처럼 파일 구조가 중요한 작업은 로컬 환경에서 진행하는 것이 좋습니다.

---

## 9. MkDocs 404가 발생할 때

MkDocs에서 메뉴는 보이는데 페이지가 404인 경우, 대부분 `mkdocs.yml`의 nav 경로와 `docs/` 안의 실제 파일 경로가 맞지 않는 상태입니다.

현재 권장 구조는 다음과 같습니다.

```text
NLP-Training-2026/
├── lecture/
│   └── 원본 강의자료
├── docs/
│   ├── index.md
│   └── part01/
│       └── chapter01/
│           ├── README.md
│           ├── 01_Opening.md
│           └── ...
└── mkdocs.yml
```

`mkdocs.yml`에서는 다음처럼 `docs/` 기준 상대 경로를 사용합니다.

```yaml
Overview: part01/chapter01/README.md
01. Opening: part01/chapter01/01_Opening.md
```

문서 수정 후 MkDocs용 문서에 반영하려면 다음 명령을 사용합니다.

```bash
rm -rf docs/part01/chapter01
mkdir -p docs/part01/chapter01

cp lecture/Part01_자연어처리기초와Python/Chapter01_인공지능과자연어처리의이해/*.md docs/part01/chapter01/
```

---

## 10. 강의 전 체크리스트

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

## 11. 빠른 해결 명령어 모음

### 가상환경 활성화

```bash
cd /Users/jeongjonguk/Documents/GitHub/NLP-Training-2026
source .venv/bin/activate
```

### Python 버전 확인

```bash
python --version
```

### 예제 코드 실행

```bash
python examples/01_simple_tokenization.py
python examples/02_rule_based_intent.py
python examples/03_sqlite_keyword_search.py
```

### VS Code Notebook Kernel 등록

```bash
python -m pip install ipykernel jupyterlab notebook

python -m ipykernel install --user \
  --name nlp-training-2026 \
  --display-name "Python 3.11 (NLP Training 2026)"
```

### JupyterLab 실행

```bash
jupyter lab
```

### MkDocs 실행

```bash
mkdocs serve
```

---

## 핵심 정리

```text
콘솔 실행이 되면 코드와 Python 환경은 대체로 정상이다.
VS Code Notebook 문제는 대부분 Kernel 등록 문제이다.
ipykernel을 설치하고 명시적으로 Kernel을 등록하면 해결되는 경우가 많다.
Colab은 Chapter 1 Notebook 실행에 적합하지만 Google 계정 로그인이 필요하다.
MkDocs 404는 nav 경로와 docs 폴더 구조를 먼저 확인한다.
```
