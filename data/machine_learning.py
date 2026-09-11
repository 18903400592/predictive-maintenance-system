import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression

# 读取原始数据
df = pd.read_csv("ai4i2020.csv")

# 和之前的数据分析保持完全一样的列名
df.columns = [
    "UDI设备编号",
    "Product ID产品编号",
    "Type设备类型",
    "Air temperature [K]空气温度K",
    "Process temperature [K]工艺温度K",
    "Rotational speed [rpm]转速",
    "Torque [Nm]扭矩",
    "Tool wear [min]刀具磨损",
    "Machine failure机器故障",
    "TWF刀具磨损故障",
    "HDF散热故障",
    "PWF电力故障",
    "OSF过冲 / 突发故障",
    "RNF随机故障"
]

print("========== 数据检查 ==========")
print(df.shape)
print(df.columns.tolist())
print(df.head())

# ==================== 构建 X 和 y ====================

X = df[
    [
        "Type设备类型",
        "Air temperature [K]空气温度K",
        "Process temperature [K]工艺温度K",
        "Rotational speed [rpm]转速",
        "Torque [Nm]扭矩",
        "Tool wear [min]刀具磨损"
    ]
]

y = df["Machine failure机器故障"]

print("========== X 和 y 检查 ==========")
print("X的形状：", X.shape)
print("y的形状：", y.shape)

print("\nX的前5行：")
print(X.head())

print("\ny的前5行：")
print(y.head())

# ==================== 划分训练集和测试集 ====================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


print("\n========== 训练集和测试集 ==========")
print("X_train：", X_train.shape)
print("X_test：", X_test.shape)
print("y_train：", y_train.shape)
print("y_test：", y_test.shape)


# ==================== 处理设备类型 ====================

encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)

type_train = encoder.fit_transform(X_train[["Type设备类型"]])
type_test = encoder.transform(X_test[["Type设备类型"]])

print("\n========== Type 编码 ==========")
print("编码后的训练集：")
print(type_train[:5])

print("\n类别顺序：")
print(encoder.categories_)

# ==================== 组合最终的 X ====================

X_train_numeric = X_train.drop(columns=["Type设备类型"])
X_test_numeric = X_test.drop(columns=["Type设备类型"])

X_train_final = pd.concat(
    [
        X_train_numeric.reset_index(drop=True),
        pd.DataFrame(type_train, columns=["Type_H", "Type_L", "Type_M"])
    ],
    axis=1
)

X_test_final = pd.concat(
    [
        X_test_numeric.reset_index(drop=True),
        pd.DataFrame(type_test, columns=["Type_H", "Type_L", "Type_M"])
    ],
    axis=1
)

print("\n========== 最终 X ==========")
print("X_train_final：", X_train_final.shape)
print("X_test_final：", X_test_final.shape)

print("\n最终 X 的前5行：")
print(X_train_final.head())

# ==================== Logistic Regression ====================

model = LogisticRegression(max_iter=1000)

model.fit(X_train_final, y_train)

print("\n========== 模型训练完成 ==========")

# ==================== 模型预测 ====================

y_pred = model.predict(X_test_final)

print("\n========== 预测结果 ==========")
print(y_pred[:20])

print("\n========== 预测类别数量 ==========")
print(pd.Series(y_pred).value_counts())

from sklearn.metrics import confusion_matrix

cm = confusion_matrix(y_test, y_pred)

print("\n========== 混淆矩阵 ==========")
print(cm)

from sklearn.metrics import accuracy_score

accuracy = accuracy_score(y_test, y_pred)

print("\n========== Accuracy ==========")
print("准确率：", accuracy)

y_prob = model.predict_proba(X_test_final)[:, 1]

print("\n========== 故障概率 ==========")
print(y_prob[:20])

# ==================== 改变预测阈值 ====================

threshold = 0.05

y_pred_new = (y_prob >= threshold).astype(int)

print("\n========== 新阈值预测 ==========")
print("阈值：", threshold)
print(pd.Series(y_pred_new).value_counts())

# ==================== 划分训练集和验证集 ====================

X_train_new, X_val, y_train_new, y_val = train_test_split(
    X_train,
    y_train,
    test_size=0.2,
    random_state=42,
    stratify=y_train
)

print("\n========== Train / Validation / Test ==========")
print("训练集：", X_train_new.shape)
print("验证集：", X_val.shape)
print("测试集：", X_test.shape)

print("\n========== 三份数据的故障比例 ==========")

