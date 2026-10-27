from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from models.staff_model import Staff
from forms.staff_forms import StaffForm
from services.cloudinary_service import CloudinaryService
from utils.decorators import admin_required, roles_required

staff_bp = Blueprint('staff', __name__, url_prefix='/staff')

@staff_bp.route('/')
@login_required
@roles_required('admin', 'manager')
def list_staff():
    """List staff members with search functionality (Admin & Manager)."""
    search_query = request.args.get('q', '').strip()
    if search_query:
        staff_list = Staff.search(search_query)
    else:
        staff_list = Staff.get_all()

    return render_template('staff/list.html', staff_list=staff_list, search_query=search_query)

@staff_bp.route('/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_staff():
    """Add a new staff member and upload photograph (Admin Only)."""
    form = StaffForm()
    if form.validate_on_submit():
        if Staff.find_by_email(form.email.data):
            flash("A staff member with this email address already exists.", "warning")
            return render_template('staff/add.html', form=form)

        photo_url = ""
        if form.photo.data:
            try:
                photo_url = CloudinaryService.upload_image(form.photo.data, folder="staff_photos")
            except Exception as e:
                flash(f"Photo Upload Warning: {e}", "warning")

        joining_date_str = form.joining_date.data.strftime('%Y-%m-%d')

        staff = Staff.create(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            designation=form.designation.data,
            salary=form.salary.data,
            address=form.address.data,
            joining_date=joining_date_str,
            photo_url=photo_url
        )

        if staff:
            flash(f"Staff record for '{form.name.data}' added successfully!", "success")
            return redirect(url_for('staff.list_staff'))
        else:
            flash("Failed to create staff record.", "danger")

    return render_template('staff/add.html', form=form)

@staff_bp.route('/<staff_id>')
@login_required
@roles_required('admin', 'manager')
def staff_details(staff_id):
    """View detailed staff profile."""
    staff = Staff.find_by_id(staff_id)
    if not staff:
        flash("Staff member not found.", "danger")
        return redirect(url_for('staff.list_staff'))

    return render_template('staff/details.html', staff=staff)

@staff_bp.route('/<staff_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_staff(staff_id):
    """Edit staff member parameters (Admin Only)."""
    staff = Staff.find_by_id(staff_id)
    if not staff:
        flash("Staff member not found.", "danger")
        return redirect(url_for('staff.list_staff'))

    form = StaffForm(data=staff)

    if form.validate_on_submit():
        update_data = {
            'name': form.name.data.strip(),
            'email': form.email.data.lower().strip(),
            'phone': form.phone.data.strip(),
            'designation': form.designation.data.strip(),
            'salary': float(form.salary.data),
            'address': form.address.data.strip(),
            'joining_date': form.joining_date.data.strftime('%Y-%m-%d')
        }

        if form.photo.data:
            try:
                new_photo = CloudinaryService.upload_image(form.photo.data, folder="staff_photos")
                if new_photo:
                    update_data['photo_url'] = new_photo
            except Exception as e:
                flash(f"Photo Upload Warning: {e}", "warning")

        success = Staff.update(staff_id, update_data)
        if success:
            flash(f"Staff record for '{form.name.data}' updated successfully!", "success")
            return redirect(url_for('staff.staff_details', staff_id=staff_id))
        else:
            flash("Failed to update staff record.", "danger")

    return render_template('staff/edit.html', form=form, staff=staff)

@staff_bp.route('/<staff_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_staff(staff_id):
    """Delete staff member record (Admin Only)."""
    staff = Staff.find_by_id(staff_id)
    if staff:
        Staff.delete(staff_id)
        flash(f"Staff member '{staff.get('name')}' deleted successfully.", "info")
    else:
        flash("Staff member not found.", "danger")

    return redirect(url_for('staff.list_staff'))
