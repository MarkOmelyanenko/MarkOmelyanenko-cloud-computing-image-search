import random
import string

def generate_postgresql_password(length=24):
    if length < 4:
        raise ValueError("Password length must be at least 4 to include all character types.")
    
    # Define safe special characters (avoid quotes, backslashes, semicolons)
    safe_specials = "!@#$%^&*()-_=+[]{}<>:?/"
    
    # Ensure the password contains at least one of each required type
    mandatory = [
        random.choice(string.ascii_uppercase),  # At least one uppercase
        random.choice(string.ascii_lowercase),  # At least one lowercase
        random.choice(string.digits),           # At least one digit
        random.choice(safe_specials)            # At least one safe special char
    ]

    # Remaining characters
    all_allowed = string.ascii_letters + string.digits + safe_specials
    remaining = [random.choice(all_allowed) for _ in range(length - 4)]

    # Combine and shuffle
    password_list = mandatory + remaining
    random.shuffle(password_list)

    return ''.join(password_list)

# Generate and print the PostgreSQL-safe password
print("PostgreSQL Password:", generate_postgresql_password())
