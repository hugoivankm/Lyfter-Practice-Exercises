from .contact_routes import contact_bp
from .invoice_routes import invoice_bp
from .order_routes import order_bp
from .product_routes import product_bp
from .user_routes import user_bp

__all__ = ["contact_bp", "invoice_bp", "order_bp", "product_bp", "user_bp"]
