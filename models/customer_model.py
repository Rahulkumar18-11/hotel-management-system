from datetime import datetime
from bson import ObjectId
from database.db import get_customers_col

class Customer:
    """Customer Model representing hotel guests."""

    @staticmethod
    def create(full_name, email, phone, address, id_type, id_number, id_proof_url=''):
        """Create and store a new customer record."""
        col = get_customers_col()
        if col is None:
            return None

        customer_doc = {
            'full_name': full_name.strip(),
            'email': email.lower().strip(),
            'phone': phone.strip(),
            'address': address.strip(),
            'id_type': id_type.strip(),  # Passport, Aadhaar, Driving License, Voter ID
            'id_number': id_number.strip(),
            'id_proof_url': id_proof_url,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        result = col.insert_one(customer_doc)
        customer_doc['_id'] = result.inserted_id
        return customer_doc

    @staticmethod
    def find_by_id(customer_id):
        """Find customer by MongoDB ObjectId."""
        col = get_customers_col()
        if col is None or not customer_id:
            return None
        try:
            return col.find_one({'_id': ObjectId(customer_id)})
        except Exception:
            return None

    @staticmethod
    def find_by_email(email):
        """Find customer by email address."""
        col = get_customers_col()
        if col is None:
            return None
        return col.find_one({'email': email.lower().strip()})

    @staticmethod
    def get_all(limit=100, skip=0):
        """Fetch all customers sorted by creation date."""
        col = get_customers_col()
        if col is None:
            return []
        return list(col.find().sort('created_at', -1).skip(skip).limit(limit))

    @staticmethod
    def search(query):
        """Search customers by name, email, phone, or ID number."""
        col = get_customers_col()
        if col is None or not query:
            return Customer.get_all()

        regex_pattern = {'$regex': query.strip(), '$options': 'i'}
        search_filter = {
            '$or': [
                {'full_name': regex_pattern},
                {'email': regex_pattern},
                {'phone': regex_pattern},
                {'id_number': regex_pattern}
            ]
        }
        return list(col.find(search_filter).sort('created_at', -1))

    @staticmethod
    def update(customer_id, update_data):
        """Update existing customer details."""
        col = get_customers_col()
        if col is None or not customer_id:
            return False

        update_data['updated_at'] = datetime.utcnow()
        try:
            result = col.update_one(
                {'_id': ObjectId(customer_id)},
                {'$set': update_data}
            )
            return result.modified_count > 0 or result.matched_count > 0
        except Exception:
            return False

    @staticmethod
    def delete(customer_id):
        """Delete customer record."""
        col = get_customers_col()
        if col is None or not customer_id:
            return False
        try:
            result = col.delete_one({'_id': ObjectId(customer_id)})
            return result.deleted_count > 0
        except Exception:
            return False
