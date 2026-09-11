import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]

CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "ai4i2020.csv")

# CSV 表头是中英混合列名，这里映射到 machines 表的英文 snake_case 字段
COLUMN_MAP = {
    "UDI设备编号": "udi",
    "Product ID产品编号": "product_id",
    "Type设备类型": "type",
    "Air temperature [K]空气温度K": "air_temp_k",
    "Process temperature [K]工艺温度K": "process_temp_k",
    "Rotational speed [rpm]转速": "rotational_speed_rpm",
    "Torque [Nm]扭矩": "torque_nm",
    "Tool wear [min]刀具磨损": "tool_wear_min",
    "Machine failure机器故障": "machine_failure",
    "TWF刀具磨损故障": "twf",
    "HDF散热故障": "hdf",
    "PWF电力故障": "pwf",
    "OSF过冲 / 突发故障": "osf",
    "RNF随机故障": "rnf",
}

BOOL_COLUMNS = ["machine_failure", "twf", "hdf", "pwf", "osf", "rnf"]


INSERT_SQL = text(
    """
    INSERT INTO machines (
        udi, product_id, type, air_temp_k, process_temp_k,
        rotational_speed_rpm, torque_nm, tool_wear_min,
        machine_failure, twf, hdf, pwf, osf, rnf
    ) VALUES (
        :udi, :product_id, :type, :air_temp_k, :process_temp_k,
        :rotational_speed_rpm, :torque_nm, :tool_wear_min,
        :machine_failure, :twf, :hdf, :pwf, :osf, :rnf
    )
    ON CONFLICT (udi) DO NOTHING
    """
)


def load_data(engine, batch_size: int = 500) -> int:
    """从 CSV 加载设备数据到 machines 表，按 udi 去重（重复 udi 会被跳过）。返回处理的记录总数。"""
    df = pd.read_csv(CSV_PATH)
    df = df.rename(columns=COLUMN_MAP)

    missing = set(COLUMN_MAP.values()) - set(df.columns)
    if missing:
        raise ValueError(f"CSV 缺少字段: {missing}")

    for col in BOOL_COLUMNS:
        df[col] = df[col].astype(bool)

    records = df[list(COLUMN_MAP.values())].to_dict(orient="records")

    with engine.begin() as conn:
        # 分批插入，避免一次向云端数据库发送 10,000 条记录
        for i in range(0, len(records), batch_size):
            batch = records[i:i + batch_size]
            conn.execute(INSERT_SQL, batch)
            print(f"已插入 {min(i + batch_size, len(records))}/{len(records)} 条记录")

    return len(records)


def main():
    engine = create_engine(DATABASE_URL)
    count = load_data(engine)
    print(f"已处理 {count} 条记录（重复 udi 会被跳过）")


if __name__ == "__main__":
    main()
