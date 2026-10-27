from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from models.booking_model import Booking
from services.billing_service import BillingService
from utils.decorators import roles_required

billing_bp = Blueprint('billing', __name__, url_prefix='/billing')

@billing_bp.route('/')
@login_required
@roles_required('admin', 'receptionist', 'manager')
def list_invoices():
    """Billing overview listing all completed/billed bookings."""
    bookings = Booking.get_all()
    billed_list = [b for b in bookings if b.get('status') in ['checked_out', 'checked_in', 'reserved']]
    return render_template('billing/list.html', bookings=billed_list)

@billing_bp.route('/invoice/<booking_id>')
@login_required
@roles_required('admin', 'receptionist', 'manager')
def invoice(booking_id):
    """
    Render official GST Hotel Invoice page with itemized charges and Print trigger.
    """
    booking = Booking.find_by_id(booking_id)
    if not booking:
        flash("Booking record not found for invoice generation.", "danger")
        return redirect(url_for('booking.list_bookings'))

    room_price = float(booking.get('room_price', 0.0))
    days = int(booking.get('number_of_days', 1))
    food = float(booking.get('food_charges', 0.0))

    bill_details = BillingService.calculate_bill(room_price, days, food_charges=food)

    invoice_number = f"INV-HTL-{str(booking['_id'])[-6:].upper()}"
    generated_date = datetime.utcnow().strftime("%d %B %Y, %I:%M %p")

    return render_template(
        'billing/invoice.html',
        booking=booking,
        bill=bill_details,
        invoice_number=invoice_number,
        generated_date=generated_date
    )
