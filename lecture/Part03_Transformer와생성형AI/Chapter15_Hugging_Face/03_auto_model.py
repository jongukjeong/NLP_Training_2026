####################################################
# 15.3 AutoModel: Base Model과 Task Head 구분
####################################################
input_shape = (2, 5)
hidden_size = 8
classes = 3

base_output_shape = (input_shape[0], input_shape[1], hidden_size)
classification_logits_shape = (input_shape[0], classes)

print("Token ID shape:", input_shape)
print("AutoModel hidden state shape:", base_output_shape)
print("AutoModelForSequenceClassification logit shape:", classification_logits_shape)
