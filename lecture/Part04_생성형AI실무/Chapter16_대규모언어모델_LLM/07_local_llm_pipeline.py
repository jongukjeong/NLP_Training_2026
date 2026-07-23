####################################################
# 16장 연결 예제: 로컬 LLM 용량과 속도 계획
####################################################
model = {"parameters_b": 8, "bits": 4}
context_tokens = 4096
runtime_buffer_gb = 1.5
kv_cache_gb = context_tokens / 4096 * 1.0
weight_gb = model["parameters_b"] * model["bits"] / 8
required_gb = weight_gb + kv_cache_gb + runtime_buffer_gb
available_gb = 8

print("가중치:", weight_gb, "GB")
print("KV cache:", kv_cache_gb, "GB")
print("예상 총 메모리:", required_gb, "GB")
print("실행 가능(추정):", required_gb <= available_gb)
