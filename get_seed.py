import requests
import json
import sys

# API URL (Fixed)
API_URL = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws"

def get_seed():
    print("--- Dynamic Seed Request ---")
    
    # 1. Get User Input
    student_id = input("Enter your Student ID: ").strip()
    if not student_id:
        print("Error: Student ID cannot be empty.")
        return

    repo_url = input("Enter your GitHub Repo URL: ").strip()
    if not repo_url:
        print("Error: Repo URL cannot be empty.")
        return

    # 2. Read your public key
    try:
        with open("student_public.pem", "r") as f:
            public_key_content = f.read()
    except FileNotFoundError:
        print("Error: student_public.pem not found. Did you run Step 2?")
        return

    # 3. Prepare Payload
    payload = {
        "student_id": student_id,
        "github_repo_url": repo_url,
        "public_key": public_key_content
    }

    print(f"\nRequesting seed for {student_id}...")

    # 4. Send Request
    try:
        response = requests.post(API_URL, json=payload, timeout=15)
        
        if response.status_code != 200:
            print(f"Error: API returned status code {response.status_code}")
            print(f"Response: {response.text}")
            return

        data = response.json()
        
        if "encrypted_seed" in data:
            # 5. Save to file
            seed = data["encrypted_seed"]
            with open("encrypted_seed.txt", "w") as f:
                f.write(seed)
            print("Success! Encrypted seed saved to 'encrypted_seed.txt'")
        else:
            print("Error: 'encrypted_seed' not found in response.")
            print(data)

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Tip: Check your internet connection if you see a NameResolutionError.")

if __name__ == "__main__":
    get_seed()