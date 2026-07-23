####################################################
# 15.1 Transformers: 구성 요소 역할 구분
####################################################
components = {
    "Tokenizer": "문장을 token ID로 변환",
    "Config": "모델 구조와 설정 저장",
    "Model": "입력을 hidden state 또는 logit으로 변환",
    "Pipeline": "전처리부터 후처리까지 연결",
}

print("=== Hugging Face 구성 요소 ===")
for name, role in components.items():
    print(f"{name:10s}: {role}")
