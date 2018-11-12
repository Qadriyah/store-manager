from flask_jwt_extended import (
    verify_jwt_in_request, get_jwt_claims
)
from flask import jsonify
from functools import wraps

from api import jwt
from models.models import User


def admin_required(fn):
    """
    Ensures that JWT is present in the request and that a user 
    has a role of admin in the access token
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_data = get_jwt_claims()
        if user_data["roles"] != "admin":
            return jsonify({"msg": "Admin previlidges required"}), 403
        return fn(*args, **kwargs)
    return wrapper


def attendant_required(fn):
    """
    Ensures that JWT is present in the request and that a user 
    has a role of attendant in the access token
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_data = get_jwt_claims()
        if user_data["roles"] != "attendant":
            return jsonify({"msg": "Attendants only"}), 403
        return fn(*args, **kwargs)
    return wrapper


@jwt.user_claims_loader
def add_claims_to_access_token(user):
    """
    Defines what custom claims should be added to the access token

    Args:
        user(User): User object

    Returns:
        dict: Claims added to the access token
    """
    return {
        "id": user.id,
        "fullname": user.fullname,
        "username": user.username,
        "roles": user.roles
    }


@jwt.user_identity_loader
def user_identity_lookup(user):
    """
    Defines what the identity of the access token should be

    Args:
        user(User): User object

    Returns:
        str: Identity of the access token
    """
    return user.username


@jwt.user_loader_callback_loader
def user_loader_callback(identity):
    claims = get_jwt_claims()
    if claims["username"] != identity:
        return None

    return User(
        id=claims["id"],
        fullname=claims["fullname"],
        username=identity,
        password="",
        roles=claims["roles"],
        created_at=""
    )
