from datetime import datetime
from bson import ObjectId

def format_currency(amount):
    """Format float amount into Indian Rupee currency format (e.g. ₹ 2,200.00)."""
    try:
        val = float(amount)
        return f"₹ {val:,.2f}"
    except (ValueError, TypeError):
        return "₹ 0.00"

def format_date(date_obj, fmt="%d %b %Y"):
    """Format datetime object or date string into readable text."""
    if not date_obj:
        return "-"
    if isinstance(date_obj, str):
        try:
            date_obj = datetime.strptime(date_obj[:10], "%Y-%m-%d")
        except ValueError:
            return date_obj
    return date_obj.strftime(fmt)

def str_id(doc):
    """Safely return string representation of document _id."""
    if not doc:
        return ""
    if isinstance(doc, dict):
        return str(doc.get('_id', ''))
    return str(doc)
