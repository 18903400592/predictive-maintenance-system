import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency

df = pd.read_csv("ai4i2020.csv")

# 中文字体
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

# ====================
# 第一部分：画散点图
# ====================

normal = df[df["Machine failure机器故障"] == 0]
failure = df[df["Machine failure机器故障"] == 1]

plt.figure(figsize=(10, 7))

plt.scatter(
    normal["Rotational speed [rpm]转速"],
    normal["Torque [Nm]扭矩"],
    alpha=0.25,
    label="正常机器"
)

plt.scatter(
    failure["Rotational speed [rpm]转速"],
    failure["Torque [Nm]扭矩"],
    alpha=0.8,
    label="故障机器"
)

plt.xlabel("转速 [rpm]")
plt.ylabel("扭矩 [Nm]")
plt.title("转速与扭矩关系：正常机器 vs 故障机器")

plt.legend()
plt.grid(alpha=0.2)

plt.show(block=False)
plt.pause(1)
plt.close()


# ====================
# 第二部分：统计9个区域
# ====================

df["转速区间"] = pd.cut(
    df["Rotational speed [rpm]转速"],
    bins=3,
    labels=["低转速", "中转速", "高转速"]
)

df["扭矩区间"] = pd.cut(
    df["Torque [Nm]扭矩"],
    bins=3,
    labels=["低扭矩", "中扭矩", "高扭矩"]
)

result = df.groupby(
    ["转速区间", "扭矩区间"],
    observed=True
)["Machine failure机器故障"].agg(
    ["count", "sum", "mean"]
)

print(result)

high_speed_low_torque = df[
    (df["转速区间"] == "高转速") &
    (df["扭矩区间"] == "低扭矩")
]

print(high_speed_low_torque.shape)

print(
    high_speed_low_torque[
        [
            "Rotational speed [rpm]转速",
            "Torque [Nm]扭矩",
            "Tool wear [min]刀具磨损",
            "Machine failure机器故障"
        ]
    ].describe()
)

print(
    high_speed_low_torque["Tool wear [min]刀具磨损"].describe()
)

other_machines = df[
    ~(
        (df["转速区间"] == "高转速") &
        (df["扭矩区间"] == "低扭矩")
    )
]

print("高转速+低扭矩：")
print(
    high_speed_low_torque["Tool wear [min]刀具磨损"].describe()
)

print("\n其他机器：")
print(
    other_machines["Tool wear [min]刀具磨损"].describe()
)

failure_modes = [
    "TWF刀具磨损故障",
    "HDF散热故障",
    "PWF电力故障",
    "OSF过冲 / 突发故障",
    "RNF随机故障"
]

print(
    high_speed_low_torque[failure_modes].sum()
)

pwf_machines = df[
    df["PWF电力故障"] == 1
]

print(pwf_machines.shape)

print(
    pwf_machines[
        [
            "Rotational speed [rpm]转速",
            "Torque [Nm]扭矩"
        ]
    ].describe()
)

print(
    pwf_machines[
        [
            "Rotational speed [rpm]转速",
            "Torque [Nm]扭矩"
        ]
    ].head(20)
)

import numpy as np

df["机械功率W"] = (
    df["Torque [Nm]扭矩"]
    * df["Rotational speed [rpm]转速"]
    * 2 * np.pi / 60
)

print(
    df["机械功率W"].describe()
)

print("PWF故障机器：")

print(
    df[df["PWF电力故障"] == 1]["机械功率W"].describe()
)

print("\n正常机器：")

print(
    df[df["PWF电力故障"] == 0]["机械功率W"].describe()
)

df["功率区间"] = pd.cut(
    df["机械功率W"],
    bins=[0, 3500, 9000, 11000],
    labels=["低功率", "正常功率", "高功率"]
)

power_result = df.groupby(
    "功率区间",
    observed=True
)["PWF电力故障"].agg(
    ["count", "sum", "mean"]
)

print(power_result)

df["重点区域"] = (
    (df["转速区间"] == "低转速") &
    (df["扭矩区间"] == "高扭矩")
)
print(df["重点区域"].value_counts())

print(
    df.groupby("重点区域")["Machine failure机器故障"].agg(
        ["count", "sum", "mean"]
    )
)

