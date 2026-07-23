####################################################
# 18.2 Vector Database: Vector와 Metadata를 함께 저장
####################################################
records = [
    {"id": "d1", "vector": [0.9, 0.1], "department": "고객지원", "version": 2},
    {"id": "d2", "vector": [0.8, 0.2], "department": "개발", "version": 2},
    {"id": "d3", "vector": [0.7, 0.3], "department": "고객지원", "version": 1},
]

filtered = [
    row for row in records
    if row["department"] == "고객지원" and row["version"] == 2
]
print("Metadata filter 결과:", filtered)
