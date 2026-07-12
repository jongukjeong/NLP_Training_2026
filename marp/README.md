# Marp 슬라이드 운영

각 Chapter의 `slides/ChapterXX_Slides.md`를 Marp 원본으로 관리합니다. 일반 Chapter는 40~45장을 기본으로 하며, 상세 강의 문서는 기존 Markdown을 유지합니다.

## VS Code

1. `Marp for VS Code` 확장을 설치합니다.
2. 슬라이드 Markdown을 엽니다.
3. `Marp: Export slide deck...`에서 PPTX를 선택합니다.

## CLI

```powershell
npx @marp-team/marp-cli@latest `
  lecture\Part01_자연어처리기초와Python\Chapter01_인공지능과자연어처리의이해\slides\Chapter01_Slides.md `
  --theme marp\nlp-training.css `
  --allow-local-files `
  -o outputs\Chapter01_Marp.pptx
```

일반 PPTX는 슬라이드가 렌더링 이미지로 들어갑니다. 내용 수정은 Marp Markdown에서 하고 다시 내보내는 방식을 권장합니다.
