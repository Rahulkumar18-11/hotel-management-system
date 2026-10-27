"""
Expanded Database Seeding Script for Hotel Management System.
Populates 20+ Rooms with room images, 20+ Guests/Customers, 15+ Staff Members, System Users, and 15+ Bookings.
"""
from datetime import datetime, timedelta
from database.db import Database, get_users_col, get_customers_col, get_rooms_col, get_staff_col, get_bookings_col
from models.user_model import User
from models.customer_model import Customer
from models.room_model import Room
from models.staff_model import Staff
from models.booking_model import Booking
from services.billing_service import BillingService

def seed_database():
    print("=====================================================")
    print("[*] Starting Hotel Management System Database Seeding")
    print("=====================================================")

    db = Database.init_db()
    if db is None:
        print("[!] Database connection failed. Ensure MongoDB is running.")
        return

    # Clear existing collections to refresh with large realistic dataset
    get_users_col().delete_many({})
    get_customers_col().delete_many({})
    get_rooms_col().delete_many({})
    get_staff_col().delete_many({})
    get_bookings_col().delete_many({})
    print("[+] Cleared old sample collections.")

    # Curated High-Quality Hotel Room Image URLs by Category
    single_images = [
        "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1595526114035-0d45ed16cfbf?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1566665797739-1674de7a421a?auto=format&fit=crop&w=800&q=80"
    ]
    
    double_images = [
        "https://images.unsplash.com/photo-1618773928121-c32242e63f39?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1590490360182-c33d57733427?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1591088398332-8a7791972843?auto=format&fit=crop&w=800&q=80"
    ]

    deluxe_images = [
        "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=800&q=80"
    ]

    suite_images = [
        "https://images.unsplash.com/photo-1611892440504-42a792e24d32?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1596394516093-501ba68a0ba6?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80"
    ]

    # 1. Seed System Users (Admins, Receptionists, Managers)
    print("[+] Seeding 10 System User Accounts...")
    User.create_user('admin', 'admin@hotel.com', 'Admin@123', role='admin', phone='9876543210')
    User.create_user('receptionist', 'receptionist@hotel.com', 'Receip@123', role='receptionist', phone='9812345678')
    User.create_user('manager', 'manager@hotel.com', 'Manager@123', role='manager', phone='9988776655')
    User.create_user('receptionist2', 'sarah.reception@hotel.com', 'Receip@123', role='receptionist', phone='9765432109')
    User.create_user('receptionist3', 'david.frontdesk@hotel.com', 'Receip@123', role='receptionist', phone='9654321098')
    User.create_user('manager2', 'robert.opsmanager@hotel.com', 'Manager@123', role='manager', phone='9543210987')
    User.create_user('admin2', 'system.admin2@hotel.com', 'Admin@123', role='admin', phone='9432109876')

    User.create_user('staff_user1', 'anita.staff@hotel.com', 'Receip@123', role='receptionist')
    User.create_user('staff_user2', 'vikram.staff@hotel.com', 'Receip@123', role='receptionist')
    User.create_user('finance_mgr', 'finance.manager@hotel.com', 'Manager@123', role='manager')

    # 2. Seed 20+ Hotel Rooms with Room Images
    print("[+] Seeding 20 Hotel Rooms with High-Res Photographs...")
    rooms_data = [
        ('101', 'Single', 1500.0, 1, 'available', 'Standard single bed room with high-speed Wi-Fi and AC.', single_images[0]),
        ('102', 'Single', 1600.0, 1, 'available', 'Cozy single room facing quiet garden lawn.', single_images[1]),
        ('103', 'Double', 2500.0, 2, 'booked', 'Spacious double room with queen bed and LED TV.', double_images[0]),
        ('104', 'Double', 2600.0, 2, 'available', 'Double bed room with city view and mini fridge.', double_images[1]),
        ('105', 'Deluxe', 3800.0, 3, 'available', 'Luxury deluxe room with king bed and balcony.', deluxe_images[0]),
        
        ('201', 'Double', 2700.0, 2, 'booked', 'Executive double room with work desk and tea maker.', double_images[2]),
        ('202', 'Deluxe', 4000.0, 3, 'booked', 'Deluxe family room with dual queen beds.', deluxe_images[1]),
        ('203', 'Deluxe', 4200.0, 3, 'available', 'Corner deluxe suite featuring panoramic windows.', deluxe_images[2]),
        ('204', 'Single', 1800.0, 1, 'maintenance', 'Single room currently undergoing routine HVAC servicing.', single_images[2]),
        ('205', 'Suite', 6000.0, 4, 'booked', 'Premium junior suite with living area and sofa.', suite_images[0]),

        ('301', 'Suite', 6500.0, 4, 'available', 'Executive suite with private jacuzzi and ocean view.', suite_images[1]),
        ('302', 'Suite', 7000.0, 4, 'booked', 'Presidential suite featuring master bedroom and dining.', suite_images[2]),
        ('303', 'Deluxe', 4500.0, 3, 'available', 'Deluxe room with plush seating and bath tub.', deluxe_images[0]),
        ('304', 'Double', 2800.0, 2, 'available', 'Double room on 3rd floor with hill view.', double_images[0]),
        ('305', 'Single', 1900.0, 1, 'available', 'Single room equipped with ergonomic workspace.', single_images[0]),

        ('401', 'Suite', 8000.0, 5, 'available', 'Grand Royal Suite with private rooftop terrace.', suite_images[0]),
        ('402', 'Deluxe', 4800.0, 3, 'available', 'Deluxe suite with high-ceiling modern interior.', deluxe_images[1]),
        ('403', 'Double', 3000.0, 2, 'maintenance', 'Double room undergoing bathroom renovation.', double_images[1]),
        ('404', 'Single', 2000.0, 1, 'available', 'Top floor single room with quiet environment.', single_images[1]),
        ('405', 'Suite', 7500.0, 4, 'available', 'Penthouse suite with panoramic skyline views.', suite_images[1])
    ]

    created_rooms = []
    for rnum, rtype, price, cap, status, desc, img in rooms_data:
        r = Room.create(rnum, rtype, price, cap, description=desc, image_url=img)
        if r:
            Room.update_status(r['_id'], status)
            created_rooms.append(r)

    # 3. Seed 20+ Customer/Guest Records
    print("[+] Seeding 20 Guest / Customer Records...")
    customers_data = [
        ('Rahul Sharma', 'rahul.sharma@example.com', '9876543210', '12 Park Street, Mumbai, MS', 'Aadhaar Card', 'AADHAR-1029-3847'),
        ('Priya Patel', 'priya.patel@example.com', '9812345678', '45 MG Road, Bengaluru, KA', 'Passport', 'PASS-IND-998877'),
        ('Vikram Singh', 'vikram.singh@example.com', '9988776655', '78 Sector 17, Chandigarh, PB', 'Driving License', 'DL-PB-2024-9988'),
        ('Ananya Roy', 'ananya.roy@example.com', '9765432109', '34 Park Street, Kolkata, WB', 'Voter ID', 'VOTER-WB-88776'),
        ('Siddharth Malhotra', 'siddharth.m@example.com', '9898989898', '89 Jubilee Hills, Hyderabad, TS', 'Aadhaar Card', 'AADHAR-5544-3322'),
        
        ('Kavita Krishnan', 'kavita.k@example.com', '9123456789', '56 Anna Salai, Chennai, TN', 'Passport', 'PASS-IND-112233'),
        ('Arjun Kapoor', 'arjun.k@example.com', '9234567890', '12 Connaught Place, New Delhi, DL', 'Government Issued ID', 'GOVT-DL-44556'),
        ('Meera Joshi', 'meera.joshi@example.com', '9345678901', '67 FC Road, Pune, MH', 'Aadhaar Card', 'AADHAR-9900-1122'),
        ('Rohan Mehta', 'rohan.mehta@example.com', '9456789012', '23 CG Road, Ahmedabad, GJ', 'Driving License', 'DL-GJ-2023-7766'),
        ('Neha Gupta', 'neha.gupta@example.com', '9567890123', '90 Civil Lines, Jaipur, RJ', 'Passport', 'PASS-IND-334455'),

        ('Aman Verma', 'aman.verma@example.com', '9678901234', '11 Hazratganj, Lucknow, UP', 'Aadhaar Card', 'AADHAR-7788-9900'),
        ('Divya Nair', 'divya.nair@example.com', '9789012345', '44 MG Road, Kochi, KL', 'Voter ID', 'VOTER-KL-55667'),
        ('Karan Johar', 'karan.j@example.com', '9890123456', '88 Marine Drive, Mumbai, MH', 'Passport', 'PASS-IND-667788'),
        ('Shweta Tripathi', 'shweta.t@example.com', '9901234567', '22 Mall Road, Shimla, HP', 'Aadhaar Card', 'AADHAR-3322-1100'),
        ('Varun Dhawan', 'varun.d@example.com', '9012345678', '99 Linking Road, Mumbai, MH', 'Driving License', 'DL-MH-2025-1234'),

        ('Pooja Hegde', 'pooja.h@example.com', '9112233445', '55 Banjara Hills, Hyderabad, TS', 'Aadhaar Card', 'AADHAR-6677-8899'),
        ('Rishabh Pant', 'rishabh.p@example.com', '9223344556', '77 Rajpur Road, Dehradun, UK', 'Passport', 'PASS-IND-778899'),
        ('Smriti Mandhana', 'smriti.m@example.com', '9334455667', '33 Sangli Road, Pune, MH', 'Driving License', 'DL-MH-2024-5544'),
        ('Shreyas Iyer', 'shreyas.i@example.com', '9445566778', '14 Worli Sea Face, Mumbai, MH', 'Aadhaar Card', 'AADHAR-8899-0011'),
        ('Kriti Sanon', 'kriti.s@example.com', '9556677889', '66 Vasant Vihar, New Delhi, DL', 'Passport', 'PASS-IND-223344')
    ]

    created_customers = []
    for name, email, phone, addr, idt, idn in customers_data:
        c = Customer.create(name, email, phone, addr, idt, idn)
        if c:
            created_customers.append(c)

    # 4. Seed 15+ Staff Members
    print("[+] Seeding 15 Staff Employee Records...")
    staff_data = [
        ('Amit Verma', 'amit.v@hotel.com', '9822110033', 'Front Desk Manager', 45000.0, 'Churchgate, Mumbai', '2022-01-15'),
        ('Sunita Reddy', 'sunita.r@hotel.com', '9844332211', 'Executive Housekeeper', 32000.0, 'Indiranagar, Bengaluru', '2022-05-10'),
        ('Rajesh Khanna', 'chef.rajesh@hotel.com', '9911223344', 'Head Executive Chef', 65000.0, 'Bandra West, Mumbai', '2021-11-01'),
        ('Deepak Saxena', 'deepak.s@hotel.com', '9777888999', 'Chief Security Officer', 38000.0, 'Vashi, Navi Mumbai', '2023-02-01'),
        ('Anjali Rao', 'anjali.rao@hotel.com', '9666555444', 'Guest Relations Lead', 40000.0, 'Koramangala, Bengaluru', '2023-04-18'),

        ('Manish Pandey', 'manish.p@hotel.com', '9555444333', 'Chief Maintenance Engineer', 42000.0, 'Whitefield, Bengaluru', '2022-08-20'),
        ('Pooja Banerjee', 'pooja.b@hotel.com', '9444333222', 'Spa & Wellness Director', 48000.0, 'Juhu, Mumbai', '2023-01-05'),
        ('Suresh Iyer', 'suresh.i@hotel.com', '9333222111', 'Senior Accountant', 50000.0, 'T Nagar, Chennai', '2021-06-12'),
        ('Rina Sen', 'rina.sen@hotel.com', '9222111000', 'Concierge Executive', 30000.0, 'Salt Lake, Kolkata', '2023-07-01'),
        ('Gaurav Bhatia', 'gaurav.b@hotel.com', '9111000999', 'Food & Beverage Supervisor', 35000.0, 'CP, New Delhi', '2022-10-15'),

        ('Tanya Deshmukh', 'tanya.d@hotel.com', '9000999888', 'Front Desk Executive', 28000.0, 'Thane, Maharashtra', '2023-09-10'),
        ('Kunal Kapoor', 'kunal.k@hotel.com', '9888777666', 'Sous Chef', 40000.0, 'Andheri East, Mumbai', '2023-03-25'),
        ('Nisha Sharma', 'nisha.s@hotel.com', '9777666555', 'Housekeeping Supervisor', 29000.0, 'HSR Layout, Bengaluru', '2023-08-14'),
        ('Rakesh Nambiar', 'rakesh.n@hotel.com', '9666555777', 'IT & Systems Manager', 55000.0, 'Gachibowli, Hyderabad', '2022-03-01'),
        ('Preeti Kulkarni', 'preeti.k@hotel.com', '9555666777', 'HR Executive', 36000.0, 'Kothrud, Pune', '2023-02-15')
    ]

    for name, email, phone, desig, sal, addr, jdate in staff_data:
        Staff.create(name, email, phone, desig, sal, addr, jdate)

    # 5. Seed 15+ Active, Reserved, and Checked Out Bookings
    print("[+] Seeding 15 Active, Reserved, and Checked Out Bookings...")
    today = datetime.utcnow().date()

    if len(created_customers) >= 10 and len(created_rooms) >= 10:
        bookings_data = [
            (created_customers[0], created_rooms[2], today - timedelta(days=2), today + timedelta(days=2), 500.0, 'checked_in'),
            (created_customers[1], created_rooms[4], today - timedelta(days=1), today + timedelta(days=3), 800.0, 'checked_in'),
            (created_customers[2], created_rooms[5], today, today + timedelta(days=2), 0.0, 'reserved'),
            (created_customers[3], created_rooms[6], today - timedelta(days=4), today - timedelta(days=1), 1200.0, 'checked_out'),
            (created_customers[4], created_rooms[9], today + timedelta(days=1), today + timedelta(days=4), 0.0, 'reserved'),

            (created_customers[5], created_rooms[11], today - timedelta(days=3), today, 650.0, 'checked_out'),
            (created_customers[6], created_rooms[1], today, today + timedelta(days=3), 200.0, 'reserved'),
            (created_customers[7], created_rooms[3], today - timedelta(days=5), today - timedelta(days=2), 1500.0, 'checked_out'),
            (created_customers[8], created_rooms[7], today - timedelta(days=1), today + timedelta(days=1), 400.0, 'checked_in'),
            (created_customers[9], created_rooms[10], today + timedelta(days=2), today + timedelta(days=5), 0.0, 'reserved'),

            (created_customers[10], created_rooms[12], today - timedelta(days=6), today - timedelta(days=3), 900.0, 'checked_out'),
            (created_customers[11], created_rooms[13], today - timedelta(days=2), today + timedelta(days=1), 350.0, 'checked_in'),
            (created_customers[12], created_rooms[14], today + timedelta(days=3), today + timedelta(days=6), 0.0, 'reserved'),
            (created_customers[13], created_rooms[15], today - timedelta(days=7), today - timedelta(days=2), 2500.0, 'checked_out'),
            (created_customers[14], created_rooms[16], today, today + timedelta(days=4), 600.0, 'reserved')
        ]

        for cust, room, cin, cout, food, bstatus in bookings_data:
            cin_str = cin.strftime('%Y-%m-%d')
            cout_str = cout.strftime('%Y-%m-%d')
            days = (cout - cin).days or 1
            rprice = float(room.get('price_per_day', 2000.0))
            bill = BillingService.calculate_bill(rprice, days, food_charges=food)

            Booking.create(
                customer_id=cust['_id'],
                room_id=room['_id'],
                check_in=cin_str,
                check_out=cout_str,
                number_of_days=days,
                room_price=rprice,
                food_charges=food,
                subtotal=bill['subtotal'],
                gst=bill['gst'],
                total_amount=bill['total_amount'],
                created_by='admin',
                status=bstatus
            )
            if bstatus in ['checked_in', 'reserved']:
                Room.update_status(room['_id'], 'booked')
            elif bstatus == 'checked_out':
                Room.update_status(room['_id'], 'available')

    print("=====================================================")
    print("[+] Seeding Completed Successfully with Room Images!")
    print("=====================================================")

if __name__ == '__main__':
    seed_database()
