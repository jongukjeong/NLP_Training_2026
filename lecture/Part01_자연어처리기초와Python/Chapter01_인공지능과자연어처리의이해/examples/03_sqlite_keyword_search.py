"""
Chapter 1 Example 03
SQLite를 이용한 간단한 문서 저장과 키워드 검색 예제

실행:
    python examples/chapter01/03_sqlite_keyword_search.py
"""

import sqlite3


def create_sample_db() -> sqlite3.Connection:
    """메모리 기반 SQLite DB를 만들고 샘플 문서를 저장합니다."""
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    """)
    documents = [
        ("휴가 규정", "연차휴가는 입사일 기준으로 산정합니다."),
        ("배송 안내", "상품은 결제 완료 후 2일 이내 출고됩니다."),
        ("환불 안내", "환불은 상품 수령 후 7일 이내에 신청할 수 있습니다."),
        ("계정 안내", "비밀번호를 잊은 경우 비밀번호 찾기 기능을 이용합니다."),
    ]
    cur.executemany("INSERT INTO documents (title, content) VALUES (?, ?)", documents)
    conn.commit()
    return conn


def keyword_search(conn: sqlite3.Connection, keyword: str) -> list[tuple[str, str]]:
    """SQL LIKE를 이용해 특정 키워드가 포함된 문서를 찾습니다."""
    cur = conn.cursor()
    cur.execute("SELECT title, content FROM documents WHERE content LIKE ?", (f"%{keyword}%",))
    return cur.fetchall()


def main() -> None:
    conn = create_sample_db()
    for keyword in ["연차", "휴가", "배송", "입사", "쉬는 날"]:
        rows = keyword_search(conn, keyword)
        print(f"검색어: {keyword}")
        if rows:
            for title, content in rows:
                print(f"- {title}: {content}")
        else:
            print("- 검색 결과 없음")
        print("-" * 50)
    conn.close()


if __name__ == "__main__":
    main()
