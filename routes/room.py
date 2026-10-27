from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from models.room_model import Room
from forms.room_forms import RoomForm
from services.cloudinary_service import CloudinaryService
from utils.decorators import roles_required

room_bp = Blueprint('room', __name__, url_prefix='/rooms')

@room_bp.route('/')
@login_required
@roles_required('admin', 'receptionist', 'manager')
def list_rooms():
    """List rooms with optional status and category filtering."""
    status_filter = request.args.get('status', 'all').strip()
    type_filter = request.args.get('type', 'all').strip()

    rooms = Room.get_all(status_filter=status_filter, room_type_filter=type_filter)
    return render_template(
        'rooms/list.html', 
        rooms=rooms, 
        selected_status=status_filter, 
        selected_type=type_filter
    )

@room_bp.route('/add', methods=['GET', 'POST'])
@login_required
@roles_required('admin', 'manager')
def add_room():
    """Create new room inventory record and upload photograph (Admin and Manager only)."""
    form = RoomForm()
    if form.validate_on_submit():
        # Check unique room number
        if Room.find_by_number(form.room_number.data):
            flash(f"Room Number '{form.room_number.data}' already exists in inventory.", "warning")
            return render_template('rooms/add.html', form=form)

        # Upload image to Cloudinary / storage
        image_url = ""
        if form.image.data:
            try:
                image_url = CloudinaryService.upload_image(form.image.data, folder="rooms")
            except Exception as e:
                flash(f"Image Upload Warning: {e}", "warning")

        room = Room.create(
            room_number=form.room_number.data,
            room_type=form.room_type.data,
            price_per_day=form.price_per_day.data,
            capacity=form.capacity.data,
            description=form.description.data,
            image_url=image_url
        )

        if room:
            flash(f"Room '{form.room_number.data}' added successfully to inventory!", "success")
            return redirect(url_for('room.list_rooms'))
        else:
            flash("Failed to add room to database.", "danger")

    return render_template('rooms/add.html', form=form)

@room_bp.route('/<room_id>')
@login_required
@roles_required('admin', 'receptionist', 'manager')
def room_details(room_id):
    """View room details and occupancy status."""
    room = Room.find_by_id(room_id)
    if not room:
        flash("Room not found.", "danger")
        return redirect(url_for('room.list_rooms'))

    return render_template('rooms/details.html', room=room)

@room_bp.route('/<room_id>/edit', methods=['GET', 'POST'])
@login_required
@roles_required('admin', 'manager')
def edit_room(room_id):
    """Edit room parameters (Admin & Manager)."""
    room = Room.find_by_id(room_id)
    if not room:
        flash("Room not found.", "danger")
        return redirect(url_for('room.list_rooms'))

    form = RoomForm(data=room)

    if form.validate_on_submit():
        update_data = {
            'room_number': str(form.room_number.data).strip(),
            'room_type': form.room_type.data,
            'price_per_day': float(form.price_per_day.data),
            'capacity': int(form.capacity.data),
            'status': form.status.data,
            'description': form.description.data.strip()
        }

        if form.image.data:
            try:
                new_img = CloudinaryService.upload_image(form.image.data, folder="rooms")
                if new_img:
                    update_data['image_url'] = new_img
            except Exception as e:
                flash(f"Image Upload Warning: {e}", "warning")

        success = Room.update(room_id, update_data)
        if success:
            flash(f"Room '{form.room_number.data}' updated successfully!", "success")
            return redirect(url_for('room.room_details', room_id=room_id))
        else:
            flash("Failed to update room record.", "danger")

    return render_template('rooms/edit.html', form=form, room=room)

@room_bp.route('/<room_id>/status', methods=['POST'])
@login_required
@roles_required('admin', 'manager', 'receptionist')
def update_status(room_id):
    """Quick toggle room status (available / maintenance / booked)."""
    new_status = request.form.get('status')
    if new_status in ['available', 'booked', 'maintenance']:
        Room.update_status(room_id, new_status)
        flash(f"Room status updated to {new_status.upper()}.", "success")
    else:
        flash("Invalid room status value.", "danger")

    return redirect(url_for('room.list_rooms'))

@room_bp.route('/<room_id>/delete', methods=['POST'])
@login_required
@roles_required('admin')
def delete_room(room_id):
    """Delete room inventory record (Admin only)."""
    room = Room.find_by_id(room_id)
    if room:
        Room.delete(room_id)
        flash(f"Room '{room.get('room_number')}' deleted successfully.", "info")
    else:
        flash("Room not found.", "danger")

    return redirect(url_for('room.list_rooms'))
