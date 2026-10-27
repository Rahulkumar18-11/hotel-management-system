from datetime import datetime, date
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from models.booking_model import Booking
from models.customer_model import Customer
from models.room_model import Room
from forms.booking_forms import BookingForm, CheckoutForm
from services.booking_service import BookingService
from services.billing_service import BillingService
from utils.decorators import roles_required

booking_bp = Blueprint('booking', __name__, url_prefix='/bookings')

@booking_bp.route('/')
@login_required
@roles_required('admin', 'receptionist', 'manager')
def list_bookings():
    """List all reservations and stay records with status filter."""
    status_filter = request.args.get('status', 'all').strip()
    bookings = Booking.get_all(status_filter=status_filter)
    return render_template('bookings/list.html', bookings=bookings, selected_status=status_filter)

@booking_bp.route('/add', methods=['GET', 'POST'])
@login_required
@roles_required('admin', 'receptionist', 'manager')
def add_booking():
    """Create a new booking reservation enforcing double-booking validation."""
    form = BookingForm()

    # Populate customer and room select dropdown choices
    customers = Customer.get_all()
    rooms = Room.get_all()

    form.customer_id.choices = [(str(c['_id']), f"{c['full_name']} ({c['phone']})") for c in customers]
    form.room_id.choices = [(str(r['_id']), f"Room {r['room_number']} - {r['room_type']} (₹{r['price_per_day']}/day)") for r in rooms]

    if request.method == 'GET':
        # Pre-select room if passed via URL parameter
        pre_room = request.args.get('room_id')
        if pre_room:
            form.room_id.data = pre_room
        form.check_in.data = date.today()

    if form.validate_on_submit():
        check_in_str = form.check_in.data.strftime('%Y-%m-%d')
        check_out_str = form.check_out.data.strftime('%Y-%m-%d')

        booking, msg = BookingService.create_booking(
            customer_id=form.customer_id.data,
            room_id=form.room_id.data,
            check_in_str=check_in_str,
            check_out_str=check_out_str,
            created_by=getattr(current_user, 'username', 'Staff')
        )

        if booking:
            flash(msg, "success")
            return redirect(url_for('booking.booking_details', booking_id=str(booking['_id'])))
        else:
            flash(msg, "danger")

    return render_template('bookings/add.html', form=form, customers=customers, rooms=rooms)

@booking_bp.route('/<booking_id>')
@login_required
@roles_required('admin', 'receptionist', 'manager')
def booking_details(booking_id):
    """View booking record details, customer info, room info, and charges."""
    booking = Booking.find_by_id(booking_id)
    if not booking:
        flash("Booking record not found.", "danger")
        return redirect(url_for('booking.list_bookings'))

    return render_template('bookings/details.html', booking=booking)

@booking_bp.route('/<booking_id>/checkin', methods=['GET', 'POST'])
@login_required
@roles_required('admin', 'receptionist', 'manager')
def check_in(booking_id):
    """Process guest Check-In."""
    success, msg = BookingService.check_in_guest(booking_id)
    if success:
        flash(msg, "success")
    else:
        flash(msg, "danger")

    return redirect(url_for('booking.booking_details', booking_id=booking_id))


@booking_bp.route('/<booking_id>/checkout', methods=['GET', 'POST'])
@login_required
@roles_required('admin', 'receptionist', 'manager')
def check_out(booking_id):
    """Process guest Check-Out, enter food charges, and render invoice link."""
    booking = Booking.find_by_id(booking_id)
    if not booking:
        flash("Booking record not found.", "danger")
        return redirect(url_for('booking.list_bookings'))

    form = CheckoutForm()

    if form.validate_on_submit():
        food_charges = form.food_charges.data or 0.0
        success, msg = BookingService.check_out_guest(booking_id, final_food_charges=food_charges)

        if success:
            flash(msg, "success")
            return redirect(url_for('billing.invoice', booking_id=booking_id))
        else:
            flash(msg, "danger")

    # Initial bill preview calculation
    room_price = float(booking.get('room_price', 0.0))
    days = int(booking.get('number_of_days', 1))
    current_food = float(booking.get('food_charges', 0.0))
    bill = BillingService.calculate_bill(room_price, days, food_charges=current_food)

    return render_template('bookings/checkout.html', booking=booking, form=form, bill=bill)

@booking_bp.route('/<booking_id>/cancel', methods=['GET', 'POST'])
@login_required
@roles_required('admin', 'manager', 'receptionist')
def cancel_booking(booking_id):

    """Cancel booking and set room back to available."""
    booking = Booking.find_by_id(booking_id)
    if booking:
        Booking.update_status(booking_id, 'cancelled')
        Room.update_status(booking.get('room_id'), 'available')
        flash("Booking has been cancelled.", "info")
    else:
        flash("Booking not found.", "danger")

    return redirect(url_for('booking.list_bookings'))

@booking_bp.route('/api/calculate-price', methods=['POST'])
@login_required
def api_calculate_price():
    """Live Ajax API to calculate total cost live on booking form entry."""
    data = request.get_json() or {}
    room_id = data.get('room_id')
    check_in = data.get('check_in')
    check_out = data.get('check_out')
    food_charges = float(data.get('food_charges', 0.0))

    if not (room_id and check_in and check_out):
        return jsonify({'error': 'Missing parameters'}), 400

    room = Room.find_by_id(room_id)
    if not room:
        return jsonify({'error': 'Room not found'}), 404

    days = BookingService.calculate_stay_days(check_in, check_out)
    is_avail, avail_msg = BookingService.is_room_available(room_id, check_in, check_out)

    bill = BillingService.calculate_bill(room.get('price_per_day', 0.0), days, food_charges)
    bill['available'] = is_avail
    bill['avail_msg'] = avail_msg

    return jsonify(bill)