print(
    df.groupby(
        ["重点区域", "Machine failure机器故障"]
    ).size()
)

table = pd.crosstab(
    df["重点区域"],
    df["Machine failure机器故障"]
)

print(table)

chi2, p, dof, expected = chi2_contingency(table)

print("p值：", p)

重点区域故障 = df[
    (df["重点区域"] == True) &
    (df["Machine failure机器故障"] == 1)
]

print(重点区域故障.shape)


failure_modes = [
    "TWF刀具磨损故障",
    "HDF散热故障",
    "PWF电力故障",
    "OSF过冲 / 突发故障",
    "RNF随机故障"
]


print(
    重点区域故障[failure_modes].sum()
)

print(df.columns.tolist())

hdf_result = df.groupby("重点区域")["HDF散热故障"].agg(
    ["count", "sum", "mean"]
)

print("HDF故障为："+ str(hdf_result))

pwf_result = df.groupby("重点区域")["PWF电力故障"].agg(
    ["count", "sum", "mean"]   )

print("PWF故障为："+ str(pwf_result))

osf_result = df.groupby("重点区域")["OSF过冲 / 突发故障"].agg(
    ["count", "sum", "mean"]    )

print("OSF故障为："+ str(osf_result))   

df["功率W"] = df["Torque [Nm]扭矩"] * (
    2 * 3.14159 * df["Rotational speed [rpm]转速"] / 60
)

df["功率W"] = df["Torque [Nm]扭矩"] * (
    2 * 3.14159 * df["Rotational speed [rpm]转速"] / 60
)

print(df[["Rotational speed [rpm]转速", "Torque [Nm]扭矩", "功率W"]].head())

pwf = df[df["PWF电力故障"] == 1]

print(pwf.shape)
print(pwf["功率W"].describe())

df["功率区间"] = pd.cut(
    df["功率W"],
    bins=[0, 3500, 9000, float("inf")],
    labels=["低功率", "正常功率", "高功率"]
)

result = df.groupby(
    "功率区间",
    observed=True
)["PWF电力故障"].agg(
    ["count", "sum", "mean"]
)

print(result)

重点区域机器 = df[df["重点区域"] == True]

print(
    重点区域机器["功率区间"].value_counts()
)

低功率机器 = df[df["功率区间"] == "低功率"]
print(低功率机器[["功率W", "PWF电力故障"]])

#hdf故障因素查看
#构建温差概念
df["温差K"] = (
    df["Process temperature [K]工艺温度K"]
    - df["Air temperature [K]空气温度K"]
)
print(df[[
    "Air temperature [K]空气温度K",
    "Process temperature [K]工艺温度K",
    "温差K"
]].head())

#观察温差K与HDF散热故障的关系
hdf = df[df["HDF散热故障"] == 1]

normal_hdf = df[df["HDF散热故障"] == 0]

print("HDF故障机器温差：")
print(hdf["温差K"].describe())

print("非HDF故障机器温差：")
print(normal_hdf["温差K"].describe())

#观察是否温差越低，HDF散热故障的概率越高
df["温差区间"] = pd.cut(
    df["温差K"],
    bins=[7.5, 8.6, 9.5, 10.5, 12.2],
    labels=["低温差", "较低温差", "中等温差", "高温差"]
)

result = df.groupby(
    "温差区间",
    observed=True
)["HDF散热故障"].agg(
    ["count", "sum", "mean"]
)

print(result)

hdf = df[df["HDF散热故障"] == 1]
normal_hdf = df[df["HDF散热故障"] == 0]

print("HDF故障机器的空气温度：")
print(hdf["Air temperature [K]空气温度K"].describe())

print("非HDF故障机器的空气温度：")
print(normal_hdf["Air temperature [K]空气温度K"].describe())

#HDF故障机器的工艺温度到底是什么情况
print("HDF故障机器的工艺温度：")
print(hdf["Process temperature [K]工艺温度K"].describe())

print("非HDF故障机器的工艺温度：")
print(normal_hdf["Process temperature [K]工艺温度K"].describe())

#空气温度越高，HDF故障率是不是越高
df["空气温度区间"] = pd.cut(
    df["Air temperature [K]空气温度K"],
    bins=[295, 300, 302, 304, 305],
    labels=["低温", "中低温", "中高温", "高温"]
)

