# Este archivo hace que el directorio controllers sea un paquete Python
from .auth_controller import bp as auth_bp
from .contact_controller import bp as contact_bp

__all__ = ['auth_bp', 'contact_bp']