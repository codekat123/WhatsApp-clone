from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from django.conf import settings
import base64
import logging
import os

logger = logging.getLogger(__name__)

class EncryptionService:
    def __init__(self, secret_key=None):
        """
        Initialize encryption service.
        
        Args:
            secret_key: Optional. If not provided, will use settings.SECRET_KEY
        """
        self.salt = settings.SECRET_KEY.encode()  # Using Django's secret key as salt
        self.iterations = 100000
        self.secret_key = secret_key or settings.SECRET_KEY
        self.fernet = self._get_fernet_instance()

    def _get_fernet_instance(self):
        """Create a Fernet instance with derived key"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=self.iterations,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.secret_key.encode()))
        return Fernet(key)

    def encrypt(self, data: str) -> str:
        """Encrypt string data"""
        try:
            if not isinstance(data, str):
                data = str(data)
            return self.fernet.encrypt(data.encode()).decode()
        except Exception as e:
            logger.error(f"Encryption error: {str(e)}")
            raise ValueError("Failed to encrypt data")

    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt string data"""
        try:
            return self.fernet.decrypt(encrypted_data.encode()).decode()
        except InvalidToken:
            logger.error("Invalid token during decryption")
            raise ValueError("Invalid or corrupted data")
        except Exception as e:
            logger.error(f"Decryption error: {str(e)}")
            raise ValueError("Failed to decrypt data")

    @staticmethod
    def generate_key() -> str:
        """Generate a new encryption key"""
        return Fernet.generate_key().decode()