result = df.groupby(
    "空气温度区间",
    observed=True
)["HDF散热故障"].agg(
    ["count", "sum", "mean"]
)

print(result)

# 1. 筛选出低温差机器
低温差机器 = df[df["温差区间"] == "低温差"]

# 2. 按转速区间分组，并统计机器数量、HDF故障数量、HDF故障率
result = 低温差机器.groupby(
    "转速区间",
    observed=True
)["HDF散热故障"].agg(
    ["count", "sum", "mean"]
)

# 3. 输出结果
print(result)

#验证扭矩是否和散热故障有关
低温差低转速 = df[
    (df["温差区间"] == "低温差") &
    (df["转速区间"] == "低转速")
]
print(低温差低转速["Torque [Nm]扭矩"].describe())

# ==============================
# 代码：比较 HDF 故障机器与非故障机器的扭矩
# ==============================

# HDF故障机器
HDF机器 = 低温差低转速[
    低温差低转速["HDF散热故障"] == 1
]

# 非HDF故障机器
非HDF机器 = 低温差低转速[
    低温差低转速["HDF散热故障"] == 0
]

# 查看两组机器的扭矩
print("HDF机器扭矩：")
print(HDF机器["Torque [Nm]扭矩"].describe())

print("\n非HDF机器扭矩：")
print(非HDF机器["Torque [Nm]扭矩"].describe())

# ==========================================
# 代码：在低温差 + 低转速机器中
# 按扭矩区间统计 HDF 故障率
# ==========================================

# 1. 把扭矩分成3个区间
低温差低转速["扭矩区间"] = pd.cut(
    低温差低转速["Torque [Nm]扭矩"],
    bins=3,
    labels=["低扭矩", "中扭矩", "高扭矩"]
)

# 2. 按扭矩区间分组，统计机器数量、HDF故障数量、HDF故障率
result = 低温差低转速.groupby(
    "扭矩区间",
    observed=True
)["HDF散热故障"].agg(
    ["count", "sum", "mean"]
)

# 3. 输出结果
print(result)

# ==========================================
# 代码：比较高扭矩机器中 HDF 与非 HDF 的工艺温度
# ==========================================

# 1. 从低温差 + 低转速机器中筛选出高扭矩机器
高扭矩机器 = 低温差低转速[
    低温差低转速["扭矩区间"] == "高扭矩"
]

# 2. HDF机器
HDF高扭矩 = 高扭矩机器[
    高扭矩机器["HDF散热故障"] == 1
]

# 3. 非HDF机器
非HDF高扭矩 = 高扭矩机器[
    高扭矩机器["HDF散热故障"] == 0
]

# 4. 分别查看工艺温度
print("HDF高扭矩机器的工艺温度：")
print(HDF高扭矩["Process temperature [K]工艺温度K"].describe())

print("\n非HDF高扭矩机器的工艺温度：")
print(非HDF高扭矩["Process temperature [K]工艺温度K"].describe())

# ==========================================
# 代码：按空气温度区间统计 HDF 故障率
# ==========================================

df["空气温度区间2"] = pd.cut(
    df["Air temperature [K]空气温度K"],
    bins=4,
    labels=["低空气温度", "中低空气温度", "中高空气温度", "高空气温度"]
)

result = df.groupby(
    "空气温度区间2",
    observed=True
)["HDF散热故障"].agg(
    ["count", "sum", "mean"]
)

print(result)

# ==========================================
# 代码：查看机械功率的基本分布
# ==========================================

print(df["功率W"].describe())

# ==========================================
# 代码：按机械功率区间探索 HDF 故障率
# ==========================================

df["功率探索区间"] = pd.cut(
    df["功率W"],
    bins=5,
    labels=["很低功率", "较低功率", "中等功率", "较高功率", "很高功率"]
)

result = df.groupby(
    "功率探索区间",
    observed=True
)["HDF散热故障"].agg(
    ["count", "sum", "mean"]
)

print(result)

# ==========================================
# 代码：划分空气温度区间
# ==========================================

df["空气温度区间3"] = pd.cut(
    df["Air temperature [K]空气温度K"],
    bins=3,
    labels=["低空气温度", "中空气温度", "高空气温度"]
)

