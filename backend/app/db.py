import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_engine(DATABASE_URL)


def run_query(sql: str, params: dict | None = None) -> list[dict]:
    """执行 SELECT，返回 list[dict]。sql 必须用 :name 占位符，params 传实际值，禁止手动拼接字符串。"""
    with engine.connect() as conn:
        result = conn.execute(text(sql), params or {})
        return [dict(row._mapping) for row in result]


def run_execute(sql: str, params: dict | None = None) -> list[dict]:
    """执行 INSERT/UPDATE/DELETE，自动 commit。若带 RETURNING，返回 list[dict]，否则返回空列表。"""
    with engine.begin() as conn:
        result = conn.execute(text(sql), params or {})
        if result.returns_rows:
            return [dict(row._mapping) for row in result]
        return []
