import secrets
import base64

# Generate a secure random string of bytes
secret_key = secrets.token_bytes(32)

# Encode the bytes into a base64 string
encoded_secret_key = base64.urlsafe_b64encode(secret_key).decode()

print(encoded_secret_key)