print("训练集故障率：", y_train_new.mean())
print("验证集故障率：", y_val.mean())
print("测试集故障率：", y_test.mean())

# ==================== 重新进行 Type 编码 ====================

encoder_new = OneHotEncoder(
    handle_unknown="ignore",
    sparse_output=False
)

type_train_new = encoder_new.fit_transform(
    X_train_new[["Type设备类型"]]
)

type_val_new = encoder_new.transform(
    X_val[["Type设备类型"]]
)

type_test_new = encoder_new.transform(
    X_test[["Type设备类型"]]
)

print("\n========== 新的 Type 编码 ==========")
print("类别顺序：", encoder_new.categories_)

# ==================== 组合新的 X ====================

X_train_numeric_new = X_train_new.drop(
    columns=["Type设备类型"]
)

X_val_numeric = X_val.drop(
    columns=["Type设备类型"]
)

X_test_numeric_new = X_test.drop(
    columns=["Type设备类型"]
)

X_train_final_new = pd.concat(
    [
        X_train_numeric_new.reset_index(drop=True),
        pd.DataFrame(
            type_train_new,
            columns=["Type_H", "Type_L", "Type_M"]
        )
    ],
    axis=1
)

X_val_final = pd.concat(
    [
        X_val_numeric.reset_index(drop=True),
        pd.DataFrame(
            type_val_new,
            columns=["Type_H", "Type_L", "Type_M"]
        )
    ],
    axis=1
)

X_test_final_new = pd.concat(
    [
        X_test_numeric_new.reset_index(drop=True),
        pd.DataFrame(
            type_test_new,
            columns=["Type_H", "Type_L", "Type_M"]
        )
    ],
    axis=1
)

print("\n========== 新的最终 X ==========")
print("训练集：", X_train_final_new.shape)
print("验证集：", X_val_final.shape)
print("测试集：", X_test_final_new.shape)

print("\n训练集前5行：")
print(X_train_final_new.head())

# ==================== Logistic Regression ====================

model = LogisticRegression(max_iter=1000)

model.fit(
    X_train_final_new,
    y_train_new
)

print("\n========== 新模型训练完成 ==========")

# ==================== Validation 风险预测 ====================

y_val_prob = model.predict_proba(X_val_final)[:, 1]

print("\n========== Validation 故障风险 ==========")
print(y_val_prob[:20])

# ==================== 比较两个阈值 ====================

for threshold in [0.5, 0.05]:

    y_val_pred = (y_val_prob >= threshold).astype(int)

    print("\n阈值：", threshold)
    print("预测正常数量：", (y_val_pred == 0).sum())
    print("预测故障数量：", (y_val_pred == 1).sum())

    from sklearn.metrics import confusion_matrix

threshold = 0.5

y_val_pred = (y_val_prob >= threshold).astype(int)

cm = confusion_matrix(y_val, y_val_pred)

print("\n========== Validation 混淆矩阵 ==========")
print(cm)

from sklearn.metrics import confusion_matrix

for threshold in [0.5, 0.05]:

    y_val_pred = (y_val_prob >= threshold).astype(int)

    cm = confusion_matrix(y_val, y_val_pred)

    TN, FP, FN, TP = cm.ravel()

    recall = TP / (TP + FN)
    precision = TP / (TP + FP)

    print("\n========== 阈值：", threshold, "==========")
    print("TP：", TP)
    print("FP：", FP)
    print("FN：", FN)
    print("Recall：", recall)
    print("Precision：", precision)

thresholds = [0.025, 0.026, 0.027, 0.028, 0.029,
              0.030, 0.031, 0.032, 0.033, 0.034, 0.035]

for threshold in thresholds:

    y_val_pred = (y_val_prob >= threshold).astype(int)

    cm = confusion_matrix(y_val, y_val_pred)

    TN, FP, FN, TP = cm.ravel()

    recall = TP / (TP + FN)
    precision = TP / (TP + FP)

    print(
        "阈值：", threshold,
        "Recall：", round(recall, 3),
        "Precision：", round(precision, 3)
    )

threshold = 0.031

y_val_pred = (y_val_prob >= threshold).astype(int)

cm = confusion_matrix(y_val, y_val_pred)

print(cm)

false_positive = X_val[
    (y_val == 0) & (y_val_pred == 1)
]

print(false_positive.shape)
print(false_positive.head())

# 计算误报机器中各个数值变量的平均值
# mean() 会分别计算每一列的平均值
print(false_positive.mean(numeric_only=True))

