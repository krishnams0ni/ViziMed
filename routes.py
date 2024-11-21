import os
from flask import render_template, request, flash, redirect, url_for, session, send_from_directory
from models import db, Patient, PatientLog
from security import *


def register_routes(app):
    @app.route('/')
    def init():
        if check_credentials():
            flash("You are already logged in")
            return redirect(url_for('dashboard'))
        else:
            flash("Welcome back!")
            return render_template("login.html")

    @app.route('/login', methods=['POST', 'GET'])
    def login():
        if request.method == 'POST':
            username = request.form.get("username")
            password = request.form.get("password")
            user = User.query.filter_by(username=username).first()
            if user and user.password == password:
                session['user_id'] = user.id
                session['username'] = user.username
                session['password'] = user.password
                flash("Logged in successfully")
                return redirect(url_for('dashboard'))
            else:
                flash("Invalid credentials")
        else:
            flash("Welcome back!")
        return render_template("login.html")

    @app.route('/register', methods=['POST', 'GET'])
    def register():
        flash("Welcome!")
        if request.method == 'POST':
            username = request.form.get("username")
            password = request.form.get("password")
            confirm_password = request.form.get("confirm_password")
            if not username or not password:
                flash("Please fill all the fields")
            elif confirm_password != password:
                flash("Passwords do not match")
            elif User.query.filter_by(username=username).first():
                flash("Username already exists")
            else:
                new_user = User(username=username, password=password)
                db.session.add(new_user)
                db.session.commit()
                flash("Account created successfully")
                return render_template('login.html')
        return render_template("register.html")

    @app.route('/dashboard')
    def dashboard():
        if not check_credentials(): return redirect(url_for('login'))
        info = User.query.filter_by(id=session['user_id']).first().patients
        flash("Patients retrieved successfully")
        return render_template("dashboard.html", info=info)

    @app.route('/profile', methods=['POST', 'GET'])
    def profile():
        if not check_credentials(): return redirect(url_for('login'))
        id = session['user_id']
        name = User.query.filter_by(id=id).first().username
        password = User.query.filter_by(id=id).first().password
        if request.method == 'POST':
            new_password = request.form.get("password")
            new_username = request.form.get("username")
            user = User.query.filter_by(id=id).first()

            if not new_password and not new_username:
                flash("Please fill at least one field")
            if new_password:
                confirm_password = request.form.get("confirm_password")
                if new_password != confirm_password:
                    flash("Passwords do not match")
                else:
                    user.password = new_password
                    db.session.commit()
                    flash("Password updated successfully")
                    session['password'] = new_password
            if new_username:
                if new_username in [_.username for _ in User.query.all()]:
                    flash("Username already exists")
                else:
                    user.username = new_username
                    db.session.commit()
                    flash("Username updated successfully")
                    session['username'] = new_username
            return redirect(url_for('profile'))
        return render_template("profile.html", name=name, password=password)

    @app.route('/add_patient', methods=['POST', 'GET'])
    def add_patient():
        if not check_credentials(): return redirect(url_for('login'))
        if request.method == 'POST':
            name = request.form.get("name")
            dob = request.form.get("dob")
            phone = request.form.get("phone")
            email = request.form.get("email")
            address = request.form.get("address")
            user_id = session['user_id']
            new_patient = Patient(name=name, dob=dob if dob else "N/A", phone=phone if phone else "N/A",
                email=email if email else "N/A", address=address if address else "N/A", user_id=user_id)
            db.session.add(new_patient)
            db.session.commit()
            flash("Patient added successfully")
        return render_template("add_patient.html")

    @app.route('/remove_patient/<int:id>', methods=['GET'])
    def remove_patient(id):
        if not check_credentials(): return redirect(url_for('login'))
        if not confirm_patient_identity(id):
            flash("You are not authorized to remove this patient")
            return redirect(url_for('dashboard'))

        patient = Patient.query.filter_by(id=id).first()
        db.session.delete(patient)
        db.session.commit()
        flash("Patient removed successfully")
        return redirect(url_for('dashboard'))

    @app.route('/patient_logs/<int:id>', methods=['POST', 'GET'])
    def patient_logs(id):
        if not confirm_patient_identity(id):
            flash("You are not authorized to view this patient's logs")
            return redirect(url_for('dashboard'))
        if not check_credentials(): return redirect(url_for('login'))

        logs = PatientLog.query.filter_by(patient_id=id).all()
        if not os.path.exists('static/images'):
            os.makedirs('static/images')
        if request.method == 'POST':
            notes = request.form.get("notes")
            date = request.form.get("date")
            if date in [_.date for _ in logs]:
                flash("Log already exists for this date")
                return render_template("patient_logs.html", logs=logs, patient_id=id)

            new_log = PatientLog(patient_id=id, date=date, notes=notes)
            db.session.add(new_log)
            db.session.commit()

            file = request.files.get("file")
            if file:
                path = f"static/images/{new_log.id}_{file.filename}"
                if os.path.exists(path):
                    flash("Image already exists")
                else:
                    file.save(path)
                    if new_log.images_path is None:
                        new_log.images_path = []
                    new_log.images_path.append(path)

            flash("Log added successfully")
            db.session.commit()
        else:
            flash("Logs retrieved successfully")
        logs = PatientLog.query.filter_by(patient_id=id).all()
        return render_template("patient_logs.html", logs=logs, patient_id=id, name=Patient.query.filter_by(id=id).first().name)

    @app.route('/update_log/<int:id>', methods=['POST', 'GET'])
    def update_log(id):
        if not check_credentials(): return redirect(url_for('login'))
        log = PatientLog.query.filter_by(id=id).first()
        if request.method == 'POST':
            log.date = request.form.get("date") or log.date
            log.notes = request.form.get("notes")
            file = request.files.get("file")

            if file:
                path = f"static/images/{id}_{file.filename}"
                if os.path.exists(path):
                    flash("Image already exists")
                else:
                    file.save(path)
                    if log.images_path is None:
                        log.images_path = []
                    log.images_path.append(path)

            db.session.commit()
            flash("Log updated successfully")
            return redirect(url_for('patient_logs', id=log.patient_id))
        return render_template("patient_logs.html", log=log)

    @app.route('/edit_patient/<int:id>', methods=['POST', 'GET'])
    def edit_patient(id):
        if not check_credentials(): return redirect(url_for('login'))
        if not confirm_patient_identity(id): return redirect(url_for('dashboard'))

        patient = Patient.query.filter_by(id=id).first()
        if request.method == 'POST':
            patient.dob = request.form.get("dob") or patient.dob
            patient.phone = request.form.get("phone") or patient.phone
            patient.email = request.form.get("email") or patient.email
            patient.address = request.form.get("address") or patient.address
            patient.name = request.form.get("name") or patient.name
            db.session.commit()
            flash("Patient details updated successfully")
        return redirect(url_for('dashboard'))

    @app.route('/delete_log/<int:id>', methods=['GET'])
    def delete_log(id):
        if not check_credentials(): return redirect(url_for('login'))
        log = PatientLog.query.filter_by(id=id).first()
        files = log.images_path
        for file in files:
            os.remove(file)
        db.session.delete(log)
        db.session.commit()
        flash("Log deleted successfully")
        return redirect(url_for('patient_logs', id=log.patient_id))

    @app.route('/delete_image/<int:id>', methods=['GET'])
    def delete_image(id):
        if not check_credentials(): return redirect(url_for('login'))
        log = PatientLog.query.filter_by(id=id).first()
        path = log.images_path.pop()
        os.remove(path)
        db.session.commit()
        flash("Image deleted successfully")
        return redirect(url_for('patient_logs', id=log.patient_id))

    @app.route('/image_functions', methods=['GET'])
    def image_functions():
        if not check_credentials(): return redirect(url_for('login'))
        path = request.args.get('path')
        relative_path = path[len('static/'):]
        return send_from_directory('static', relative_path)

    @app.route('/logout')
    def logout():
        session.pop('user_id', None)
        flash("Logged out successfully")
        return redirect(url_for('login'))

    @app.route('/delete_account')
    def delete_account():
        if not check_credentials(): return redirect(url_for('login'))
        id = session['user_id']
        user = User.query.filter_by(id=id).first()
        db.session.delete(user)
        db.session.commit()
        session.pop('user_id', None)
        flash("Account deleted successfully")
        return redirect(url_for('login'))
