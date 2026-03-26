import psycopg2
import json
from dotenv import load_dotenv
import os
load_dotenv()

DB_CONFIG = {
    "dbname":os.getenv("dbname"),
    "user":os.getenv("user"),
    "password":os.getenv("password"),
    "host":os.getenv("host"),
    "port":os.getenv("port")
}

def read_database(sql_query: str) -> str:
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute(sql_query)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return json.dumps(rows, ensure_ascii=False, default=str)
    except Exception as e:
        return f"Error executing query: {e}"

def modify_database(sql_query: str) -> str:
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute(sql_query)
        affected_rows = cur.rowcount
        conn.commit()
        cur.close()
        conn.close()
        return f"Success: Modified {affected_rows} rows."
    except Exception as e:
        return f"Error executing query: {e}"

tools_schema = [
    {
        "type": "function",
        "function": {
            "name": "read_database",
            "description": "ใช้สำหรับค้นหาและอ่านข้อมูลจาก PostgreSQL Database (SELECT queries) เท่านั้น",
            "parameters": {
                "type": "object",
                "properties": {
                    "sql_query": {"type": "string", "description": "คำสั่ง SQL SELECT ที่ถูกต้อง"}
                },
                "required": ["sql_query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "modify_database",
            "description": "ใช้สำหรับแก้ไข อัปเดต หรือลบข้อมูลใน PostgreSQL Database (UPDATE, DELETE, INSERT queries)",
            "parameters": {
                "type": "object",
                "properties": {
                    "sql_query": {"type": "string", "description": "คำสั่ง SQL UPDATE หรือ DELETE ที่ถูกต้อง"}
                },
                "required": ["sql_query"],
            },
        },
    }
]