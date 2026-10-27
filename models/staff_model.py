from datetime import datetime
from bson import ObjectId
from database.db import get_staff_col

class Staff:
    """Staff Model representing hotel employees."""

    @staticmethod
    def create(name, email, phone, designation, salary, address, joining_date, photo_url=''):
        """Create and store a new staff member record."""
        col = get_staff_col()
        if col is None:
            return None

        staff_doc = {
            'name': name.strip(),
            'email': email.lower().strip(),
            'phone': phone.strip(),
            'designation': designation.strip(),
            'salary': float(salary),
            'address': address.strip(),
            'joining_date': str(joining_date),
            'photo_url': photo_url,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        result = col.insert_one(staff_doc)
        staff_doc['_id'] = result.inserted_id
        return staff_doc

    @staticmethod
    def find_by_id(staff_id):
        """Find staff by MongoDB ObjectId."""
        col = get_staff_col()
        if col is None or not staff_id:
            return None
        try:
            return col.find_one({'_id': ObjectId(staff_id)})
        except Exception:
            return None

    @staticmethod
    def find_by_email(email):
        """Find staff by email address."""
        col = get_staff_col()
        if col is None:
            return None
        return col.find_one({'email': email.lower().strip()})

    @staticmethod
    def get_all():
        """Fetch all staff sorted by creation date."""
        col = get_staff_col()
        if col is None:
            return []
        return list(col.find().sort('created_at', -1))

    @staticmethod
    def search(query):
        """Search staff by name, email, phone, or designation."""
        col = get_staff_col()
        if col is None or not query:
            return Staff.get_all()

        regex_pattern = {'$regex': query.strip(), '$options': 'i'}
        search_filter = {
            '$or': [
                {'name': regex_pattern},
                {'email': regex_pattern},
                {'phone': regex_pattern},
                {'designation': regex_pattern}
            ]
        }
        return list(col.find(search_filter).sort('created_at', -1))

    @staticmethod
    def update(staff_id, update_data):
        """Update existing staff member details."""
        col = get_staff_col()
        if col is None or not staff_id:
            return False

        if 'salary' in update_data:
            update_data['salary'] = float(update_data['salary'])

        update_data['updated_at'] = datetime.utcnow()
        try:
            result = col.update_one(
                {'_id': ObjectId(staff_id)},
                {'$set': update_data}
            )
            return result.modified_count > 0 or result.matched_count > 0
        except Exception:
            return False

    @staticmethod
    def delete(staff_id):
        """Delete staff record."""
        col = get_staff_col()
        if col is None or not staff_id:
            return False
        try:
            result = col.delete_one({'_id': ObjectId(staff_id)})
            return result.deleted_count > 0
        except Exception:
            return False
