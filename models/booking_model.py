from datetime import datetime
from bson import ObjectId
from database.db import get_bookings_col, get_customers_col, get_rooms_col

def to_oid(val):
    """Safely convert string or ObjectId into PyMongo BSON ObjectId."""
    if not val:
        return None
    if isinstance(val, ObjectId):
        return val
    try:
        return ObjectId(str(val))
    except Exception:
        return None

class Booking:
    """Booking Model representing room reservations, stay records, and billing details."""

    @staticmethod
    def create(customer_id, room_id, check_in, check_out, number_of_days, room_price, 
               food_charges=0.0, subtotal=0.0, gst=0.0, total_amount=0.0, 
               created_by='', status='reserved'):
        """Create a new booking document in MongoDB."""
        col = get_bookings_col()
        if col is None:
            return None

        # Convert date strings to standard ISO format strings if necessary
        if isinstance(check_in, datetime):
            check_in_str = check_in.strftime('%Y-%m-%d')
        else:
            check_in_str = str(check_in)

        if isinstance(check_out, datetime):
            check_out_str = check_out.strftime('%Y-%m-%d')
        else:
            check_out_str = str(check_out)

        booking_doc = {
            'customer_id': str(customer_id),
            'room_id': str(room_id),
            'check_in': check_in_str,
            'check_out': check_out_str,
            'number_of_days': int(number_of_days),
            'room_price': float(room_price),
            'food_charges': float(food_charges),
            'subtotal': float(subtotal),
            'gst': float(gst),
            'total_amount': float(total_amount),
            'status': status,  # reserved, checked_in, checked_out, cancelled
            'created_by': created_by,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        result = col.insert_one(booking_doc)
        booking_doc['_id'] = result.inserted_id
        return booking_doc

    @staticmethod
    def find_by_id(booking_id):
        """Find booking by ObjectId and attach customer and room details."""
        col = get_bookings_col()
        oid = to_oid(booking_id)
        if col is None or not oid:
            return None
        try:
            booking = col.find_one({'_id': oid})
            if booking:
                return Booking._populate_relations(booking)
            return None
        except Exception:
            return None

    @staticmethod
    def _populate_relations(booking):
        """Helper to attach customer and room objects to booking dict."""
        customers_col = get_customers_col()
        rooms_col = get_rooms_col()
        
        if booking.get('customer_id'):
            c_oid = to_oid(booking['customer_id'])
            if c_oid and customers_col is not None:
                booking['customer'] = customers_col.find_one({'_id': c_oid})
            else:
                booking['customer'] = None
                
        if booking.get('room_id'):
            r_oid = to_oid(booking['room_id'])
            if r_oid and rooms_col is not None:
                booking['room'] = rooms_col.find_one({'_id': r_oid})
            else:
                booking['room'] = None
                
        return booking

    @staticmethod
    def get_all(status_filter=None):
        """Get all bookings with optional status filter."""
        col = get_bookings_col()
        if col is None:
            return []
        
        query = {}
        if status_filter and status_filter != 'all':
            query['status'] = status_filter

        bookings = list(col.find(query).sort('created_at', -1))
        return [Booking._populate_relations(b) for b in bookings]

    @staticmethod
    def find_overlapping_bookings(room_id, check_in_str, check_out_str, exclude_booking_id=None):
        """
        Check if room has any active/reserved booking that overlaps with given dates.
        Overlapping condition: (RequestedIn < ExistingOut) AND (RequestedOut > ExistingIn)
        """
        col = get_bookings_col()
        if col is None:
            return []

        query = {
            'room_id': str(room_id),
            'status': {'$in': ['reserved', 'checked_in']},
            'check_in': {'$lt': str(check_out_str)},
            'check_out': {'$gt': str(check_in_str)}
        }

        if exclude_booking_id:
            e_oid = to_oid(exclude_booking_id)
            if e_oid:
                query['_id'] = {'$ne': e_oid}

        return list(col.find(query))

    @staticmethod
    def update_status(booking_id, new_status):
        """Update booking status (reserved -> checked_in -> checked_out / cancelled)."""
        col = get_bookings_col()
        oid = to_oid(booking_id)
        if col is None or not oid:
            return False

        try:
            result = col.update_one(
                {'_id': oid},
                {'$set': {'status': new_status, 'updated_at': datetime.utcnow()}}
            )
            return result.modified_count > 0 or result.matched_count > 0
        except Exception as e:
            print(f"[!] update_status failed: {e}")
            return False

    @staticmethod
    def update_billing(booking_id, food_charges, subtotal, gst, total_amount):
        """Update billing amounts for checkout final invoice."""
        col = get_bookings_col()
        oid = to_oid(booking_id)
        if col is None or not oid:
            return False

        try:
            result = col.update_one(
                {'_id': oid},
                {'$set': {
                    'food_charges': float(food_charges),
                    'subtotal': float(subtotal),
                    'gst': float(gst),
                    'total_amount': float(total_amount),
                    'updated_at': datetime.utcnow()
                }}
            )
            return result.modified_count > 0 or result.matched_count > 0
        except Exception:
            return False

    @staticmethod
    def delete(booking_id):
        """Delete booking record."""
        col = get_bookings_col()
        oid = to_oid(booking_id)
        if col is None or not oid:
            return False
        try:
            result = col.delete_one({'_id': oid})
            return result.deleted_count > 0
        except Exception:
            return False
