"""
Quick CLI Utility Script to Inspect MongoDB Database Records & Credentials
"""
from database.db import Database, get_users_col, get_customers_col, get_rooms_col, get_staff_col, get_bookings_col

def inspect_database():
    print("=====================================================")
    print("[*] Hotel Management System Database Inspection")
    print("=====================================================")

    db = Database.init_db()
    if db is None:
        print("[!] Connection failed.")
        return

    # Default Seed Credentials Reference
    print("\n[+] DEFAULT ACCOUNTS & PASSWORDS REFERENCE:")
    print("-" * 65)
    print("  • Admin Account:        admin@hotel.com        / Admin@123   (or Phone: 9876543210)")
    print("  • Receptionist Account: receptionist@hotel.com / Receip@123  (or Phone: 9812345678)")
    print("  • Manager Account:      manager@hotel.com      / Manager@123 (or Phone: 9988776655)")

    # 1. Registered System Users in MongoDB
    users = list(get_users_col().find())
    print(f"\n[+] STORED MONGODB USER DOCUMENTS ({len(users)} Total):")
    print("    Note: Passwords are encrypted with Bcrypt hashing ($2b$) for security.")
    print("-" * 65)
    for u in users:
        print(f"  - Username: {u.get('username'):<15} | Email: {u.get('email'):<25} | Role: {u.get('role').upper():<12} | Phone: {u.get('phone', 'N/A')}")
        print(f"    Password Hash: {u.get('password')[:25]}...")

    # 2. Customers / Guests
    customers = list(get_customers_col().find())
    print(f"\n[+] GUESTS / CUSTOMERS ({len(customers)} Total):")
    print("-" * 65)
    for c in customers[:5]:
        print(f"  - {c.get('full_name')} | Email: {c.get('email')} | Phone: {c.get('phone')} | ID: {c.get('id_type')} ({c.get('id_number')})")
    if len(customers) > 5:
        print(f"    ... and {len(customers) - 5} more guests.")

    # 3. Rooms Inventory
    rooms = list(get_rooms_col().find())
    print(f"\n[+] ROOM INVENTORY ({len(rooms)} Total):")
    print("-" * 65)
    for r in rooms[:5]:
        print(f"  - Room {r.get('room_number')} ({r.get('room_type')}) | Rs.{r.get('price_per_day')}/day | Status: {r.get('status').upper()}")
    if len(rooms) > 5:
        print(f"    ... and {len(rooms) - 5} more rooms.")

    # 4. Staff Members
    staff = list(get_staff_col().find())
    print(f"\n[+] STAFF EMPLOYEES ({len(staff)} Total):")
    print("-" * 65)
    for s in staff[:5]:
        print(f"  - {s.get('name')} | Designation: {s.get('designation')} | Salary: Rs.{s.get('salary')}")
    if len(staff) > 5:
        print(f"    ... and {len(staff) - 5} more staff members.")

    # 5. Bookings
    bookings = list(get_bookings_col().find())
    print(f"\n[+] BOOKINGS & STAYS ({len(bookings)} Total):")
    print("-" * 65)
    for b in bookings[:5]:
        print(f"  - Booking #{str(b['_id'])[-6:].upper()} | Dates: {b.get('check_in')} to {b.get('check_out')} | Total: Rs.{b.get('total_amount')} | Status: {b.get('status').upper()}")
    if len(bookings) > 5:
        print(f"    ... and {len(bookings) - 5} more bookings.")

    print("\n=====================================================")
    print("[+] Inspection Complete.")
    print("=====================================================")

if __name__ == '__main__':
    inspect_database()
