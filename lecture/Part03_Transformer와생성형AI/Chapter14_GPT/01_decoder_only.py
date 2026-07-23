####################################################
# 14.1 Decoder Only: Causal Mask
####################################################
length = 4
mask = [
    [1 if key <= query else 0 for key in range(length)]
    for query in range(length)
]

print("=== Causal Mask ===")
for row in mask:
    print(row)
print("각 위치는 자신과 앞쪽 토큰만 볼 수 있습니다.")
