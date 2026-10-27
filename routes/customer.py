from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from models.customer_model import Customer
from forms.customer_forms import CustomerForm
from services.cloudinary_service import CloudinaryService
from utils.decorators import roles_required

customer_bp = Blueprint('customer', __name__, url_prefix='/customers')

@customer_bp.route('/')
@login_required
@roles_required('admin', 'receptionist', 'manager')
def list_customers():
    """Customer list view with search filter capability."""
    search_query = request.args.get('q', '').strip()
    if search_query:
        customers = Customer.search(search_query)
    else:
        customers = Customer.get_all()

    return render_template('customers/list.html', customers=customers, search_query=search_query)

@customer_bp.route('/add', methods=['GET', 'POST'])
@login_required
@roles_required('admin', 'receptionist', 'manager')
def add_customer():
    """Register new customer and upload ID proof image/document."""
    form = CustomerForm()
    if form.validate_on_submit():
        # Check duplicate email
        if Customer.find_by_email(form.email.data):
            flash("A customer with this email address already exists.", "warning")
            return render_template('customers/add.html', form=form)

        # Upload ID proof file to Cloudinary / storage
        id_proof_url = ""
        if form.id_proof.data:
            try:
                id_proof_url = CloudinaryService.upload_image(form.id_proof.data, folder="id_proofs")
            except Exception as e:
                flash(f"ID Proof Upload warning: {e}", "warning")

        customer = Customer.create(
            full_name=form.full_name.data,
            email=form.email.data,
            phone=form.phone.data,
            address=form.address.data,
            id_type=form.id_type.data,
            id_number=form.id_number.data,
            id_proof_url=id_proof_url
        )

        if customer:
            flash(f"Customer '{form.full_name.data}' added successfully!", "success")
            return redirect(url_for('customer.list_customers'))
        else:
            flash("Failed to add customer. Database error occurred.", "danger")

    return render_template('customers/add.html', form=form)

@customer_bp.route('/<customer_id>')
@login_required
@roles_required('admin', 'receptionist', 'manager')
def customer_details(customer_id):
    """View customer details and uploaded ID proof."""
    customer = Customer.find_by_id(customer_id)
    if not customer:
        flash("Customer not found.", "danger")
        return redirect(url_for('customer.list_customers'))

    return render_template('customers/details.html', customer=customer)

@customer_bp.route('/<customer_id>/edit', methods=['GET', 'POST'])
@login_required
@roles_required('admin', 'receptionist', 'manager')
def edit_customer(customer_id):
    """Edit existing customer details."""
    customer = Customer.find_by_id(customer_id)
    if not customer:
        flash("Customer not found.", "danger")
        return redirect(url_for('customer.list_customers'))

    form = CustomerForm(data=customer)

    if form.validate_on_submit():
        update_data = {
            'full_name': form.full_name.data.strip(),
            'email': form.email.data.lower().strip(),
            'phone': form.phone.data.strip(),
            'address': form.address.data.strip(),
            'id_type': form.id_type.data.strip(),
            'id_number': form.id_number.data.strip()
        }

        # If new ID proof file selected
        if form.id_proof.data:
            try:
                new_url = CloudinaryService.upload_image(form.id_proof.data, folder="id_proofs")
                if new_url:
                    update_data['id_proof_url'] = new_url
            except Exception as e:
                flash(f"File Upload Warning: {e}", "warning")

        success = Customer.update(customer_id, update_data)
        if success:
            flash(f"Customer record for '{form.full_name.data}' updated successfully!", "success")
            return redirect(url_for('customer.customer_details', customer_id=customer_id))
        else:
            flash("Failed to update customer record.", "danger")

    return render_template('customers/edit.html', form=form, customer=customer)

@customer_bp.route('/<customer_id>/delete', methods=['POST'])
@login_required
@roles_required('admin', 'manager')
def delete_customer(customer_id):
    """Delete customer record (Admin and Manager role only)."""
    customer = Customer.find_by_id(customer_id)
    if customer:
        Customer.delete(customer_id)
        flash(f"Customer '{customer.get('full_name')}' deleted successfully.", "info")
    else:
        flash("Customer not found.", "danger")

    return redirect(url_for('customer.list_customers'))
