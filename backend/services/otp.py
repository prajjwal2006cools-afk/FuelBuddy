import random
import hashlib
from datetime import datetime, timedelta

# In a real app, use Redis or a DB table for OTPs. 
# For demo, using an in-memory dictionary.
OTP_STORE = {}

def generate_otp() -> str:
    return str(random.randint(100000, 999999))

def hash_otp(otp: str) -> str:
    return hashlib.sha256(otp.encode()).hexdigest()

def send_otp_sms(phone_number: str, otp: str):
    # DEV mode implementation
    print(f"\n{'='*40}")
    print(f"🚀 DEV MODE: OTP for {phone_number} is: {otp}")
    print(f"{'='*40}\n")
    return True

def store_otp(phone_number: str, otp: str):
    expires_at = datetime.utcnow() + timedelta(minutes=5)
    OTP_STORE[phone_number] = {
        "hash": hash_otp(otp),
        "expires_at": expires_at,
        "attempts": 0
    }

def verify_otp(phone_number: str, otp: str) -> bool:
    record = OTP_STORE.get(phone_number)
    if not record:
        return False
    
    if datetime.utcnow() > record["expires_at"]:
        del OTP_STORE[phone_number]
        return False
        
    if record["attempts"] >= 5:
        del OTP_STORE[phone_number]
        return False
        
    record["attempts"] += 1
    
    if hash_otp(otp) == record["hash"]:
        del OTP_STORE[phone_number]
        return True
        
    return False
