import os
from pymongo import MongoClient, ASCENDING
from config import Config

class Database:
    """MongoDB Connection Manager supporting local MongoDB and MongoDB Atlas."""
    client = None
    db = None

    @classmethod
    def init_db(cls, app=None):
        """Initialize MongoDB connection and setup collection indexes."""
        mongo_uri = Config.MONGO_URI
        db_name = Config.MONGO_DB_NAME

        try:
            cls.client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
            cls.db = cls.client[db_name]
            
            # Setup collection indexes
            cls.setup_indexes()
            print(f"[*] Successfully connected to MongoDB database: {db_name}")
            return cls.db
        except Exception as e:
            print(f"[!] MongoDB Connection Warning: {e}")
            return None

    @classmethod
    def get_db(cls):
        """Get current database instance."""
        if cls.db is None:
            cls.init_db()
        return cls.db

    @classmethod
    def setup_indexes(cls):
        """Create necessary database indexes for fast query lookup and uniqueness."""
        if cls.db is None:
            return

        # Collection: users
        cls.db.users.create_index([("username", ASCENDING)], unique=True)
        cls.db.users.create_index([("email", ASCENDING)], unique=True)

        # Collection: customers
        cls.db.customers.create_index([("email", ASCENDING)], unique=True)

        # Collection: rooms
        cls.db.rooms.create_index([("room_number", ASCENDING)], unique=True)

        # Collection: staff
        cls.db.staff.create_index([("email", ASCENDING)], unique=True)

        # Collection: bookings
        cls.db.bookings.create_index([("customer_id", ASCENDING)])
        cls.db.bookings.create_index([("room_id", ASCENDING)])

    @classmethod
    def get_collection(cls, name):
        """Helper to retrieve specific collection."""
        database = cls.get_db()
        if database is not None:
            return database[name]
        return None

# Export direct collection accessors
def get_users_col():
    return Database.get_collection('users')

def get_customers_col():
    return Database.get_collection('customers')

def get_rooms_col():
    return Database.get_collection('rooms')

def get_bookings_col():
    return Database.get_collection('bookings')

def get_staff_col():
    return Database.get_collection('staff')
