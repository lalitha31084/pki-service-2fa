from crypto_utils import decrypt_seed

# Read the encrypted seed from file
with open("encrypted_seed.txt", "r") as f:
    encrypted_seed = f.read().strip()

# Attempt decryption
seed = decrypt_seed(encrypted_seed)

if seed:
    print("SUCCESS! Decrypted Seed:", seed)
    # Save it securely for the next steps (simulating persistence)
    with open("decrypted_seed.txt", "w") as f:
        f.write(seed)
else:
    print("FAILED to decrypt.")