####################################################
# 15.2 AutoTokenizer: Token ID와 Attention Mask 읽기
####################################################
vocabulary = {"[PAD]": 0, "[UNK]": 1, "배송": 2, "빠름": 3}
tokens = ["배송", "빠름", "[PAD]"]
input_ids = [vocabulary.get(token, vocabulary["[UNK]"]) for token in tokens]
attention_mask = [int(token != "[PAD]") for token in tokens]

print("tokens:", tokens)
print("input_ids:", input_ids)
print("attention_mask:", attention_mask)
