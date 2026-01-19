from crypto_utils import generate_totp_code, verify_totp_code

# Read the decrypted seed we saved in the previous step
try:
    with open("decrypted_seed.txt", "r") as f:
        hex_seed = f.read().strip()

    print(f"Using Seed: {hex_seed[:10]}...") # Printing just start for privacy

    # 1. Generate Code
    code = generate_totp_code(hex_seed)
    print(f"Generated 2FA Code: {code}")

    # 2. Verify Code (Self-check)
    is_valid = verify_totp_code(hex_seed, code)
    print(f"Verification Result: {is_valid}")
    
    if is_valid:
        print("SUCCESS! TOTP logic is working.")
    else:
        print("FAILED to verify generated code.")

except FileNotFoundError:
    print("Error: decrypted_seed.txt not found. Please run Step 5 test again.")