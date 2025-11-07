import time
import psycopg2
from sentence_transformers import SentenceTransformer
from functools import lru_cache
from fastapi import FastAPI, Query

# 1️⃣ Load model tạo embedding
model = SentenceTransformer("BAAI/bge-large-en-v1.5")

app = FastAPI(title="Product Search API")

# 2️⃣ Cache embedding để tăng tốc độ xử lý
@lru_cache(maxsize=500)
def get_embedding(text: str):
    return model.encode(text, normalize_embeddings=True).tolist()

# 3️⃣ Hàm kết nối database
def get_connection():
    return psycopg2.connect(
        host="localhost",
        port=5432,
        database="shop_db",
        user="postgres",
        password="123456"
    )

# 4️⃣ Hàm tạo đoạn văn mô tả sản phẩm để so sánh ngữ nghĩa tốt hơn
def build_product_text(row):
    """
    row gồm: name, description, category, brand, chipset, ram, storage,
             battery, screen_size, weight, performance_score, release_year, price
    """
    (
        name, description, category, brand, chipset, ram, storage,
        battery, screen_size, weight, performance_score, release_year, price
    ) = row

    # Xử lý nếu giá trị None
    def safe(x): return x if x not in (None, '') else "unknown"

    return f"""
    Product name: {safe(name)}.
    Description: {safe(description)}.
    Category: {safe(category)}.
    Brand: {safe(brand)}.
    Chipset: {safe(chipset)}.
    RAM: {safe(ram)}.
    Storage: {safe(storage)}.
    Battery: {safe(battery)} mAh.
    Screen size: {safe(screen_size)} inches.
    Weight: {safe(weight)} grams.
    Performance score: {safe(performance_score)}.
    Release year: {safe(release_year)}.
    Price: {safe(price)} dollars.
    """

# 5️⃣ API tìm kiếm sản phẩm bằng vector similarity
@app.get("/search_products")
def search_products(keyword: str = Query(..., description="Từ khóa tìm sản phẩm")):
    # Tạo embedding cho truy vấn người dùng
    query_text = f"Tìm sản phẩm có đặc điểm: {keyword}"
    query_emb = get_embedding(query_text)

    conn = get_connection()
    cur = conn.cursor()

    start_time = time.time()

    # Lấy thông tin đầy đủ (để hiển thị & ghép text)
    cur.execute("""
        SELECT id, name, price, image_url, description, category, brand,
               chipset, ram, storage, battery, screen_size, weight,
               performance_score, release_year,
               embedding <=> %s::vector AS distance
        FROM public.product
        WHERE embedding IS NOT NULL
        ORDER BY embedding <=> %s::vector
        LIMIT 10;
    """, (query_emb, query_emb))

    rows = cur.fetchall()
    end_time = time.time()

    cur.close()
    conn.close()

    # Chuẩn hóa dữ liệu trả về
    output = []
    for r in rows:
        output.append({
            "id": r[0],
            "name": r[1],
            "price": float(r[2]) if r[2] else 0.0,
            "image_url": r[3],
            "description": r[4],
            "category": r[5],
            "brand": r[6],
            "chipset": r[7],
            "ram": r[8],
            "storage": r[9],
            "battery": r[10],
            "screen_size": r[11],
            "weight": r[12],
            "performance_score": r[13],
            "release_year": r[14],
            "distance": float(r[15])
        })

    return {
        "query": keyword,
        "results": output,
        "time_ms": round((end_time - start_time) * 1000, 2),
        "total_found": len(output)
    }

print("🚀 Product Search API is running with full semantic product info!")
