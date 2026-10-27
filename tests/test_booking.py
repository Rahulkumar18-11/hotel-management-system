import pytest
from services.booking_service import BookingService
from models.room_model import Room
from models.customer_model import Customer
from models.booking_model import Booking
from database.db import Database
import mongomock

@pytest.fixture
def mock_db():
    Database.client = mongomock.MongoClient()
    Database.db = Database.client['test_booking_db']
    Database.setup_indexes()
    return Database.db

def test_stay_days_calculation():
    """Test stay duration calculation logic."""
    days = BookingService.calculate_stay_days('2026-10-01', '2026-10-05')
    assert days == 4

    invalid_days = BookingService.calculate_stay_days('2026-10-05', '2026-10-01')
    assert invalid_days == 0

def test_double_booking_prevention(mock_db):
    """Test double-booking protection algorithm for overlapping dates."""
    room = Room.create('105', 'Deluxe', 3000.0, 2)
    cust = Customer.create('John Doe', 'john@example.com', '9876543210', 'Address', 'Passport', 'P12345')

    # Initial booking for Oct 10 - Oct 15
    booking1, msg1 = BookingService.create_booking(
        customer_id=str(cust['_id']),
        room_id=str(room['_id']),
        check_in_str='2026-10-10',
        check_out_str='2026-10-15'
    )
    assert booking1 is not None

    # Overlapping booking attempt: Oct 12 - Oct 18 (Should fail)
    booking2, msg2 = BookingService.create_booking(
        customer_id=str(cust['_id']),
        room_id=str(room['_id']),
        check_in_str='2026-10-12',
        check_out_str='2026-10-18'
    )
    assert booking2 is None
    assert "already booked" in msg2.lower()
