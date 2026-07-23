####################################################
# 16.5 Mistral 계열: 처리량과 지연의 trade-off 비교
####################################################
runs = [
    {"batch": 1, "tokens_per_second": 28, "latency": 1.2},
    {"batch": 4, "tokens_per_second": 65, "latency": 2.8},
    {"batch": 8, "tokens_per_second": 91, "latency": 5.4},
]

print("=== Batch 성능 ===")
for run in runs:
    print(
        f"batch={run['batch']}, 처리량={run['tokens_per_second']} token/s, "
        f"지연={run['latency']}초"
    )
