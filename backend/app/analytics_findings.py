"""
离线统计结论常量。这些数值来自 data/data_exploration.py 对完整 CSV 的一次性分析
（卡方检验、分组统计），不会随请求变化，所以不在接口里重新计算，直接返回已验证的结果。
"""

TYPE_BREAKDOWN = {
    "groups": [
        {"type": "H", "count": 1003, "failures": 21, "failure_rate": 0.0209},
        {"type": "M", "count": 2997, "failures": 83, "failure_rate": 0.0277},
        {"type": "L", "count": 6000, "failures": 235, "failure_rate": 0.0392},
    ],
    "chi2_p_value": 0.00103,
    "conclusion": "设备类型与故障率显著相关（卡方检验 p≈0.00103）：L 型故障率最高，H 型最低。",
}

SPEED_TORQUE_REGION = {
    "focus_region": {
        "name": "低转速 + 高扭矩",
        "count": 1055,
        "failures": 187,
        "failure_rate": 0.1773,
    },
    "other_region": {
        "name": "其他区域",
        "count": 8945,
        "failures": 152,
        "failure_rate": 0.0170,
    },
    "chi2_p_value": 6.8e-162,
    "conclusion": "低转速+高扭矩的重点区域故障率是其他区域的约10倍（p<0.001），是最强的故障预警区间。",
}

PWF_POWER_RULE = {
    "low_power_boundary_w": 3496.13,
    "high_power_boundary_w": 9001.22,
    "rule": "机械功率 < 低边界 或 > 高边界 ⇒ 判定为 PWF（电力故障）风险",
    "validation": "该规则在全量数据上完全复现了全部95例真实PWF故障，无漏报无误报。",
    "note": "这是从已知PWF故障样本反推出的可解释边界规则，不是有泛化保证的分类器。",
}

HDF_TEMPDIFF = {
    "bins": [
        {"range": "7.5-8.6", "count": 720, "failures": 115, "failure_rate": 0.1597},
        {"range": "8.6-9.5", "count": 3188, "failures": 0, "failure_rate": 0.0},
        {"range": "9.5-10.5", "count": 2403, "failures": 0, "failure_rate": 0.0},
        {"range": "10.5-12.2", "count": 3689, "failures": 0, "failure_rate": 0.0},
    ],
    "conclusion": "HDF（散热故障）几乎全部集中在温差最小的区间（7.5-8.6K），符合“散热间隙不足→过热”的物理直觉。",
}

OSF_RISK_INDEX = {
    "index_formula": "扭矩(Nm) × 刀具磨损(min)",
    "risk_threshold": 11000,
    "high_risk_group": {"count": 125, "failures": 98, "failure_rate": 0.784},
    "low_risk_group": {"count": 9875, "failures": 0, "failure_rate": 0.0},
    "chi2_p_value": 0.0001,
    "conclusion": "扭矩×磨损指标≥11000的设备，OSF故障率高达78.4%，是极强的高风险判定指标（p<0.0001）。",
}