# ==========================================
# 代码：划分机械功率区间
# ==========================================

df["功率区间3"] = pd.cut(
    df["功率W"],
    bins=3,
    labels=["低功率", "中功率", "高功率"]
)

# ==========================================
# 代码：检查空气温度和功率分组
# ==========================================

print(df["空气温度区间3"].value_counts())
print()
print(df["功率区间3"].value_counts())

# ==========================================
# 代码：按照空气温度和功率同时分组
# ==========================================

print(df.groupby(
    ["空气温度区间3", "功率区间3"]
)["HDF散热故障"].agg(["count", "sum", "mean"]))

# ==========================================
# 代码：比较不同空气温度下高功率机器的温差
# ==========================================

中温高功率 = df[
    (df["空气温度区间3"] == "中空气温度") &
    (df["功率区间3"] == "高功率")
]

高温高功率 = df[
    (df["空气温度区间3"] == "高空气温度") &
    (df["功率区间3"] == "高功率")
]

print("中温 + 高功率机器的温差：")
print(中温高功率["温差K"].describe())

print("\n高温 + 高功率机器的温差：")
print(高温高功率["温差K"].describe())

# ==========================================
# 代码：筛选高功率机器
# ==========================================

高功率机器 = df[df["功率区间3"] == "高功率"]

print(高功率机器.shape)


print(高功率机器.groupby(
    "空气温度区间3"
)["HDF散热故障"].agg(
    ["count", "sum", "mean"]
))  

# ==========================================
# 代码：建立高功率机器的空气温度 × HDF交叉表
# ==========================================

table = pd.crosstab(
    高功率机器["空气温度区间3"],
    高功率机器["HDF散热故障"]
)

print(table)

# ==========================================
# 代码：检验高功率条件下
# 空气温度与 HDF 是否存在统计关联
# ==========================================

from scipy.stats import chi2_contingency

chi2, p, dof, expected = chi2_contingency(table)

print("卡方统计量：", chi2)
print("p值：", p)

# ==========================================
# 代码：查看当前数据的所有列
# ==========================================

print(df.columns.tolist())

# ==========================================
# 代码：比较 OSF 与非 OSF 机器的基本特征
# ==========================================

OSF机器 = df[df["OSF过冲 / 突发故障"] == 1]
非OSF机器 = df[df["OSF过冲 / 突发故障"] == 0]

变量 = [
    "Torque [Nm]扭矩",
    "Tool wear [min]刀具磨损",
    "Rotational speed [rpm]转速",
    "功率W"
]

print("OSF机器：")
print(OSF机器[变量].describe())

print("\n非OSF机器：")
print(非OSF机器[变量].describe())

# ==========================================
# 代码：划分扭矩和刀具磨损区间
# ==========================================

df["OSF扭矩区间"] = pd.cut(
    df["Torque [Nm]扭矩"],
    bins=3,
    labels=["低扭矩", "中扭矩", "高扭矩"]
)

df["OSF磨损区间"] = pd.cut(
    df["Tool wear [min]刀具磨损"],
    bins=3,
    labels=["低磨损", "中磨损", "高磨损"]
)

# ==========================================
# 代码：统计不同扭矩 × 刀具磨损组合的 OSF 故障率
# ==========================================

result = df.groupby(
    ["OSF扭矩区间", "OSF磨损区间"],
    observed=True
)["OSF过冲 / 突发故障"].agg(
    ["count", "sum", "mean"]
)

print(result)

# ==========================================
# 代码：标记高扭矩 + 高磨损区域
# ==========================================

df["OSF重点区域"] = (
    (df["OSF扭矩区间"] == "高扭矩") &
    (df["OSF磨损区间"] == "高磨损")
)

print(df["OSF重点区域"].value_counts())

# ==========================================
# 代码：比较重点区域与其他机器的 OSF 故障率
# ==========================================

result = df.groupby(
    "OSF重点区域"
)["OSF过冲 / 突发故障"].agg(
    ["count", "sum", "mean"]
)

print(result)

# ==========================================
# 代码：建立 OSF 重点区域交叉表
# ==========================================

table = pd.crosstab(
    df["OSF重点区域"],
    df["OSF过冲 / 突发故障"]
)

