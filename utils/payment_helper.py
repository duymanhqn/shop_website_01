# # utils/payment_helper.py
# from flask import request, url_for
# from urllib.parse import urljoin

# def get_callback_url(endpoint):
#     """
#     Tạo URL callback động cho mọi môi trường:
#     - localhost → http://localhost:5000
#     - Render → https://htmthshop.onrender.com
#     - Production → https://mhtmh.id.vn
#     """
#     host = request.host  # Ví dụ: localhost:5000, htmthshop.onrender.com, mhtmh.id.vn

#     # Xác định scheme (http hay https)
#     if host.startswith('localhost') or host.startswith('127.0.0.1'):
#         scheme = 'http'
#     else:
#         scheme = 'https'

#     base_url = f"{scheme}://{host}"
#     return urljoin(base_url + '/', url_for(endpoint))
# utils/payment_helper.py
from flask import request, url_for
from urllib.parse import urljoin

def get_callback_url(endpoint):
    """
    Tạo URL callback động cho mọi môi trường
    endpoint phải là 'order_bp.momo_return', 'order_bp.momo_ipn', ...
    """
    host = request.host

    # Xác định scheme
    if host.startswith('localhost') or host.startswith('127.0.0.1'):
        scheme = 'http'
    else:
        scheme = 'https'

    base_url = f"{scheme}://{host}"
    return urljoin(base_url + '/', url_for(endpoint)) 