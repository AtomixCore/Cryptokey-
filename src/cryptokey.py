from src.lib.encryption import SLE
import random
import string


class Cryptokey:
  """
  A utility class for encrypting TOML code using a password,
  and generating secure random passwords if needed.
  """

  def __init__(self, password: str, toml_code: str, file_name: str):
    """
    Initialize the Cryptokey encryption handler.

    Args:
        password (str): Password used to encrypt the content.
        toml_code (str): Raw TOML string to encrypt.
        file_name (str): Output file name for encrypted data.
    """
    self.password = password
    self.toml_code = toml_code
    self.file_name = file_name
    self.sle = SLE(password.encode())

  def generate(self):
    """
    Encrypt the TOML code and save it to the specified file.
    """
    self.sle.generate_file(self.file_name, self.toml_code.encode())

  def generate_password(self, length: int = 16, include_special: bool = True) -> str:
    """
    Generate a secure random password.

    Args:
        length (int): Desired password length.
        include_special (bool): Whether to include special characters.

    Returns:
        str: The generated password.
    """
    chars = string.ascii_letters + string.digits
    if include_special:
        chars += "!@#$%^&*()-_=+[]{}|;:,.<>?/"

    password = ''.join(random.choices(chars, k=length))
    return password
