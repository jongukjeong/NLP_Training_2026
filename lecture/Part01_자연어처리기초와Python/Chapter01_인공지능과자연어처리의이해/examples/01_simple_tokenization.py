"""
Chapter 1 Example 01
간단한 공백 기준 토큰화 예제

실행:
    python examples/chapter01/01_simple_tokenization.py
"""

def simple_tokenize(sentence: str) -> list[str]:
    """마침표를 제거한 뒤 공백 기준으로 문장을 나눕니다."""
    return sentence.replace(".", "").split()


def main() -> None:
    sentence = "나는 자연어처리를 공부하고 있습니다."
    tokens = simple_tokenize(sentence)
    print("원문:", sentence)
    print("토큰:", tokens)


if __name__ == "__main__":
    main()
