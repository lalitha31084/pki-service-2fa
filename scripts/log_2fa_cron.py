import sys
import os
import datetime

# Add the parent directory to path so we can import crypto_utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crypto_utils import generate_totp_code

SEED_FILE = "/data/seed.txt"

def log_code():
    # 1. Check if seed exists
    if not os.path.exists(SEED_FILE):
        print("Seed not found. Waiting for decryption...")
        return

    try:
        # 2. Read Seed
        with open(SEED_FILE, "r") as f:
            hex_seed = f.read().strip()

        # 3. Generate Code
        code = generate_totp_code(hex_seed)

        # 4. Get UTC Timestamp (Critical: Must be UTC)
        now = datetime.datetime.now(datetime.timezone.utc)
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

        # 5. Print to stdout (Cron will redirect this to file)
        print(f"{timestamp} - 2FA Code: {code}")

    except Exception as e:
        print(f"Cron Error: {e}")

if __name__ == "__main__":
    log_code()