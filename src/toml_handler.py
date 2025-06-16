import tomli
from types import SimpleNamespace
from typing import Any, Union


def _dict_to_namespace(d: dict) -> Any:
  """
  Recursively converts a dictionary to a SimpleNamespace object
  to allow dot notation access.

  Args:
      d (dict): The dictionary to convert.

  Returns:
      SimpleNamespace or value: Namespace or original value.
  """
  if not isinstance(d, dict):
      return d
  return SimpleNamespace(**{k: _dict_to_namespace(v) for k, v in d.items()})


class TomlHandler:
  """
  Parses TOML code and provides dot-accessible attributes.
  """

  def __init__(self, toml_code: str):
      """
      Initialize the handler with TOML source code.

      Args:
          toml_code (str): The TOML string to parse.

      Raises:
          ValueError: If the TOML code is invalid.
      """
      try:
          self._raw_dict = tomli.loads(toml_code)
      except tomli.TOMLDecodeError as e:
          raise ValueError(f"Invalid TOML syntax: {e}")

      self._data = _dict_to_namespace(self._raw_dict)

  def __getattr__(self, item: str) -> Any:
    """
    Allows attribute access via dot notation.

    Args:
        item (str): Attribute name.

    Returns:
        Any: Value of the attribute.

    Raises:
        AttributeError: If the attribute doesn't exist.
    """
    try:
        return getattr(self._data, item)
    except AttributeError:
        raise AttributeError(f"'{item}' not found in TOML data.")

  def as_dict(self) -> dict:
    """
    Get the original parsed data as a plain dictionary.

    Returns:
        dict: Raw parsed TOML data.
    """
    return self._raw_dict
