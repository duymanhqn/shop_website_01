from models.models import db
from sqlalchemy import text
import re, unicodedata


# ===== Lấy danh sách sản phẩm =====
def get_all_products():
    result = db.session.execute(text("""
        SELECT id, name, description, price, brand, chipset, ram, storage, battery,
               screen_size, performance_score, release_year, weight
        FROM product;
    """))
    rows = result.fetchall()
    cols = ["id", "name", "description", "price", "brand", "chipset", "ram",
            "storage", "battery", "screen_size", "performance_score", "release_year", "weight"]
    return [dict(zip(cols, r)) for r in rows]


# ===== Chuẩn hóa văn bản =====
def normalize_text(text):
    if not text:
        return ""
    text = text.lower().strip()
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text


# ===== Tìm sản phẩm gần đúng =====
def find_product(name, products):
    name_norm = normalize_text(name)
    best = None
    score = 0
    for p in products:
        pname = normalize_text(p["name"])
        s = len(set(name_norm.split()) & set(pname.split()))
        if s > score:
            score = s
            best = p
    return best


# ===== So sánh hai sản phẩm =====
def compare_products(n1, n2, products):
    p1 = find_product(n1, products)
    p2 = find_product(n2, products)
    if not p1 or not p2:
        return "Không tìm thấy sản phẩm để so sánh."

    reply = (
        f"So sánh:\n"
        f"- {p1['name']} — {p1['price']:,}đ | {p1['battery']}mAh | {p1['chipset']} | RAM {p1['ram']}\n"
        f"- {p2['name']} — {p2['price']:,}đ | {p2['battery']}mAh | {p2['chipset']} | RAM {p2['ram']}\n"
    )

    better = []
    if p1["performance_score"] != p2["performance_score"]:
        best = p1 if p1["performance_score"] > p2["performance_score"] else p2
        better.append(f"Hiệu năng tốt hơn: {best['name']}")
    if p1["battery"] != p2["battery"]:
        best = p1 if p1["battery"] > p2["battery"] else p2
        better.append(f"Pin lâu hơn: {best['name']}")
    if p1["price"] != p2["price"]:
        best = p1 if p1["price"] < p2["price"] else p2
        better.append(f"Giá rẻ hơn: {best['name']}")

    if better:
        reply += "\n" + " | ".join(better)
    else:
        reply += "\nHai sản phẩm khá tương đồng."
    return reply


# ===== Xử lý tin nhắn chatbot =====
def handle_chat_message(user_message):
    products = get_all_products()
    msg = normalize_text(user_message)
    reply = None

    # So sánh 2 sản phẩm
    match = re.findall(r"so sanh (.+?) (?:va|vs|voi|với) (.+)", msg)
    if match:
        n1, n2 = match[0]
        reply = compare_products(n1, n2, products)

    # Tìm sản phẩm cụ thể
    if not reply:
        p = find_product(user_message, products)
        if p:
            if any(w in msg for w in ["gia", "bao nhieu", "mấy tien", "mấy tiền"]):
                reply = f"{p['name']} có giá {int(p['price']):,}đ."
            elif "pin" in msg:
                reply = f"{p['name']} có dung lượng pin {p['battery']} mAh."
            elif any(w in msg for w in ["manh", "hieu nang"]):
                reply = f"{p['name']} đạt {p['performance_score']} điểm hiệu năng."
            elif any(w in msg for w in ["ra mat", "nam", "moi nhat", "mới nhất"]):
                reply = f"{p['name']} ra mắt năm {p['release_year']}."
            else:
                reply = (
                    f"{p['name']} — {p['price']:,}đ | {p['battery']}mAh | "
                    f"{p['chipset']} | RAM {p['ram']} | Điểm {p['performance_score']}"
                )

    # Trường hợp đặc biệt
    if not reply:
        if any(x in msg for x in ["re nhat", "rẻ nhất"]):
            p = min(products, key=lambda x: x["price"])
            reply = f"{p['name']} là sản phẩm rẻ nhất: {p['price']:,}đ."
        elif any(x in msg for x in ["dat nhat", "đắt nhất"]):
            p = max(products, key=lambda x: x["price"])
            reply = f"{p['name']} là sản phẩm đắt nhất: {p['price']:,}đ."
        elif "pin" in msg and any(x in msg for x in ["tot nhat", "trau nhat", "lâu nhất"]):
            p = max(products, key=lambda x: x["battery"])
            reply = f"{p['name']} có pin trâu nhất: {p['battery']}mAh."
        elif "moi nhat" in msg or "mới nhất" in msg:
            p = max(products, key=lambda x: x["release_year"])
            reply = f"{p['name']} là mẫu mới nhất, ra mắt năm {p['release_year']}."

    if not reply:
        reply = "Xin lỗi, tôi chưa hiểu câu hỏi của bạn."

    return reply
