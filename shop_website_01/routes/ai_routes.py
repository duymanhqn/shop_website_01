from flask import Blueprint, request, jsonify
import AI as ai

ai_bp = Blueprint("ai_bp", __name__)


@ai_bp.route("/ai/search_products")
def search_products():
    keyword = request.args.get("keyword")
    if not keyword:
        return jsonify({"error": "keyword is required"}), 400

    try:
        result = ai.search_products(keyword=keyword)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(result)
