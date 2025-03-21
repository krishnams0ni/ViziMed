from flask import session
from werkzeug.security import check_password_hash
from models import User


def check_credentials():
    if "user_id" not in session:
        return False
    user = User.query.filter_by(id=session["user_id"]).first()
    return user and session.get("authenticated") == True


def confirm_patient_identity(id):
    l = User.query.filter_by(id=session["user_id"]).first().patients
    l = [_.id for _ in l]
    return id in l
