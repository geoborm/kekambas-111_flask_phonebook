from app import app, db
from flask import render_template, redirect, url_for, flash 
from app.forms import PhoneForm, LoginForm, SignupForm
from app.models import Address, User
from flask_login import login_user, logout_user, login_required, current_user



@app.route('/')
def index():
    return render_template('index.html')


# @app.route('/add-phone', methods=["GET", "POST"])
# def add_phone():
#     form = PhoneForm()
#     # Check if the form was submitted and is valid
#     if form.validate_on_submit():
#         first = form.first_name.data
#         last = form.last_name.data
#         address = form.address.data
#         phone = form.phone_number.data
#         print(first, last, address, phone)
#         new_contact = Address(first_name=first, last_name=last, address=address, phone_number=phone)
#         flash(f"{new_contact.first_name} {new_contact.last_name} has been added to the phone book", "success")
#         return redirect(url_for('index'))
#     return render_template('add_phone.html', form=form)

@app.route('/sign_up', methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password = form.password.data
        print(email, username)
        check_user = db.session.execute(db.select(User).filter((User.username == username) | (User.email == email))).scalars().all()
        if check_user:
            # Flash a message saying that user with email/username already exists
            flash("A user with that username and/or email already exists", "warning")
            return redirect(url_for('signup'))
        new_user = User(email=email, username=username, password=password)
        flash(f"{new_user.username} has been created!")
        return redirect(url_for('add_phone'))
    return render_template('sign_up.html', form=form)
    

@app.route('/log_in', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print('Form Validated :)')
        email = form.email.data
        password = form.password.data
        print(email, password)
        # Check if there is a user with username and that password
        user = User.query.filter_by(email=email).first()
        if user is not None and user.check_password(password):
            # If the user exists and has the correct password, log them in
            login_user(user)
            flash(f'You have successfully logged in as {email}', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email and/or password. Please try again', 'danger')
            return redirect(url_for('login'))
    return render_template('log_in.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash("You have logged out", "info")
    return redirect(url_for('index'))

@app.route('/add-phone', methods=["GET", "POST"])
@login_required
def add_phone():
    form = PhoneForm()
    # Check if the form was submitted and is valid
    if form.validate_on_submit():
        first = form.first_name.data
        last = form.last_name.data
        address = form.address.data
        phone = form.phone_number.data
        print(first, last, address, phone)
        user = current_user
        u_address = Address(first_name=first, last_name=last, address=address, phone_number=phone)
        user.add_addee(u_address)
        flash(f"{u_address.first_name} {u_address.last_name} has been added to the phone book", "success")
        return redirect(url_for('index'))
    return render_template('add_phone.html', form=form)

@app.route('/edit-phone/<id>', methods=["GET", "POST"])
@login_required 
def edit_phone(id):
    phone_edit = Address.query.get(int(id))
    form = PhoneForm()
    if form.validate_on_submit():
        first = form.first_name.data
        last = form.last_name.data
        address = form.address.data
        phone = form.phone_number.data
        print(first, last, address, phone)
        phone_edit.edit(first_name=first, last_name=last, address=address, phone_number=phone)
        flash(f"{phone_edit.first_name} {phone_edit.last_name} has been edited in the phone book", "success")
        return redirect(url_for('index'))
    return render_template('add_phone.html', form=form)

@app.route('/delete/<id>', methods=["GET", "POST"])
@login_required 
def delete_phone(id):
    phone_delete = Address.query.get(int(id))
    current_user.remove_addee(phone_delete)
    db.session.delete(phone_delete)
    db.session.commit()
    return redirect(url_for('index'))



