from flask import Flask, request, jsonify, Blueprint
from models import db, User

user_bp = Blueprint("user_bp", __name__)

# registering user
@user_bp.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()

    username = data.get("username")
    email = data.get("email")

    if not username or not email:
        return jsonify({"error": "Username and email are required"}), 400
     
    username_exists = User.query.filter_by(username=username).first()
    email_exists = User.query.filter_by(email=email).first()

    if username_exists:
        return jsonify({"error": "Username already exists"}), 400

    if email_exists:
        return jsonify({"error": "Email already exists"}), 400

    new_user = User(username=username, email=email)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"success":"User created successfully"}), 201

# get user by id
@user_bp.route("/users/<user_id>", methods=["GET"])
def fetch_user_by_id(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    user_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_admin": user.is_admin,
        "is_blocked": user.is_blocked,
        "created_at": user.created_at
    }
    return jsonify(user_data), 200

# get all users
@user_bp.route("/users", methods=["GET"])
def fetch_all_users():
    users = User.query.all()

    user_list = []
    for user in users:
        user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_admin": user.is_admin,
            "is_blocked": user.is_blocked,
            "created_at": user.created_at
        }
        user_list.append(user_data)
    return jsonify(user_list), 200

# delete user
@user_bp.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"success": "User deleted successfully"}), 200

#update user
@user_bp.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")

    if username:
        username_exists = User.query.filter(User.username == username, User.id != user_id).first()
        if username_exists:
            return jsonify({"error": "Username already exists"}), 400
        user.username = username
    if email:
        email_exists = User.query.filter(User.email == email, User.id != user_id).first()
        if email_exists:
            return jsonify({"error": "Email already exists"}), 400
        user.email = email

    db.session.commit()
    return jsonify({"success": "User updated successfully"}), 200

    