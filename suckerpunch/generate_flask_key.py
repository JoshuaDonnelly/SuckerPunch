import secrets
# Generates a 24-byte key in URL-safe base64 encoding (produces a shorter string)
secret_key = secrets.token_urlsafe(24)
print(secret_key)