# 计算 Validation 集中实际正常机器的平均值
# y_val == 0 表示这些机器实际上没有发生故障
normal_val = X_val[y_val == 0]

print(normal_val.mean(numeric_only=True))

# 判断每台机器是否属于高扭矩
# 使用 Validation 数据中的 3 等分区间
torque_high = X_val["Torque [Nm]扭矩"] >= X_val["Torque [Nm]扭矩"].quantile(2/3)

# 判断每台机器是否属于高刀具磨损
# 同样使用 2/3 分位数作为“高磨损”的划分标准
wear_high = X_val["Tool wear [min]刀具磨损"] >= X_val["Tool wear [min]刀具磨损"].quantile(2/3)

# 在291台误报机器中，同时满足“高扭矩 + 高磨损”的机器
fp_high = false_positive[
    torque_high.loc[false_positive.index] &
    wear_high.loc[false_positive.index]
]

# 查看数量
print("误报机器总数：", len(false_positive))
print("高扭矩 + 高磨损的误报机器：", len(fp_high))

# 计算它们占全部误报的比例
print(
    "占比：",
    len(fp_high) / len(false_positive)
)

# 找出真正正常，并且模型也正确判断为正常的机器
true_negative = X_val[
    (y_val == 0) & (y_val_pred == 0)
]

# 计算正确判断为正常的机器中，
# 有多少台同时属于“高扭矩 + 高刀具磨损”
tn_high = true_negative[
    torque_high.loc[true_negative.index] &
    wear_high.loc[true_negative.index]
]

# 输出两组数据进行比较
print("误报机器总数：", len(false_positive))
print("误报中高扭矩 + 高磨损：", len(fp_high))
print("误报中占比：", len(fp_high) / len(false_positive))

print()

print("正确判断正常机器总数：", len(true_negative))
print("正确判断正常中高扭矩 + 高磨损：", len(tn_high))
print("正确判断正常中占比：", len(tn_high) / len(true_negative))

# ==============================
# 分析误报机器的扭矩 × 刀具磨损组合
# ==============================

# 根据前面已经计算好的“高扭矩”和“高磨损”结果，
# 把每台误报机器分成四种组合

fp_torque_wear = pd.DataFrame({
    "扭矩水平": torque_high.loc[false_positive.index].map(
        {
            True: "高扭矩",
            False: "低扭矩"
        }
    ),
    "磨损水平": wear_high.loc[false_positive.index].map(
        {
            True: "高磨损",
            False: "低磨损"
        }
    )
})

# 统计四种组合分别有多少台误报机器
print("误报机器的扭矩 × 磨损分组：")

print(
    fp_torque_wear.groupby(
        ["扭矩水平", "磨损水平"]
    ).size()
)

# ==============================
# 分析正确判断正常机器的扭矩 × 刀具磨损组合
# ==============================

# 对真正正常、并且模型也判断为正常的机器进行同样的分组
# 这样我们才能和误报机器进行公平比较

tn_torque_wear = pd.DataFrame({
    "扭矩水平": torque_high.loc[true_negative.index].map(
        {
            True: "高扭矩",
            False: "低扭矩"
        }
    ),
    "磨损水平": wear_high.loc[true_negative.index].map(
        {
            True: "高磨损",
            False: "低磨损"
        }
    )
})

# 统计四种组合分别有多少台正确判断正常的机器
print("正确判断正常机器的扭矩 × 磨损分组：")

print(
    tn_torque_wear.groupby(
        ["扭矩水平", "磨损水平"]
    ).size()
)

# ==============================
# 计算四种组合的实际误报率
# ==============================

# 先给 Validation 中的每台机器标记：
# 它属于哪一种“扭矩 × 磨损”组合
all_torque_wear = pd.DataFrame({
    "扭矩水平": torque_high.map(
        {
            True: "高扭矩",
            False: "低扭矩"
        }
    ),
    "磨损水平": wear_high.map(
        {
            True: "高磨损",
            False: "低磨损"
        }
    ),
    # 标记这台机器是否属于误报
    "是否误报": (
        (y_val == 0) & (y_val_pred == 1)
    )
})

# 按照四种组合进行统计
result = all_torque_wear.groupby(
    ["扭矩水平", "磨损水平"]
)["是否误报"].agg(
    ["count", "sum", "mean"]
)

# 修改列名，让结果更容易理解
result.columns = [
    "机器总数",
    "误报数量",
    "误报率"
]

print(result)