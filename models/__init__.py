# Este archivo hace que el directorio models sea un paquete Python
from .database import get_db, close_db, init_db
from .user import User
from .contact import Contact

__all__ = ['get_db', 'close_db', 'init_db', 'User', 'Contact']