print(table)

# ==========================================
# 代码：卡方检验 OSF重点区域与故障的关联
# ==========================================

from scipy.stats import chi2_contingency

chi2, p, dof, expected = chi2_contingency(table)

print("卡方统计量：", chi2)
print("p值：", p)

# ==========================================
# 代码：单独分析扭矩与 OSF 的关系
# ==========================================

result = df.groupby(
    "OSF扭矩区间",
    observed=True
)["OSF过冲 / 突发故障"].agg(
    ["count", "sum", "mean"]
)

print(result)

# ==========================================
# 代码：单独分析刀具磨损与 OSF 的关系
# ==========================================

result = df.groupby(
    "OSF磨损区间",
    observed=True
)["OSF过冲 / 突发故障"].agg(
    ["count", "sum", "mean"]
)

print(result)

# ==========================================
# 代码：查看高扭矩 + 高磨损区域中
# 不同产品类型的 OSF 故障率
# ==========================================

重点区域数据 = df[
    df["OSF重点区域"] == True
]

result = 重点区域数据.groupby(
    "Type设备类型"
)["OSF过冲 / 突发故障"].agg(
    ["count", "sum", "mean"]
)

print(result)

# ==========================================
# 代码：比较不同产品类型的整体 OSF 故障率
# ==========================================

result = df.groupby(
    "Type设备类型"
)["OSF过冲 / 突发故障"].agg(
    ["count", "sum", "mean"]
)

print(result)

# ==========================================
# 代码：计算扭矩 × 刀具磨损
# ==========================================

df["扭矩磨损指标"] = (
    df["Torque [Nm]扭矩"] *
    df["Tool wear [min]刀具磨损"]
)

print(df["扭矩磨损指标"].describe())

# ==========================================
# 代码：比较 OSF 与非 OSF 的扭矩磨损指标
# ==========================================

OSF机器 = df[df["OSF过冲 / 突发故障"] == 1]

非OSF机器 = df[df["OSF过冲 / 突发故障"] == 0]

print("OSF机器：")
print(OSF机器["扭矩磨损指标"].describe())

print("\n非OSF机器：")
print(非OSF机器["扭矩磨损指标"].describe())

PWF机器 = df[
    df["PWF电力故障"] == 1
]

print(PWF机器["功率W"].sort_values().to_string(index=False))

# ==========================================
# 代码：查看 PWF 边界附近的所有机器
# ==========================================

低功率区域 = df[
    (df["功率W"] >= 3000) &
    (df["功率W"] <= 4000)
]

print("===== 3000~4000 W =====")
print(
    低功率区域[
        ["功率W", "PWF电力故障"]
    ].sort_values("功率W").to_string(index=False)
)


高功率区域 = df[
    (df["功率W"] >= 8500) &
    (df["功率W"] <= 9200)
]

print("\n===== 8500~9200 W =====")
print(
    高功率区域[
        ["功率W", "PWF电力故障"]
    ].sort_values("功率W").to_string(index=False)
)

低功率边界 = (3477.237476 + 3515.030803) / 2
高功率边界 = (8998.016414 + 9004.425258) / 2

print("低功率候选边界：", 低功率边界)
print("高功率候选边界：", 高功率边界)

# ==========================================
# 根据我们发现的边界，预测 PWF
# ==========================================

df["PWF预测"] = (
    (df["功率W"] < 3496.1341395) |
    (df["功率W"] > 9001.220836)
).astype(int)

print(
    pd.crosstab(
        df["PWF电力故障"],
        df["PWF预测"]
    )
)

# ==========================================
# 查看我们预测为 PWF 的机器
# ==========================================

预测PWF机器 = df[
    df["PWF预测"] == 1
]

print(
    预测PWF机器[
        ["功率W", "PWF电力故障"]
    ]
    .sort_values("功率W")
    .to_string(index=False)
)

df["OSF高指标区域"] = (
    df["扭矩磨损指标"] >= 11000
)

result = df.groupby(
    "OSF高指标区域"
)["OSF过冲 / 突发故障"].agg(
    ["count", "sum", "mean"]
)

print(result)


result = df.groupby(
    ["转速区间", "扭矩区间"],
    observed=True
)["PWF电力故障"].agg(
    ["count", "sum", "mean"]
)

