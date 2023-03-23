from app import app
from flask import render_template, redirect, url_for, flash
from app.forms import PhoneForm
from app.models import Address

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add-phone', methods=["GET", "POST"])
def add_phone():
    form = PhoneForm()
    # Check if the form was submitted and is valid
    if form.validate_on_submit():
        first = form.first_name.data
        last = form.last_name.data
        address = form.address.data
        phone = form.phone_number.data
        print(first, last, address, phone)
        new_contact = Address(first_name=first, last_name=last, address=address, phone_number=phone)
        flash(f"{new_contact.first_name} {new_contact.last_name} has been added to the phone book", "success")
        return redirect(url_for('index'))
    return render_template('add_phone.html', form=form)
