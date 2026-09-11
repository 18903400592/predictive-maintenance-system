from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from app.db import run_query
from app.model_store import predict_risk, predict_risk_batch, threshold as RISK_THRESHOLD

router = APIRouter(prefix="/api/machines", tags=["machines"])

# risk_score 是模型对每台机器实时算出的故障概率。风险等级用于列表/详情页的展示分段，
# 和模型自己的判定阈值(at_risk, RISK_THRESHOLD=0.031)是两件事，故意分开：
# - at_risk / RISK_THRESHOLD(0.031) 是模型训练时选定的召回优先的决策阈值，不能改，
#   面试时要讲的"漏报代价远高于误报代价"就是基于这个值算的混淆矩阵。
# - risk_level 的"高风险"展示阈值(UI_HIGH_RISK_MAX)刻意设得更高(0.2)，只是为了让列表页
#   "高风险"标签的数量和真实故障率(~3.4%)大致匹配，避免大量健康机器被贴上高风险标签，
#   仍然完全来自同一个 risk_score，只是展示分段的切法不同，模型和 at_risk 语义不受影响。
RISK_LOW_MAX = 0.01
UI_HIGH_RISK_MAX = 0.2
STATUS_VALUES = {"all", "normal", "failure"}
RISK_LEVEL_VALUES = {"all", "low", "medium", "high"}


def _attach_risk(rows: list[dict]) -> None:
    if not rows:
        return
    risks = predict_risk_batch(
        [
            {
                "type": r["type"],
                "air_temp_k": r["air_temp_k"],
                "process_temp_k": r["process_temp_k"],
                "rotational_speed_rpm": r["rotational_speed_rpm"],
                "torque_nm": r["torque_nm"],
                "tool_wear_min": r["tool_wear_min"],
            }
            for r in rows
        ]
    )
    for row, risk in zip(rows, risks):
        row["risk_score"] = risk["risk_score"]
        row["at_risk"] = risk["at_risk"]
        row["risk_level"] = _risk_level(risk["risk_score"])


def _risk_level(risk_score: float) -> str:
    if risk_score >= UI_HIGH_RISK_MAX:
        return "high"
    if risk_score >= RISK_LOW_MAX:
        return "medium"
    return "low"


@router.get("")
def list_machines(
    limit: int = Query(50, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    type: Optional[str] = Query(None, min_length=1, max_length=1, description="设备类型 H/M/L"),
    status: str = Query("all", description="故障状态筛选：all/normal/failure，对应真实 machine_failure 标签"),
    risk_level: str = Query("all", description="模型风险等级筛选：all/low/medium/high，基于实时 risk_score"),
):
    if status not in STATUS_VALUES:
        raise HTTPException(status_code=400, detail=f"status 必须是 {sorted(STATUS_VALUES)} 之一")
    if risk_level not in RISK_LEVEL_VALUES:
        raise HTTPException(status_code=400, detail=f"risk_level 必须是 {sorted(RISK_LEVEL_VALUES)} 之一")

    sql = """
        SELECT udi, product_id, type, air_temp_k, process_temp_k,
               rotational_speed_rpm, torque_nm, tool_wear_min, machine_failure
        FROM machines
        WHERE (:type IS NULL OR type = :type)
          AND (:status = 'all' OR (:status = 'failure' AND machine_failure) OR (:status = 'normal' AND NOT machine_failure))
        ORDER BY udi
    """
    rows = run_query(sql, {"type": type, "status": status})
    _attach_risk(rows)

    if risk_level != "all":
        rows = [r for r in rows if r["risk_level"] == risk_level]

    # 默认按 udi 自然顺序排列（SQL 里已经 ORDER BY udi）：默认页反映设备真实分布
    # （正常设备占绝大多数），不做按风险分数排序，避免默认页看起来"全是故障/高风险"。

    page = rows[offset : offset + limit]
    return {"count": len(page), "total_matched": len(rows), "items": page}


@router.get("/stats")
def machine_stats():
    """全量设备的实时统计：总数/正常/故障（真实标签）+ 高风险（模型阈值）。
    不是硬编码常量,每次请求都基于当前数据库里的真实数据现算。"""
    rows = run_query(
        "SELECT type, air_temp_k, process_temp_k, rotational_speed_rpm, torque_nm, tool_wear_min, machine_failure FROM machines"
    )
    total = len(rows)
    failure = sum(1 for r in rows if r["machine_failure"])
    normal = total - failure

    risks = predict_risk_batch(
        [
            {
                "type": r["type"],
                "air_temp_k": r["air_temp_k"],
                "process_temp_k": r["process_temp_k"],
                "rotational_speed_rpm": r["rotational_speed_rpm"],
                "torque_nm": r["torque_nm"],
                "tool_wear_min": r["tool_wear_min"],
            }
            for r in rows
        ]
    )
    # 用展示层的高风险分档(UI_HIGH_RISK_MAX)而不是模型的 at_risk(0.031)，
    # 让首页统计卡片里的"高风险设备"数量和列表页风险等级筛选的"高"保持一致。
    high_risk = sum(1 for r in risks if r["risk_score"] >= UI_HIGH_RISK_MAX)

    return {
        "total": total,
        "normal": normal,
        "failure": failure,
        "high_risk": high_risk,
    }


@router.get("/{udi}")
def get_machine(udi: int):
    sql = """
        SELECT udi, product_id, type, air_temp_k, process_temp_k,
               rotational_speed_rpm, torque_nm, tool_wear_min, machine_failure,
               twf, hdf, pwf, osf, rnf
        FROM machines
        WHERE udi = :udi
    """
    rows = run_query(sql, {"udi": udi})
    if not rows:
        raise HTTPException(status_code=404, detail="设备不存在")

    row = rows[0]
    risk = predict_risk(
        machine_type=row["type"],
        air_temp_k=row["air_temp_k"],
        process_temp_k=row["process_temp_k"],
        rotational_speed_rpm=row["rotational_speed_rpm"],
        torque_nm=row["torque_nm"],
        tool_wear_min=row["tool_wear_min"],
    )
    row["risk_score"] = risk["risk_score"]
    row["at_risk"] = risk["at_risk"]
    row["risk_level"] = _risk_level(risk["risk_score"])
    row["power_w"] = float(row["torque_nm"]) * float(row["rotational_speed_rpm"]) * 2 * 3.14159 / 60
    row["temp_diff_k"] = float(row["process_temp_k"]) - float(row["air_temp_k"])

    return row
