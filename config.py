class Config:
    #  Kết nối đến PostgreSQL hiện tại của bạn (shop_db)
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:123456@localhost:5432/shop_db"

    #  Tắt track modification để tránh warning
    SQLALCHEMY_TRACK_MODIFICATIONS = False
