-- 设备表：对应 ai4i2020.csv 的原始字段
CREATE TABLE IF NOT EXISTS machines (
    udi INTEGER PRIMARY KEY,
    product_id VARCHAR(20) NOT NULL,
    type CHAR(1) NOT NULL,
    air_temp_k NUMERIC(6,2) NOT NULL,
    process_temp_k NUMERIC(6,2) NOT NULL,
    rotational_speed_rpm INTEGER NOT NULL,
    torque_nm NUMERIC(6,2) NOT NULL,
    tool_wear_min INTEGER NOT NULL,
    machine_failure BOOLEAN NOT NULL,
    twf BOOLEAN NOT NULL,
    hdf BOOLEAN NOT NULL,
    pwf BOOLEAN NOT NULL,
    osf BOOLEAN NOT NULL,
    rnf BOOLEAN NOT NULL
);

-- 工单表：故障处理工单
CREATE TABLE IF NOT EXISTS tickets (
    id SERIAL PRIMARY KEY,
    machine_id INTEGER NOT NULL REFERENCES machines(udi),
    description TEXT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'open',
    priority VARCHAR(10) NOT NULL DEFAULT 'medium',
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    resolved_at TIMESTAMP NULL
);
