"""
进程启动时（模块被 import 时）只从磁盘加载一次 model.joblib，
之后各个请求直接复用这里的 model/encoder/threshold，不用每次都重新读文件或重新训练。
"""
import os

import joblib
import pandas as pd

MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "model.joblib")

_artifact = joblib.load(MODEL_PATH)

model = _artifact["model"]
encoder = _artifact["encoder"]
threshold = _artifact["threshold"]
feature_order = _artifact["feature_order"]


def predict_risk_batch(rows: list[dict]) -> list[dict]:
    """输入多台机器的原始传感器读数（dict 需含 type/air_temp_k/process_temp_k/
    rotational_speed_rpm/torque_nm/tool_wear_min），一次性向量化计算风险分数。
    统计类接口（如 /api/machines/stats）需要对全表算风险时，避免逐行调用模型。
    """
    if not rows:
        return []

    df = pd.DataFrame(rows)
    type_encoded = encoder.transform(df[["type"]])

    features = df[
        ["air_temp_k", "process_temp_k", "rotational_speed_rpm", "torque_nm", "tool_wear_min"]
    ].astype(float)
    features[["Type_H", "Type_L", "Type_M"]] = type_encoded
    features = features[feature_order]

    scores = model.predict_proba(features)[:, 1]
    return [{"risk_score": float(s), "at_risk": bool(s >= threshold)} for s in scores]


def predict_risk(
    machine_type: str,
    air_temp_k: float,
    process_temp_k: float,
    rotational_speed_rpm: float,
    torque_nm: float,
    tool_wear_min: float,
) -> dict:
    """输入一台机器的原始传感器读数，返回故障概率和按业务阈值判断的风险标记。"""
    return predict_risk_batch(
        [
            {
                "type": machine_type,
                "air_temp_k": air_temp_k,
                "process_temp_k": process_temp_k,
                "rotational_speed_rpm": rotational_speed_rpm,
                "torque_nm": torque_nm,
                "tool_wear_min": tool_wear_min,
            }
        ]
    )[0]
