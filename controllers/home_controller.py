from flask import render_template
from models.models import Product
import requests


class HomeController:
    #  Hiển thị trang chủ
    @staticmethod
    def show_home():
        
        iphones = Product.query.filter(Product.category.ilike('iphone')).all()
        samsungs = Product.query.filter(Product.category.ilike('samsung')).all()
        laptops = Product.query.filter(Product.category.ilike('laptop')).all()

        
        return render_template(
            "home.html",
            iphones=iphones,
            samsungs=samsungs,
            laptops=laptops,
            search_results=None,
            keyword=None
        )

    # Tìm kiếm sản phẩm bằng AI
    @staticmethod
    def search_products(keyword):
        if not keyword:
            return HomeController.show_home()

        try:
            
            response = requests.get(
                "http://127.0.0.1:5000/ai/search_products",
                params={"keyword": keyword},
                timeout=3
            )
            data = response.json()

            if "results" in data and data["results"]:
                matched_products = data["results"]
            else:
                matched_products = []
        except Exception as e:
            print("❌ Lỗi AI search:", e)
            matched_products = []

        # Trả dữ liệu cho giao diện
        return render_template(
            "home.html",
            search_results=matched_products,
            keyword=keyword,
            iphones=[],
            samsungs=[],
            laptops=[]
        )
