from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def generate_rsa_keypair():
    print("Generating 4096-bit RSA keys. This might take a moment...")
    
    # Generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
    )

    # Serialize private key to PEM
    pem_private = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Serialize public key to PEM
    public_key = private_key.public_key()
    pem_public = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Save to files
    with open("student_private.pem", "wb") as f:
        f.write(pem_private)
    
    with open("student_public.pem", "wb") as f:
        f.write(pem_public)

    print("Keys generated successfully:")
    print("- student_private.pem")
    print("- student_public.pem")

if __name__ == "__main__":
    generate_rsa_keypair()