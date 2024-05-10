from flask import Flask, render_template, request, jsonify, make_response, redirect
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
)
from flask_pymongo import PyMongo
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId

app = Flask(__name__, static_folder="static", template_folder="templates")
app.config["JWT_SECRET_KEY"] = "super-secret"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
app.config["MONGO_URI"] = "mongodb://localhost:27017/database"
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_COOKIE_CSRF_PROTECT"] = False


jwt = JWTManager(app)
mongo = PyMongo(app)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = mongo.db.users.find_one({"username": username})
        if user and check_password_hash(user["password"], password):
            access_token = create_access_token(identity=str(user["_id"]))
            response = make_response(redirect("/dashboard"))
            response.set_cookie("access_token_cookie", access_token)
            return response
        else:
            return jsonify({"message": "Invalid username or password"}), 401
    return render_template("signin.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        existing_user = mongo.db.users.find_one({"username": username})

        if existing_user:
            return jsonify({"message": "Username already exists"}), 400

        hashed_password = generate_password_hash(password)
        mongo.db.users.insert_one(
            {
                "username": username,
                "password": hashed_password,
                "created_at": datetime.now(),
            }
        )

        return jsonify({"message": "User created successfully"}), 201
    return render_template("signup.html")


@app.route("/dashboard", methods=["GET"])
@jwt_required()
def dashboard():
    current_user = get_jwt_identity()
    user = mongo.db.users.find_one({"_id": ObjectId(current_user)})
    return render_template("dashboard.html", user=user)


@app.route("/logout", methods=["GET"])
def logout():
    response = make_response(redirect("/"))
    response.set_cookie("access_token_cookie", expires=0)
    return response


## API ROUTES
@app.route("/api/tasks/create", methods=["POST"])
@jwt_required()
def create_task():
    current_user = get_jwt_identity()
    user_id = ObjectId(current_user)

    title = request.form.get("title")
    description = request.form.get("description")
    due_date = request.form.get("due_date")

    task = {
        "user_id": user_id,
        "title": title,
        "description": description,
        "due_date": datetime.strptime(due_date, "%Y-%m-%d"),
    }

    mongo.db.tasks.insert_one(task)

    return jsonify({"message": "Task created successfully"}), 201


@app.route("/api/tasks", methods=["GET"])
@jwt_required()
def get_tasks():
    current_user = get_jwt_identity()
    user_id = ObjectId(current_user)

    tasks = list(mongo.db.tasks.find({"user_id": user_id}))

    for task in tasks:
        task["_id"] = str(task["_id"])
        task["user_id"] = str(task["user_id"])

    return jsonify({"tasks": tasks}), 200


if __name__ == "__main__":
    app.run(debug=True)