print(result)

# ==================================================
# OSF分析：寻找高扭矩×高磨损但没有发生OSF的机器
# ==================================================

特殊机器 = df[
    (df["扭矩磨损指标"] >= 11000) &
    (df["OSF过冲 / 突发故障"] == 0)
]

# ==================================================
# 终端输出：特殊机器的关键变量
# ==================================================

print("\n========== OSF分析：高指标但未发生OSF的机器 ==========")

print(
    特殊机器[
        [
            "Type设备类型",
            "Air temperature [K]空气温度K",
            "Process temperature [K]工艺温度K",
            "Rotational speed [rpm]转速",
            "Torque [Nm]扭矩",
            "Tool wear [min]刀具磨损",
            "功率W",
            "扭矩磨损指标"
        ]
    ]
)

# ==================================================
# OSF分析：不同刀具磨损程度下，扭矩与OSF的关系
# ==================================================

# 把刀具磨损分成三组
df["刀具磨损区间"] = pd.cut(
    df["Tool wear [min]刀具磨损"],
    bins=[-1, 100, 200, 300],
    labels=["低磨损", "中磨损", "高磨损"]
)

# 把扭矩分成三组
df["扭矩区间"] = pd.cut(
    df["Torque [Nm]扭矩"],
    bins=[-1, 40, 50, 100],
    labels=["低扭矩", "中扭矩", "高扭矩"]
)

# ==================================================
# 终端输出：不同磨损 × 扭矩下的OSF情况
# ==================================================

print("\n========== 不同刀具磨损 × 扭矩下的OSF ==========")

result = df.groupby(
    ["刀具磨损区间", "扭矩区间"],
    observed=True
)["OSF过冲 / 突发故障"].agg(
    ["count", "sum", "mean"]
)

print(result)

# ==================================================
# OSF分析：扭矩磨损指标与OSF的卡方检验
# ==================================================

from scipy.stats import chi2_contingency

# 根据11000划分高风险区域
df["OSF高指标区域"] = (
    df["扭矩磨损指标"] >= 11000
).astype(int)

# ==================================================
# 终端输出：卡方检验
# ==================================================

print("\n========== 扭矩磨损指标 × OSF 卡方检验 ==========")

# 建立列联表
table = pd.crosstab(
    df["OSF高指标区域"],
    df["OSF过冲 / 突发故障"]
)

print("\n列联表：")
print(table)

# 进行卡方检验
chi2, p, dof, expected = chi2_contingency(table)

print("\n卡方统计量：", chi2)
print("p值：", p)
print("自由度：", dof)

# ==================================================
# 产品类型分析：不同Type的机器故障率
# ==================================================

print("\n========== 不同产品类型的机器故障率 ==========")

result = df.groupby(
    "Type设备类型"
)["Machine failure机器故障"].agg(
    ["count", "sum", "mean"]
)

print(result)

# ==================================================
# 产品类型分析：Type与Machine Failure的卡方检验
# ==================================================

from scipy.stats import chi2_contingency

# ==================================================
# 终端输出：Type × Machine Failure
# ==================================================

print("\n========== 产品类型 × 机器故障卡方检验 ==========")

table = pd.crosstab(
    df["Type设备类型"],
    df["Machine failure机器故障"]
)

print("\n列联表：")
print(table)

chi2, p, dof, expected = chi2_contingency(table)

print("\n卡方统计量：", chi2)
print("p值：", p)
print("自由度：", dof)

# ==================================================
# 产品类型分析：Type与各类故障的关系
# ==================================================

from scipy.stats import chi2_contingency

故障类型 = [
    "PWF电力故障",
    "HDF散热故障",
    "OSF过冲 / 突发故障",
    "TWF刀具磨损故障"
]

# ==================================================
# 终端输出：Type × 各类故障
# ==================================================

print("\n========== 产品类型 × 各类故障分析 ==========")

for 故障 in 故障类型:

    print(f"\n--- Type × {故障} ---")

    table = pd.crosstab(
        df["Type设备类型"],
        df[故障]
    )

    print(table)

    chi2, p, dof, expected = chi2_contingency(table)

    print("卡方统计量：", chi2)
    print("p值：", p)

