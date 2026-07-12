# Windows 실습 환경 확인

> **기준 환경:** Windows 10/11, Python 3.11.9, VS Code, PowerShell

## Python 버전

이 과정은 Python `>=3.11,<3.12`를 사용합니다. Windows용 공식 설치 프로그램이 제공된 마지막 Python 3.11 릴리스는 3.11.9이므로 Windows 실습 기준 버전은 **Python 3.11.9**입니다.

Python 3.11.15는 보안 수정 릴리스지만 소스 코드만 배포되므로 Windows 교육 환경에서 직접 빌드해 사용할 필요는 없습니다.

```powershell
py -3.11 --version
```

예상 결과:

```text
Python 3.11.9
```

## 가상환경 생성과 활성화

```powershell
cd D:\git\NLP_Training_2026
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

PowerShell 실행 정책 때문에 활성화가 차단되면 현재 프로세스에서만 정책을 완화합니다.

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## VS Code 설정

1. VS Code에서 `D:\git\NLP_Training_2026` 폴더를 엽니다.
2. `Ctrl+Shift+P`를 누릅니다.
3. `Python: Select Interpreter`를 실행합니다.
4. `.venv\Scripts\python.exe`를 선택합니다.
5. Notebook 오른쪽 위에서도 같은 `.venv` Kernel을 선택합니다.

## 실행 확인

```powershell
python examples\chapter01\01_simple_tokenization.py
python projects\chapter01_mini_project\test_faq_chatbot.py
```

Notebook 전체 실행 확인:

```powershell
python -m jupyter nbconvert --to notebook --execute `
  notebooks\chapter01\01_chapter01_quick_demo.ipynb `
  --output 01_executed.ipynb
```

## MkDocs 실행

```powershell
mkdocs build --strict
mkdocs serve
```

브라우저에서 `http://127.0.0.1:8000/`에 접속해 모든 메뉴가 열리는지 확인합니다.

## JupyterLab 실행

```powershell
jupyter lab
```

Notebook이 실행되지 않으면 VS Code와 JupyterLab이 모두 `.venv`의 Python 3.11.9를 사용하고 있는지 먼저 확인합니다.
