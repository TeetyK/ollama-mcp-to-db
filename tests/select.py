import json
import psycopg2

def read_database(sql_query: str ,**DB_CONFIG) -> str:
    """รับค่าที่เป็น ค้นหาข้อมูล โดยที่ใช้ Query SELECT"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute(sql_query)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return json.dumps(rows, ensure_ascii=False , default=str)
    except Exception as e:
        return f"Error query : {e}"