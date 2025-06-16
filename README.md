# Cryptokey

A secure, lightweight command-line tool for encrypting TOML configuration files using AES-256 encryption with PBKDF2 key derivation.

[![License: APUL-1.0](https://img.shields.io/badge/License-APUL--1.0-blue.svg)](LICENSE)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Security: AES-256](https://img.shields.io/badge/Security-AES--256-green.svg)](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard)

## Features

- **Military-grade encryption**: AES-256 in CBC mode with PBKDF2 key derivation
- **TOML support**: Specifically designed for TOML configuration files
- **Secure by default**: 100,000 PBKDF2 iterations for strong key derivation
- **Password generation**: Built-in secure random password generator
- **Lightweight**: Minimal dependencies, fast encryption/decryption
- **CLI interface**: Simple command-line interface with Click
- **Input validation**: Automatic TOML syntax validation and file extension checks

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/AtomixCore/Cryptokey-.git
cd Cryptokey-

# Install dependencies
pip install click tomli cryptography
```

### Basic Usage

```bash
# Encrypt a TOML file with a custom password
python CryptokeyCli.py -x config.ac.esc -o encrypted.ac.es -p "my-secure-password"

# Generate a secure password automatically
python CryptokeyCli.py -x config.ac.esc -o encrypted.ac.es --gen-pass
```

## Detailed Usage

### Command Line Options

| Option | Description | Required |
|--------|-------------|----------|
| `-x, --input` | Input TOML file (must end with `.ac.esc`) | Yes |
| `-o, --output` | Output encrypted file (must end with `.ac.es`) | Yes |
| `-p, --password` | Password for encryption | No* |
| `--gen-pass` | Generate a secure random password | No* |

*Either `--password` or `--gen-pass` is required.

### File Extensions

- **Input files**: Must have `.ac.esc` extension and contain valid TOML
- **Output files**: Must have `.ac.es` extension (encrypted binary format)

### Examples

```bash
# Example 1: Encrypt with custom password
python CryptokeyCli.py -x myconfig.ac.esc -o myconfig.ac.es -p "super-secret-123"

# Example 2: Generate password automatically
python CryptokeyCli.py -x myconfig.ac.esc -o myconfig.ac.es --gen-pass

# Example 3: Using the test file
python CryptokeyCli.py -x test/config.ac.esc -o test/encrypted.ac.es --gen-pass
```

## Architecture

### Core Components

```
Cryptokey/
├── CryptokeyCli.py          # Main CLI interface
├── src/
│   ├── cryptokey.py         # High-level encryption handler
│   ├── encryption.py        # SLE (Secure Lightweight Encryption) engine
│   └── toml_handler.py      # TOML parsing and validation
└── test/
    └── config.ac.esc        # Sample TOML configuration
```

### Security Features

- **AES-256-CBC**: Industry-standard encryption algorithm
- **PBKDF2-HMAC-SHA256**: Secure key derivation with 100,000 iterations
- **Random salt**: 16-byte salt for each encryption
- **Random IV**: 16-byte initialization vector for CBC mode
- **PKCS7 padding**: Proper padding for variable-length data
- **Magic header**: Prevents tampering and validates decryption

## Development

### Prerequisites

- Python 3.7 or higher
- Required packages: `click`, `tomli`, `cryptography`

### Project Structure

```python
# Main CLI entry point
CryptokeyCli.py          # Command-line interface with Click

# Core encryption logic
src/cryptokey.py         # Cryptokey class - high-level encryption handler
src/encryption.py        # SLE class - low-level AES encryption engine
src/toml_handler.py      # TomlHandler class - TOML parsing utilities
```

### Key Classes

#### `Cryptokey`
- High-level encryption handler
- Password generation utilities
- TOML code encryption interface

#### `SLE` (Secure Lightweight Encryption)
- AES-256-CBC encryption engine
- PBKDF2 key derivation
- Binary file I/O operations

#### `TomlHandler`
- TOML parsing and validation
- Dot-notation attribute access
- Dictionary conversion utilities

## Security Considerations

### Encryption Strength
- **Algorithm**: AES-256 in CBC mode
- **Key Derivation**: PBKDF2-HMAC-SHA256 with 100,000 iterations
- **Salt**: 16 bytes of cryptographically secure random data
- **IV**: 16 bytes of cryptographically secure random data

### Best Practices
- Use strong, unique passwords for each file
- Store passwords securely (not in plain text)
- Regularly rotate encryption keys
- Validate TOML syntax before encryption
- Use the `--gen-pass` flag for automatic password generation

## License

This project is licensed under the **AtomixCore Public Use License v1.0 (APUL-1.0)**.

**Key License Terms:**
- Free for personal, educational, and internal business use
- Can be used in closed-source or proprietary systems
- Redistribution prohibited without explicit permission
- Commercial use requires written approval
- Attribution required: Leo Lan - https://github.com/atomixcore

For commercial licensing or redistribution rights, contact the author.

## Contributing

While this project is primarily for personal and internal use, suggestions and bug reports are welcome. Please ensure compliance with the license terms before contributing.

## Support

- **Author**: Leo Lan
- **GitHub**: https://github.com/AtomixCore
- **Repository**: https://github.com/AtomixCore/Cryptokey-
- **License**: APUL-1.0

---

**Security Notice**: This tool is designed for encrypting TOML configuration files. Always use strong passwords and keep them secure. The encrypted files contain sensitive data and should be handled with appropriate security measures.
