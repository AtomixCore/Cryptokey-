import os
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

MAGIC_HEADER = b"__SLE__"


class SLE:
    """
    Secure Lightweight Encryption (SLE) utility for encrypting and decrypting binary data
    using password-based AES encryption with PBKDF2 and CBC mode.
    """

    def __init__(self, password: bytes):
        """
        Initialize the encryption engine.

        Args:
            password (bytes): The password used for encryption and decryption.
        """
        if not isinstance(password, bytes):
            raise TypeError("Password must be of type bytes.")
        self.password = password
        self.backend = default_backend()

    def _derive_key(self, salt: bytes) -> bytes:
        """
        Derive a strong encryption key from the password and salt.

        Args:
            salt (bytes): A 16-byte salt for KDF.

        Returns:
            bytes: A 32-byte AES key.
        """
        if len(salt) != 16:
            raise ValueError("Salt must be exactly 16 bytes.")

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100_000,
            backend=self.backend,
        )
        return kdf.derive(self.password)

    def encrypt(self, data: bytes) -> bytes:
        """
        Encrypt binary data using AES-256 in CBC mode.

        Args:
            data (bytes): Raw data to encrypt.

        Returns:
            bytes: Encrypted binary blob with salt and IV prepended.
        """
        salt = os.urandom(16)
        iv = os.urandom(16)
        key = self._derive_key(salt)

        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(MAGIC_HEADER + data) + padder.finalize()

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=self.backend)
        encryptor = cipher.encryptor()
        encrypted = encryptor.update(padded_data) + encryptor.finalize()

        return salt + iv + encrypted

    def decrypt(self, encrypted_data: bytes) -> bytes:
        """
        Decrypt data previously encrypted with this class.

        Args:
            encrypted_data (bytes): Data to decrypt.

        Returns:
            bytes: Decrypted original content.

        Raises:
            ValueError: If decryption fails or data is invalid.
        """
        if len(encrypted_data) < 32:
            raise ValueError("Encrypted data is too short or corrupted.")

        salt = encrypted_data[:16]
        iv = encrypted_data[16:32]
        encrypted = encrypted_data[32:]

        key = self._derive_key(salt)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=self.backend)

        decryptor = cipher.decryptor()
        padded_data = decryptor.update(encrypted) + decryptor.finalize()

        unpadder = padding.PKCS7(128).unpadder()
        data = unpadder.update(padded_data) + unpadder.finalize()

        if not data.startswith(MAGIC_HEADER):
            raise ValueError("Invalid password or data corrupted.")

        return data[len(MAGIC_HEADER):]

    def generate_file(self, filename: str, data: bytes) -> None:
        """
        Encrypt data and save it to a file.

        Args:
            filename (str): Destination file path.
            data (bytes): Raw data to encrypt.
        """
        encrypted = self.encrypt(data)
        with open(filename, "wb") as f:
            f.write(encrypted)

    def read_file(self, filename: str) -> bytes:
        """
        Read raw encrypted content from a file.

        Args:
            filename (str): Path to the encrypted file.

        Returns:
            bytes: File content.
        """
        if not os.path.exists(filename):
            raise FileNotFoundError(f"File not found: {filename}")

        with open(filename, "rb") as f:
            return f.read()


# from src.lib.encryption import SLE

# password = b"mysecretpassword"
# sle = SLE(password)

# original_data = b"Top secret configuration goes here."
# sle.generate_file("config.ac.esc", original_data)

# # Later...
# encrypted = sle.read_file("config.ac.esc")
# decrypted = sle.decrypt(encrypted)
# print("Decrypted:", decrypted.decode())
