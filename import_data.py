"""
Import JSON files into MongoDB (Data Restore Utility).
"""
import os
import json
from bson import json_util
from database.db import Database, get_users_col, get_customers_col, get_rooms_col, get_staff_col, get_bookings_col

def import_database(input_dir="data_backup"):
    print("=====================================================")
    print("[*] Importing JSON Backup Data into MongoDB")
    print("=====================================================")

    db = Database.init_db()
    if db is None:
        print("[!] Database connection failed.")
        return

    if not os.path.exists(input_dir):
        print(f"[!] Backup directory '{input_dir}' not found.")
        return

    collections = {
        'users.json': get_users_col(),
        'customers.json': get_customers_col(),
        'rooms.json': get_rooms_col(),
        'staff.json': get_staff_col(),
        'bookings.json': get_bookings_col()
    }

    for filename, col in collections.items():
        filepath = os.path.join(input_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                docs = json_util.loads(f.read())
            if docs:
                col.delete_many({})  # Clear existing collection before import
                col.insert_many(docs)
                print(f"  [+] Imported {len(docs)} records from {filename} -> MongoDB")
            else:
                print(f"  [=] File {filename} is empty.")
        else:
            print(f"  [!] File {filename} not found.")

    print("=====================================================")
    print("[+] All JSON data successfully restored to MongoDB!")
    print("=====================================================")

if __name__ == '__main__':
    import_database()
