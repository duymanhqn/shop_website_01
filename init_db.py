from app import app, db
from models.models import Product

with app.app_context():
   
    db.drop_all()
    db.create_all()

    # ===== iPhone =====
    iphones = [
        Product(name="iPhone 11", price=12000000, description="iPhone 11 - Hiệu năng ổn định, camera kép", image_url="images/IP_11.png", category="iphone"),
        Product(name="iPhone 12", price=15000000, description="iPhone 12 - Chip A14 Bionic mạnh mẽ", image_url="images/IP_12.png", category="iphone"),
        Product(name="iPhone 13", price=18000000, description="iPhone 13 - Thiết kế đẹp, pin lâu", image_url="images/IP_13.png", category="iphone"),
        Product(name="iPhone 14", price=21000000, description="iPhone 14 - Mượt mà và hiện đại", image_url="images/IP_14.png", category="iphone"),
        Product(name="iPhone 15", price=25000000, description="iPhone 15 - Chip A16 cực mạnh", image_url="images/IP_15.png", category="iphone"),
        Product(name="iPhone 16", price=28000000, description="iPhone 16 - Cấu hình cao cấp", image_url="images/IP_16.png", category="iphone"),
        Product(name="iPhone 17", price=31000000, description="iPhone 17 - Mẫu flagship mới nhất", image_url="images/IP_17.png", category="iphone"),
        Product(name="iPhone XS Max", price=13000000, description="iPhone XS Max - Sang trọng, camera kép", image_url="images/IP_XS_Max.png", category="iphone"),
    ]

    # ===== Samsung =====
    samsungs = [
        Product(name="Samsung Galaxy A07", price=7000000, description="Galaxy A07 - Giá rẻ, pin trâu, màn hình lớn", image_url="images/Galaxy_A07.png", category="samsung"),
        Product(name="Samsung Galaxy A17", price=9000000, description="Galaxy A17 - Giá rẻ, pin trâu", image_url="images/Galaxy_A17.png", category="samsung"),
        Product(name="Samsung Galaxy Flip7", price=28000000, description="Galaxy Flip7 - Thiết kế gập sang trọng, hiệu năng cao", image_url="images/Galaxy_Flip7.png", category="samsung"),
        Product(name="Samsung Galaxy S22 Ultra", price=24000000, description="Galaxy S22 Ultra - Camera đỉnh cao, cấu hình mạnh mẽ", image_url="images/Galaxy_S22ultra.png", category="samsung"),
        Product(name="Samsung Galaxy S24", price=26000000, description="Galaxy S24 - Mạnh mẽ, màn hình đẹp, chip Snapdragon 8 Gen 3", image_url="images/Galaxy_S24.png", category="samsung"),
        Product(name="Samsung Galaxy S25 FE", price=20000000, description="Galaxy S25 FE - Giá hợp lý, cấu hình tốt", image_url="images/Galaxy_S25_FE.png", category="samsung"),
        Product(name="Samsung Galaxy S25", price=28000000, description="Galaxy S25 - Flagship cao cấp", image_url="images/Galaxy_S25.png", category="samsung"),
        Product(name="Samsung Galaxy Z Fold7", price=42000000, description="Galaxy Z Fold7 - Điện thoại gập cao cấp, đa nhiệm mạnh mẽ", image_url="images/GalaxyZ_Fold7.png", category="samsung"),
    ]

    # ===== Laptop =====
    laptops = [
        Product(name="Laptop Acer A715", price=19000000, description="Acer Aspire 7 A715 - Chip Ryzen, card GTX", image_url="images/Laptop_Acer_A715.png", category="laptop"),
        Product(name="Laptop Asus F16", price=22000000, description="Asus F16 - Hiệu năng ổn định", image_url="images/Laptop_Asus_F16.png", category="laptop"),
        Product(name="Laptop Asus V16", price=24000000, description="Asus V16 - Mạnh mẽ, sang trọng", image_url="images/Laptop_Asus_V16.png", category="laptop"),
        Product(name="Laptop HP 15", price=17500000, description="HP 15 - Mỏng nhẹ, pin lâu", image_url="images/Laptop_Hp_15.png", category="laptop"),
        Product(name="Laptop Lenovo Slim3", price=18500000, description="Lenovo Slim 3 - Cân đối giá và hiệu năng", image_url="images/Laptop_Lenovo_Slim3.png", category="laptop"),
        Product(name="Laptop MSI 14", price=26000000, description="MSI 14 - Dành cho dân thiết kế và game", image_url="images/Laptop_MSI_14.png", category="laptop"),
        Product(name="MacBook M2", price=32000000, description="MacBook M2 - Hiệu năng vượt trội", image_url="images/MacBook_M2.png", category="laptop"),
        Product(name="MacBook M4", price=38000000, description="MacBook M4 - Siêu mạnh mẽ và bền bỉ", image_url="images/MacBook_M4.png", category="laptop"),
    ]

    # ===== Gộp tất cả sản phẩm =====
    all_products = iphones + samsungs + laptops

    db.session.add_all(all_products)
    db.session.commit()

    print(" Database đã được khởi tạo lại với toàn bộ sản phẩm iPhone, Samsung và Laptop!")
