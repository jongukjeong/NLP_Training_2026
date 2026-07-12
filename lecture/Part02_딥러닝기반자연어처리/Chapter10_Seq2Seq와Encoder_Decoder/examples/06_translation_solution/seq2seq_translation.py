import json
from pathlib import Path

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

BASE_DIR, SEED = Path(__file__).resolve().parent, 42
START, END, PAD = "\t", "\n", " "


def vocabulary(texts):
    chars = sorted(set("".join(texts)) | {START, END, PAD})
    char_to_id = {char: i for i, char in enumerate(chars)}
    return chars, char_to_id


def encode(texts, mapping, max_length):
    data = np.full((len(texts), max_length), mapping[PAD], dtype="int32")
    for row, text in enumerate(texts):
        for column, char in enumerate(text[:max_length]):
            data[row, column] = mapping[char]
    return data


def main():
    keras.utils.set_random_seed(SEED)
    df = pd.read_csv(BASE_DIR / "translations.csv", encoding="utf-8-sig")
    sources = df["source"].astype(str).tolist()
    targets = [START + text + END for text in df["target"].astype(str)]
    source_chars, source_to_id = vocabulary(sources)
    target_chars, target_to_id = vocabulary(targets)
    max_source, max_target = max(map(len, sources)), max(map(len, targets))
    encoder_x = encode(sources, source_to_id, max_source)
    decoder_full = encode(targets, target_to_id, max_target)
    decoder_x, decoder_y = decoder_full[:, :-1], decoder_full[:, 1:]
    sample_weight = (decoder_y != target_to_id[PAD]).astype("float32")

    latent = 64
    encoder_inputs = keras.Input(shape=(None,), name="encoder_input")
    encoder_embedding = layers.Embedding(len(source_chars), 32, mask_zero=False)(encoder_inputs)
    _, state_h, state_c = layers.LSTM(latent, return_state=True, name="encoder_lstm")(encoder_embedding)
    decoder_inputs = keras.Input(shape=(None,), name="decoder_input")
    decoder_embedding_layer = layers.Embedding(len(target_chars), 32, mask_zero=False, name="decoder_embedding")
    decoder_embedding = decoder_embedding_layer(decoder_inputs)
    decoder_lstm = layers.LSTM(latent, return_sequences=True, return_state=True, name="decoder_lstm")
    decoder_outputs, _, _ = decoder_lstm(decoder_embedding, initial_state=[state_h, state_c])
    decoder_dense = layers.Dense(len(target_chars), activation="softmax", name="token_probability")
    outputs = decoder_dense(decoder_outputs)
    model = keras.Model([encoder_inputs, decoder_inputs], outputs)
    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    model.fit([encoder_x, decoder_x], decoder_y, sample_weight=sample_weight, epochs=80, batch_size=4, verbose=0)

    out = BASE_DIR / "output"; out.mkdir(exist_ok=True)
    model.save(out / "seq2seq.keras")
    config = {"source_chars": source_chars, "target_chars": target_chars, "max_source": max_source, "max_target": max_target, "start_id": target_to_id[START], "end_id": target_to_id[END], "pad_id": target_to_id[PAD]}
    (out / "vocabulary.json").write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
    print({"samples": len(df), "encoder_shape": list(encoder_x.shape), "decoder_shape": list(decoder_x.shape)})


if __name__ == "__main__": main()
