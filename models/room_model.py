from datetime import datetime
from bson import ObjectId
from database.db import get_rooms_col

def to_oid(val):
    if not val:
        return None
    if isinstance(val, ObjectId):
        return val
    try:
        return ObjectId(str(val))
    except Exception:
        return None

class Room:
    """Room Model representing physical hotel rooms."""

    @staticmethod
    def create(room_number, room_type, price_per_day, capacity, description='', image_url=''):
        """Create a new room in MongoDB."""
        col = get_rooms_col()
        if col is None:
            return None

        room_doc = {
            'room_number': str(room_number).strip(),
            'room_type': room_type.strip(),  # Single, Double, Deluxe, Suite
            'price_per_day': float(price_per_day),
            'capacity': int(capacity),
            'status': 'available',  # available, booked, maintenance
            'description': description.strip(),
            'image_url': image_url,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        result = col.insert_one(room_doc)
        room_doc['_id'] = result.inserted_id
        return room_doc

    @staticmethod
    def find_by_id(room_id):
        """Find room document by ObjectId."""
        col = get_rooms_col()
        oid = to_oid(room_id)
        if col is None or not oid:
            return None
        try:
            return col.find_one({'_id': oid})
        except Exception:
            return None

    @staticmethod
    def find_by_number(room_number):
        """Find room by room number string."""
        col = get_rooms_col()
        if col is None:
            return None
        return col.find_one({'room_number': str(room_number).strip()})

    @staticmethod
    def get_all(status_filter=None, room_type_filter=None):
        """Get all rooms with optional filtering by status or room type."""
        col = get_rooms_col()
        if col is None:
            return []

        query = {}
        if status_filter and status_filter != 'all':
            query['status'] = status_filter
        if room_type_filter and room_type_filter != 'all':
            query['room_type'] = room_type_filter

        return list(col.find(query).sort('room_number', 1))

    @staticmethod
    def get_available():
        """Retrieve all currently available rooms."""
        return Room.get_all(status_filter='available')

    @staticmethod
    def update_status(room_id, new_status):
        """Update room status ('available', 'booked', 'maintenance')."""
        col = get_rooms_col()
        oid = to_oid(room_id)
        if col is None or not oid:
            return False

        if new_status not in ['available', 'booked', 'maintenance']:
            return False

        try:
            result = col.update_one(
                {'_id': oid},
                {'$set': {'status': new_status, 'updated_at': datetime.utcnow()}}
            )
            return result.modified_count > 0 or result.matched_count > 0
        except Exception as e:
            print(f"[!] Room update_status failed: {e}")
            return False

    @staticmethod
    def update(room_id, update_data):
        """Update full room data."""
        col = get_rooms_col()
        oid = to_oid(room_id)
        if col is None or not oid:
            return False

        if 'price_per_day' in update_data:
            update_data['price_per_day'] = float(update_data['price_per_day'])
        if 'capacity' in update_data:
            update_data['capacity'] = int(update_data['capacity'])

        update_data['updated_at'] = datetime.utcnow()
        try:
            result = col.update_one(
                {'_id': oid},
                {'$set': update_data}
            )
            return result.modified_count > 0 or result.matched_count > 0
        except Exception:
            return False

    @staticmethod
    def delete(room_id):
        """Delete room record."""
        col = get_rooms_col()
        oid = to_oid(room_id)
        if col is None or not oid:
            return False
        try:
            result = col.delete_one({'_id': oid})
            return result.deleted_count > 0
        except Exception:
            return False
