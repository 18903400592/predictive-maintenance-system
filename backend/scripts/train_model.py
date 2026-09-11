"""
移植自 data/machine_learning.py 的建模逻辑，生成 FastAPI 要用的 model.joblib。
逻辑保持一致：80/20 分层切分 -> OneHotEncoder 处理 Type -> LogisticRegression -> 阈值 0.031。
"""
import os

import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_CSV = os.path.join(BACKEND_DIR, "..", "data", "ai4i2020.csv")
MODEL_PATH = os.path.join(BACKEND_DIR, "model.joblib")

FEATURE_ORDER = [
    "air_temp_k",
    "process_temp_k",
    "rotational_speed_rpm",
    "torque_nm",
    "tool_wear_min",
    "Type_H",
    "Type_L",
    "Type_M",
]
THRESHOLD = 0.031


def main():
    df = pd.read_csv(DATA_CSV)
    df.columns = [
        "udi", "product_id", "type",
        "air_temp_k", "process_temp_k", "rotational_speed_rpm",
        "torque_nm", "tool_wear_min", "machine_failure",
        "twf", "hdf", "pwf", "osf", "rnf",
    ]

    X = df[["type", "air_temp_k", "process_temp_k", "rotational_speed_rpm", "torque_nm", "tool_wear_min"]]
    y = df["machine_failure"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    type_train = encoder.fit_transform(X_train[["type"]])
    type_test = encoder.transform(X_test[["type"]])

    X_train_final = pd.concat(
        [
            X_train.drop(columns=["type"]).reset_index(drop=True),
            pd.DataFrame(type_train, columns=["Type_H", "Type_L", "Type_M"]),
        ],
        axis=1,
    )[FEATURE_ORDER]

    X_test_final = pd.concat(
        [
            X_test.drop(columns=["type"]).reset_index(drop=True),
            pd.DataFrame(type_test, columns=["Type_H", "Type_L", "Type_M"]),
        ],
        axis=1,
    )[FEATURE_ORDER]

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train_final, y_train)

    y_prob = model.predict_proba(X_test_final)[:, 1]

    print("========== 模型评估（测试集） ==========")
    for threshold in (0.5, THRESHOLD):
        y_pred = (y_prob >= threshold).astype(int)
        acc = accuracy_score(y_test, y_pred)
        tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
        recall = tp / (tp + fn)
        print(
            f"阈值={threshold}  准确率={acc:.4f}  召回率={recall:.4f}  "
            f"抓到故障={tp}/{tp + fn}  误报={fp}"
        )

    joblib.dump(
        {
            "model": model,
            "encoder": encoder,
            "threshold": THRESHOLD,
            "feature_order": FEATURE_ORDER,
        },
        MODEL_PATH,
    )
    print(f"\n模型已保存到 {MODEL_PATH}")


if __name__ == "__main__":
    main()
