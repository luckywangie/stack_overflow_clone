from flask import Flask, request, jsonify, Blueprint
from models import db, User, Question

question_bp = Blueprint("question_bp", __name__)

# Create a new question