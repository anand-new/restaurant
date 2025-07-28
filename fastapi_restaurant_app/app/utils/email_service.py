# app/utils/email_service.py
def send_reset_email(email: str, token: str):
    print(f"[DEBUG] Send reset link to {email}: http://localhost:3000/reset-password?token={token}")
