from sentence_transformers import SentenceTransformer
import psycopg2
from pgvector.psycopg2 import register_vector
import re

#  Lấy thông tin từ config.py
from config import Config

def get_connection():
    uri = Config.SQLALCHEMY_DATABASE_URI
    # Tách các phần của chuỗi postgresql://user:pass@host:port/dbname
    pattern = r"postgresql://(.*?):(.*?)@(.*?):(\d+)/(.*)"
    match = re.match(pattern, uri)
    if not match:
        raise ValueError(" Chuỗi kết nối trong Config không hợp lệ!")
    user, password, host, port, dbname = match.groups()

    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    register_vector(conn)
    return conn

def main():
    print(" Đang sinh embedding cho sản phẩm...")

    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, description, brand, chipset, ram, storage FROM product")
    rows = cur.fetchall()

    for pid, name, desc, brand, chip, ram, storage in rows:
        text = f"{name} {brand or ''} {chip or ''} {ram or ''} {storage or ''} {desc or ''}"
        emb = model.encode(text).tolist()
        cur.execute("UPDATE product SET embedding = %s WHERE id = %s", (emb, pid))

    conn.commit()
    cur.close()
    conn.close()
    print(" Hoàn tất: đã cập nhật embedding cho toàn bộ sản phẩm!")

if __name__ == "__main__":
    main()
