import pytest
from services.billing_service import BillingService

def test_billing_formula_exact_user_example():
    """
    Test billing calculation with exact prompt example:
    - Room price = ₹2200/day
    - Days = 3
    - Food = ₹850
    - Room charges: 2200 * 3 = ₹6600
    - Subtotal: 6600 + 850 = ₹7450
    - GST 18%: 7450 * 18% = ₹1341
    - Total: ₹8791
    """
    bill = BillingService.calculate_bill(room_price_per_day=2200.0, number_of_days=3, food_charges=850.0)

    assert bill['room_charges'] == 6600.0
    assert bill['subtotal'] == 7450.0
    assert bill['gst'] == 1341.0
    assert bill['total_amount'] == 8791.0

def test_billing_zero_food_charges():
    """Test billing computation when food charges are 0."""
    bill = BillingService.calculate_bill(room_price_per_day=1000.0, number_of_days=2, food_charges=0.0)

    assert bill['room_charges'] == 2000.0
    assert bill['subtotal'] == 2000.0
    assert bill['gst'] == 360.0  # 2000 * 0.18
    assert bill['total_amount'] == 2360.0

def test_billing_invalid_values_fallback():
    """Test robust fallback on invalid string inputs."""
    bill = BillingService.calculate_bill(room_price_per_day="invalid", number_of_days="abc", food_charges=None)

    assert bill['room_charges'] == 0.0
    assert bill['subtotal'] == 0.0
    assert bill['gst'] == 0.0
    assert bill['total_amount'] == 0.0
