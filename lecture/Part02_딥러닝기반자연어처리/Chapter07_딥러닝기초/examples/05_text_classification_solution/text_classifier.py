import json
from pathlib import Path

import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow import keras
from tensorflow.keras import layers

BASE_DIR, SEED = Path(__file__).resolve().parent, 42
OUTPUT_DIR = BASE_DIR / "output"


def main():
    keras.utils.set_random_seed(SEED)
    df = pd.read_csv(BASE_DIR / "inquiries.csv", encoding="utf-8-sig")
    labels = {name: i for i, name in enumerate(sorted(df["label"].unique()))}
    train, test = train_test_split(df, test_size=0.25, stratify=df["label"], random_state=SEED)
    train, valid = train_test_split(train, test_size=1/3, stratify=train["label"], random_state=SEED)
    vectorizer = layers.TextVectorization(max_tokens=1000, output_mode="multi_hot")
    vectorizer.adapt(train["text"].to_numpy())
    model = keras.Sequential([keras.Input(shape=(), dtype=tf.string), vectorizer, layers.Dense(32, activation="relu"), layers.Dropout(0.3), layers.Dense(len(labels), activation="softmax")])
    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    y = lambda frame: frame["label"].map(labels).to_numpy()
    model.fit(train["text"].to_numpy(), y(train), validation_data=(valid["text"].to_numpy(), y(valid)), epochs=30, verbose=0, callbacks=[keras.callbacks.EarlyStopping(patience=5, restore_best_weights=True)])
    metrics = model.evaluate(test["text"].to_numpy(), y(test), return_dict=True, verbose=0)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    model.save(OUTPUT_DIR / "text_classifier.keras")
    report = {"labels": labels, **{k: float(v) for k, v in metrics.items()}}
    (OUTPUT_DIR / "metrics.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(report)


if __name__ == "__main__": main()
