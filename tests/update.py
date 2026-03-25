import json
import psycopg2

def modify_database(sql_query:str , **DB_CONFIG) -> str:
    """Modify database"""
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
        return f"Error executing query : {e}"
    