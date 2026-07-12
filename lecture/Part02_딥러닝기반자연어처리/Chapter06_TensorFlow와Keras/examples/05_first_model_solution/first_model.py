import json
import os
from pathlib import Path

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow import keras
from tensorflow.keras import layers

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
SEED = 42


def make_dataset(x, y, training=False):
    ds = tf.data.Dataset.from_tensor_slices((x.astype("float32"), y.astype("float32")))
    if training:
        ds = ds.shuffle(len(y), seed=SEED)
    return ds.batch(8).prefetch(tf.data.AUTOTUNE)


def main():
    tf.keras.utils.set_random_seed(SEED)
    df = pd.read_csv(BASE_DIR / "samples.csv", encoding="utf-8-sig")
    features = ["length", "keyword_count", "question_marks", "sentiment_score"]
    x_train, x_test, y_train, y_test = train_test_split(df[features], df["label"], test_size=0.2, stratify=df["label"], random_state=SEED)
    x_train, x_valid, y_train, y_valid = train_test_split(x_train, y_train, test_size=0.25, stratify=y_train, random_state=SEED)
    train_ds, valid_ds, test_ds = make_dataset(x_train, y_train, True), make_dataset(x_valid, y_valid), make_dataset(x_test, y_test)

    model = keras.Sequential([keras.Input(shape=(4,)), layers.Normalization(), layers.Dense(16, activation="relu"), layers.Dense(1, activation="sigmoid")])
    model.layers[0].adapt(x_train.astype("float32"))
    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    callbacks = [keras.callbacks.EarlyStopping(patience=5, restore_best_weights=True), keras.callbacks.ModelCheckpoint(OUTPUT_DIR / "best.keras", save_best_only=True)]
    history = model.fit(train_ds, validation_data=valid_ds, epochs=30, callbacks=callbacks, verbose=0)
    metrics = model.evaluate(test_ds, return_dict=True, verbose=0)
    report = {"epochs": len(history.history["loss"]), **{k: float(v) for k, v in metrics.items()}}
    (OUTPUT_DIR / "metrics.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
