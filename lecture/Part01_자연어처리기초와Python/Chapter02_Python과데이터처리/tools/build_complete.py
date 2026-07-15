from pathlib import Path


CHAPTER_DIR = Path(__file__).resolve().parent.parent
OUTPUT_PATH = CHAPTER_DIR / "Chapter02_Complete.md"
SOURCES = [
    "README.md",
    "01_Opening.md",
    "02_Python_Basics.md",
    "03_Strings_and_Collections.md",
    "04_Control_Flow.md",
    "05_Functions_and_Modules.md",
    "06_File_IO.md",
    "07_Pandas.md",
    "08_Data_Cleaning.md",
    "09_Summary.md",
    "10_Quiz.md",
    "11_Assignment.md",
    "12_Mini_Project.md",
]


def main() -> None:
    sections = ["# Chapter 2 통합 강의 원고"]

    for source_name in SOURCES:
        source_path = CHAPTER_DIR / source_name
        raw_content = source_path.read_text(encoding="utf-8").strip()
        content = "\n".join(line.rstrip() for line in raw_content.splitlines())
        sections.append(f"<!-- SOURCE: {source_name} -->\n\n{content}")

    OUTPUT_PATH.write_text(
        "\n\n---\n\n".join(sections) + "\n",
        encoding="utf-8",
    )
    print(f"생성 완료: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
