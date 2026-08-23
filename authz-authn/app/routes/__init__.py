from .product_routes import product_bp
from .invoice_routes import invoice_bp
from .user_routes import user_bp
from .order_routes import order_bp
from .contact_routes import contact_bp

__all__ = ["product_bp", "invoice_bp", "user_bp", "order_bp", "contact_bp"]
