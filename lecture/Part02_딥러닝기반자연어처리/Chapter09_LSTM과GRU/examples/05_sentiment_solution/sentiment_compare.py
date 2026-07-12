import json
from pathlib import Path
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow import keras
from tensorflow.keras import layers

BASE_DIR, SEED = Path(__file__).resolve().parent, 42


def build(vectorizer, kind):
    recurrent = layers.LSTM(32) if kind == "lstm" else layers.GRU(32)
    model = keras.Sequential([keras.Input(shape=(), dtype=tf.string), vectorizer, layers.Embedding(len(vectorizer.get_vocabulary()), 32, mask_zero=True), layers.Bidirectional(recurrent), layers.Dropout(0.3), layers.Dense(1, activation="sigmoid")])
    model.compile(optimizer=keras.optimizers.Adam(clipnorm=1.0), loss="binary_crossentropy", metrics=["accuracy"])
    return model


def main():
    keras.utils.set_random_seed(SEED)
    df = pd.read_csv(BASE_DIR / "reviews.csv", encoding="utf-8-sig")
    train, test = train_test_split(df, test_size=0.25, stratify=df["label"], random_state=SEED)
    vectorizer = layers.TextVectorization(max_tokens=3000, output_mode="int", output_sequence_length=30)
    vectorizer.adapt(train["text"].to_numpy())
    reports, out = {}, BASE_DIR / "output"; out.mkdir(exist_ok=True)
    for kind in ("lstm", "gru"):
        keras.utils.set_random_seed(SEED)
        model = build(vectorizer, kind)
        model.fit(train["text"].to_numpy(), train["label"].to_numpy(), validation_split=0.25, epochs=25, verbose=0, callbacks=[keras.callbacks.EarlyStopping(patience=4, restore_best_weights=True)])
        reports[kind] = {k: float(v) for k, v in model.evaluate(test["text"].to_numpy(), test["label"].to_numpy(), return_dict=True, verbose=0).items()}
        model.save(out / f"{kind}.keras")
    (out / "comparison.json").write_text(json.dumps(reports, indent=2), encoding="utf-8")
    print(reports)


if __name__ == "__main__": main()
