import os
import time
from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from crypto_utils import decrypt_seed, generate_totp_code, verify_totp_code

app = FastAPI()

# --- CONFIGURATION ---
# In Docker, we will map this to the absolute path /data/seed.txt
# Locally, we use the relative path data/seed.txt so it works on Windows
SEED_FILE_PATH = os.getenv("SEED_PATH", "data/seed.txt")

# --- DATA MODELS ---
class DecryptRequest(BaseModel):
    encrypted_seed: str

class VerifyRequest(BaseModel):
    code: str

# --- ENDPOINTS ---

@app.post("/decrypt-seed")
def api_decrypt_seed(request: DecryptRequest):
    """
    Accepts encrypted seed, decrypts it, and saves it to storage.
    """
    try:
        # 1. Decrypt
        decrypted_seed = decrypt_seed(request.encrypted_seed)
        
        if not decrypted_seed:
            return Response(content='{"error": "Decryption failed"}', media_type="application/json", status_code=500)

        # 2. Save to persistent storage
        # Ensure directory exists
        os.makedirs(os.path.dirname(SEED_FILE_PATH), exist_ok=True)
        
        with open(SEED_FILE_PATH, "w") as f:
            f.write(decrypted_seed)
            
        return {"status": "ok"}

    except Exception as e:
        print(f"Error: {e}")
        return Response(content='{"error": "Decryption failed"}', media_type="application/json", status_code=500)

@app.get("/generate-2fa")
def api_generate_2fa():
    """
    Generates the current TOTP code based on the stored seed.
    """
    if not os.path.exists(SEED_FILE_PATH):
        return Response(content='{"error": "Seed not decrypted yet"}', media_type="application/json", status_code=500)

    try:
        with open(SEED_FILE_PATH, "r") as f:
            hex_seed = f.read().strip()
            
        code = generate_totp_code(hex_seed)
        
        # Calculate remaining validity (30 second window)
        remaining_seconds = 30 - (int(time.time()) % 30)
        
        return {
            "code": code,
            "valid_for": remaining_seconds
        }
    except Exception as e:
        print(f"Error: {e}")
        return Response(content='{"error": "Internal error"}', media_type="application/json", status_code=500)

@app.post("/verify-2fa")
def api_verify_2fa(request: VerifyRequest):
    """
    Verifies if a submitted code is valid.
    """
    if not request.code:
        return Response(content='{"error": "Missing code"}', media_type="application/json", status_code=400)

    if not os.path.exists(SEED_FILE_PATH):
        return Response(content='{"error": "Seed not decrypted yet"}', media_type="application/json", status_code=500)
        
    try:
        with open(SEED_FILE_PATH, "r") as f:
            hex_seed = f.read().strip()
            
        is_valid = verify_totp_code(hex_seed, request.code)
        
        return {"valid": is_valid}

    except Exception as e:
        return Response(content='{"error": "Internal error"}', media_type="application/json", status_code=500)