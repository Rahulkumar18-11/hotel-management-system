from datetime import datetime
from models.booking_model import Booking
from models.room_model import Room
from services.billing_service import BillingService

class BookingService:
    """Service handling booking business rules, availability checks, and status transitions."""

    @staticmethod
    def calculate_stay_days(check_in_str, check_out_str):
        """Calculate total stay duration in days given check-in and check-out date strings (YYYY-MM-DD)."""
        try:
            d_in = datetime.strptime(str(check_in_str).strip(), '%Y-%m-%d').date()
            d_out = datetime.strptime(str(check_out_str).strip(), '%Y-%m-%d').date()
            days = (d_out - d_in).days
            return days if days > 0 else 0
        except ValueError:
            return 0

    @staticmethod
    def is_room_available(room_id, check_in_str, check_out_str, exclude_booking_id=None):
        """
        Verify if a room is free for booking between check_in and check_out dates.
        Backend authoritative double-booking check.
        """
        room = Room.find_by_id(room_id)
        if not room:
            return False, "Selected room does not exist."

        if room.get('status') == 'maintenance':
            return False, "Room is currently under maintenance."

        # Check overlapping active bookings
        overlapping = Booking.find_overlapping_bookings(room_id, check_in_str, check_out_str, exclude_booking_id)
        if overlapping:
            return False, f"Room {room.get('room_number')} is already booked or reserved for the selected dates."

        return True, "Room is available."

    @classmethod
    def create_booking(cls, customer_id, room_id, check_in_str, check_out_str, created_by=''):
        """
        Orchestrates full room booking workflow:
        1. Validates stay duration
        2. Checks double booking collisions
        3. Calculates initial room charge billing
        4. Inserts booking record
        5. Updates room status to 'booked'
        """
        days = cls.calculate_stay_days(check_in_str, check_out_str)
        if days <= 0:
            return None, "Check-out date must be after Check-in date."

        is_avail, msg = cls.is_room_available(room_id, check_in_str, check_out_str)
        if not is_avail:
            return None, msg

        room = Room.find_by_id(room_id)
        room_price = float(room.get('price_per_day', 0.0))

        # Initial billing calculations (0 food charges at booking creation)
        bill = BillingService.calculate_bill(room_price, days, food_charges=0.0)

        new_booking = Booking.create(
            customer_id=customer_id,
            room_id=room_id,
            check_in=check_in_str,
            check_out=check_out_str,
            number_of_days=days,
            room_price=room_price,
            food_charges=0.0,
            subtotal=bill['subtotal'],
            gst=bill['gst'],
            total_amount=bill['total_amount'],
            created_by=created_by,
            status='reserved'
        )

        if new_booking:
            # Update room status to booked
            Room.update_status(room_id, 'booked')
            return new_booking, "Booking created successfully!"
        
        return None, "Failed to record booking in database."

    @staticmethod
    def check_in_guest(booking_id):
        """Process check-in transition (reserved -> checked_in)."""
        booking = Booking.find_by_id(booking_id)
        if not booking:
            return False, "Booking not found."

        if booking.get('status') == 'checked_in':
            return False, "Guest is already checked in."

        if booking.get('status') in ['checked_out', 'cancelled']:
            return False, f"Cannot check-in booking with status: {booking.get('status')}."

        success = Booking.update_status(booking_id, 'checked_in')
        if success:
            Room.update_status(booking.get('room_id'), 'booked')
            return True, "Guest checked in successfully!"
        
        return False, "Failed to update check-in status."

    @staticmethod
    def check_out_guest(booking_id, final_food_charges=0.0):
        """
        Process check-out transition:
        1. Recalculates final bill with food charges + 18% GST
        2. Updates booking status to checked_out
        3. Frees room status back to 'available'
        """
        booking = Booking.find_by_id(booking_id)
        if not booking:
            return False, "Booking not found."

        if booking.get('status') == 'checked_out':
            return False, "Guest is already checked out."

        room_price = float(booking.get('room_price', 0.0))
        days = int(booking.get('number_of_days', 1))

        # Compute final billing
        bill = BillingService.calculate_bill(room_price, days, food_charges=final_food_charges)

        # Update billing numbers
        Booking.update_billing(
            booking_id,
            food_charges=final_food_charges,
            subtotal=bill['subtotal'],
            gst=bill['gst'],
            total_amount=bill['total_amount']
        )

        # Update status
        success = Booking.update_status(booking_id, 'checked_out')
        if success:
            # Release room back to available
            Room.update_status(booking.get('room_id'), 'available')
            return True, "Guest checked out successfully and bill finalized!"

        return False, "Failed to process check-out."
