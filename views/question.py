from flask import Flask, request, jsonify, Blueprint
from models import db, User, Question

question_bp = Blueprint("question_bp", __name__)

# Create a new question
@question_bp.route("/questions", methods=["POST"])
def create_question():
    data = request.get_json()
    title = data.get("title")
    body = data.get("body")
    tags = data.get("tags")
    user_id = data.get("user_id")

    if not title or not body or not tags or not user_id:
        return jsonify({"error": "All fields (title, body, tags, user_id) are required"}), 400

    # Check if title exists
    if Question.query.filter_by(title=title).first():
        return jsonify({"error": "Title already exists"}), 400

    # Check if user exists
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User ID does not exist"}), 404

    new_question = Question(title=title, body=body, tags=tags, user_id=user_id)
    db.session.add(new_question)
    db.session.commit()

    return jsonify({"success": "Question created successfully"}), 201

# Get all questions
@question_bp.route("/questions", methods=["GET"])
def get_all_questions():
    questions = Question.query.all()

    question_list = []
    for q in questions:
        question_data = {
            "id": q.id,
            "title": q.title,
            "body": q.body,
            "tags": q.tags,
            "is_approved": q.is_approved,
            "created_at": q.created_at,
            "user": {
                "id": q.user.id,
                "username": q.user.username,
                "email": q.user.email
            }
        }
        question_list.append(question_data)

    return jsonify(question_list), 200

#get question_by id
@question_bp.route("/questions/<question_id>", methods=["GET"])
def get_question_by_id(question_id):
    question = Question.query.get(question_id)

    if not question:
        return jsonify({"error": "Question not found"}), 404

    user_data = {
        "id": question.user.id,
        "username": question.user.username,
        "email": question.user.email
    }

    question_data = {
        "id": question.id,
        "title": question.title,
        "body": question.body,
        "tags": question.tags,
        "is_approved": question.is_approved,
        "created_at": question.created_at,
        "user": user_data
    }

    return jsonify(question_data), 200

# Update question
@question_bp.route("/questions/<question_id>", methods=["PUT"])
def update_question(question_id):
    question = Question.query.get(question_id)

    if not question:
        return jsonify({"error": "Question not found"}), 404

    data = request.get_json()
    title = data.get("title")
    body = data.get("body")
    tags = data.get("tags")

    if title:
        existing = Question.query.filter(Question.title == title, Question.id != question.id).first()
        if existing:
            return jsonify({"error": "Title already used by another question"}), 400
        question.title = title

    if body:
        question.body = body

    if tags:
        question.tags = tags

    db.session.commit()
    return jsonify({"success": "Question updated successfully"}), 200

# Delete question
@question_bp.route("/questions/<question_id>", methods=["DELETE"])
def delete_question(question_id):
    question = Question.query.get(question_id)

    if not question:
        return jsonify({"error": "Question not found"}), 404

    db.session.delete(question)
    db.session.commit()
    return jsonify({"success": "Question deleted successfully"}), 200



