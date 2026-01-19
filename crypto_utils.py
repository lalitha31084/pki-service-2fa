import base64
import pyotp
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization

def decrypt_seed(encrypted_seed_b64: str, private_key_path: str = "student_private.pem") -> str:
    """Decrypts the base64 encoded encrypted seed using the student's private key."""
    try:
        with open(private_key_path, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None
            )

        encrypted_data = base64.b64decode(encrypted_seed_b64)

        decrypted_data = private_key.decrypt(
            encrypted_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        decrypted_seed = decrypted_data.decode("utf-8")
        
        if len(decrypted_seed) != 64:
            raise ValueError(f"Invalid seed length: {len(decrypted_seed)}")
            
        return decrypted_seed

    except Exception as e:
        print(f"Decryption Error: {e}")
        return None

def get_totp_object(hex_seed: str):
    """Helper to create the TOTP object from hex seed."""
    # 1. Convert Hex to Bytes
    seed_bytes = bytes.fromhex(hex_seed)
    # 2. Convert Bytes to Base32 (Required for TOTP)
    base32_seed = base64.b32encode(seed_bytes).decode('utf-8')
    # 3. Create TOTP object (Default: SHA1, 6 digits, 30s interval)
    return pyotp.TOTP(base32_seed)

def generate_totp_code(hex_seed: str) -> str:
    """Generates the current 6-digit TOTP code."""
    totp = get_totp_object(hex_seed)
    return totp.now()

def verify_totp_code(hex_seed: str, code: str) -> bool:
    """Verifies a code with +/- 30 seconds tolerance."""
    totp = get_totp_object(hex_seed)
    # valid_window=1 means accept code from previous 30s or next 30s
    return totp.verify(code, valid_window=1)