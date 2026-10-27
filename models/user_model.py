from datetime import datetime
from bson import ObjectId
from flask_login import UserMixin
from database.db import get_users_col
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class User(UserMixin):
    """User Model representing system staff accounts with role-based permissions."""
    
    def __init__(self, user_data):
        self.id = str(user_data.get('_id'))
        self._id = user_data.get('_id')
        self.username = user_data.get('username')
        self.email = user_data.get('email')
        self.phone = user_data.get('phone', '')
        self.password = user_data.get('password')
        self.role = user_data.get('role', 'receptionist')  # admin, receptionist, manager
        self.created_at = user_data.get('created_at', datetime.utcnow())
        self.is_active_user = user_data.get('is_active', True)

    @property
    def is_active(self):
        return self.is_active_user

    def get_id(self):
        return str(self.id)

    @classmethod
    def create_user(cls, username, email, password, role='receptionist', phone=''):
        """Hashes password with Bcrypt and inserts a new user record into MongoDB."""
        col = get_users_col()
        if col is None:
            return None
            
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user_doc = {
            'username': username.strip(),
            'email': email.lower().strip(),
            'phone': phone.strip() if phone else '',
            'password': hashed_password,
            'role': role.lower().strip(),
            'created_at': datetime.utcnow(),
            'is_active': True
        }
        result = col.insert_one(user_doc)
        user_doc['_id'] = result.inserted_id
        return cls(user_doc)

    @classmethod
    def find_by_id(cls, user_id):
        """Retrieve user by MongoDB ObjectId string."""
        col = get_users_col()
        if col is None or not user_id:
            return None
        try:
            doc = col.find_one({'_id': ObjectId(user_id)})
            return cls(doc) if doc else None
        except Exception:
            return None

    @classmethod
    def find_by_username(cls, username):
        """Find user document by username."""
        col = get_users_col()
        if col is None or not username:
            return None
        doc = col.find_one({'username': username.strip()})
        return cls(doc) if doc else None

    @classmethod
    def find_by_email(cls, email):
        """Find user document by email address."""
        col = get_users_col()
        if col is None or not email:
            return None
        doc = col.find_one({'email': email.lower().strip()})
        return cls(doc) if doc else None

    @classmethod
    def find_by_phone(cls, phone):
        """Find user document by phone number."""
        col = get_users_col()
        if col is None or not phone:
            return None
        doc = col.find_one({'phone': phone.strip()})
        return cls(doc) if doc else None

    @classmethod
    def find_by_identifier(cls, identifier):
        """Find user by Username, Email, OR Phone Number."""
        if not identifier:
            return None
        clean_id = identifier.strip()
        return (
            cls.find_by_email(clean_id) or 
            cls.find_by_username(clean_id) or 
            cls.find_by_phone(clean_id)
        )

    @classmethod
    def get_all(cls):
        """Get all registered system users."""
        col = get_users_col()
        if col is None:
            return []
        docs = col.find().sort('created_at', -1)
        return [cls(doc) for doc in docs]

    def check_password(self, plain_password):
        """Verify plain text password against stored Bcrypt hash."""
        return bcrypt.check_password_hash(self.password, plain_password)

    def is_admin(self):
        return self.role.lower() == 'admin'

    def is_receptionist(self):
        return self.role.lower() == 'receptionist'

    def is_manager(self):
        return self.role.lower() == 'manager'
