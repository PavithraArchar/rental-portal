import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///local.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "supersecretkey")

db = SQLAlchemy(app)
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(200))

@app.route("/")
def home():
    return "Rental Portal Backend Running on Railway 🚀"

@app.route("/init-db")
def init_db():
    db.create_all()
    return "Database Initialized!"

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    user = User(name=data["name"], email=data["email"], password=data["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User Registered Successfully"})

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(email=data["email"]).first()
    if user and user.password == data["password"]:
        token = create_access_token(identity=user.email)
        return jsonify({"token": token})
    return jsonify({"message": "Invalid Credentials"}), 401

if __name__ == "__main__":
    app.run()
