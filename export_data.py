"""
Export MongoDB Collections to JSON files (Data Backup Utility).
"""
import os
import json
from bson import json_util
from database.db import Database, get_users_col, get_customers_col, get_rooms_col, get_staff_col, get_bookings_col

def export_database(output_dir="data_backup"):
    print("=====================================================")
    print("[*] Exporting MongoDB Data to JSON Files")
    print("=====================================================")

    db = Database.init_db()
    if db is None:
        print("[!] Database connection failed.")
        return

    os.makedirs(output_dir, exist_ok=True)

    collections = {
        'users.json': get_users_col(),
        'customers.json': get_customers_col(),
        'rooms.json': get_rooms_col(),
        'staff.json': get_staff_col(),
        'bookings.json': get_bookings_col()
    }

    for filename, col in collections.items():
        docs = list(col.find())
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(json_util.dumps(docs, indent=2))
        print(f"  [+] Exported {len(docs)} records -> {filepath}")

    print("=====================================================")
    print(f"[+] All data successfully exported to folder: ./{output_dir}/")
    print("=====================================================")

if __name__ == '__main__':
    export_database()
