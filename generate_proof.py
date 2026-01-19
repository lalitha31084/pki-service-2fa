import os
import subprocess
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa, utils
from cryptography.hazmat.primitives import serialization

def generate_proof():
    print("--- Generating Submission Proof ---")

    # 1. Get the latest Commit Hash
    try:
        commit_hash = subprocess.check_output(['git', 'log', '-1', '--format=%H']).decode('ascii').strip()
        print(f"Commit Hash: {commit_hash}")
    except Exception as e:
        print("Error: Could not get git commit hash. Are you in a git repo?")
        return

    # 2. Load Student Private Key
    try:
        with open("student_private.pem", "rb") as key_file:
            student_private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None
            )
    except FileNotFoundError:
        print("Error: student_private.pem not found.")
        return

    # 3. Sign the Commit Hash (RSA-PSS)
    # Critical: Sign the ASCII bytes of the hash string, NOT the binary representation
    message = commit_hash.encode('utf-8')
    
    signature = student_private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    # 4. Load Instructor Public Key
    try:
        with open("instructor_public.pem", "rb") as key_file:
            instructor_public_key = serialization.load_pem_public_key(
                key_file.read()
            )
    except FileNotFoundError:
        print("Error: instructor_public.pem not found.")
        return

    # 5. Encrypt the Signature (RSA-OAEP)
    encrypted_signature = instructor_public_key.encrypt(
        signature,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # 6. Encode to Base64
    final_proof = base64.b64encode(encrypted_signature).decode('utf-8')

    print("\nSUCCESS! Here are your details for the submission form:\n")
    print(f"1. GitHub Repo URL:      https://github.com/lalitha31084/pki-service-2fa.git")
    print(f"2. Commit Hash:          {commit_hash}")
    print(f"3. Encrypted Signature:  {final_proof}")

if __name__ == "__main__":
    generate_proof()