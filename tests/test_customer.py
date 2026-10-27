import pytest
from models.customer_model import Customer
from database.db import Database
import mongomock

@pytest.fixture
def mock_db():
    Database.client = mongomock.MongoClient()
    Database.db = Database.client['test_customer_db']
    Database.setup_indexes()
    return Database.db

def test_customer_crud_operations(mock_db):
    """Test customer creation, lookup, update, and search."""
    cust = Customer.create(
        full_name='Anita Roy',
        email='anita@example.com',
        phone='9811223344',
        address='Delhi, India',
        id_type='Aadhaar Card',
        id_number='1234-5678-9012'
    )
    assert cust is not None
    assert str(cust['full_name']) == 'Anita Roy'

    # Search customer
    results = Customer.search('Anita')
    assert len(results) == 1
    assert results[0]['phone'] == '9811223344'

    # Update customer
    updated = Customer.update(str(cust['_id']), {'phone': '9900112233'})
    assert updated is True

    fetched = Customer.find_by_id(str(cust['_id']))
    assert fetched['phone'] == '9900112233'
