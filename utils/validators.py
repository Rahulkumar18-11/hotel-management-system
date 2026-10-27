import re
from datetime import datetime

def is_valid_email(email):
    """Validate email address format using regex."""
    if not email:
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email.strip()))

def is_valid_phone(phone):
    """Validate phone number format (10 to 15 digits)."""
    if not phone:
        return False
    cleaned = re.sub(r'[\s\-\(\)\+]', '', phone)
    return cleaned.isdigit() and len(cleaned) >= 10

def is_valid_date_range(check_in_str, check_out_str):
    """Ensure check-out date is strictly after check-in date."""
    try:
        d_in = datetime.strptime(str(check_in_str).strip(), '%Y-%m-%d').date()
        d_out = datetime.strptime(str(check_out_str).strip(), '%Y-%m-%d').date()
        return d_out > d_in
    except Exception:
        return False
