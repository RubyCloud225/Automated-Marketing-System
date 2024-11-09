from enum import nonmember
from Login_and_signup import MemberManager, LoginManager
from flask import Flask, request, jsonify

app = Flask(__name__)
connection_string = "database_link"
member_manager = MemberManager(connection_string)
login_manager = LoginManager(connection_string)

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    new_member = member_manager.add_member(name, email, password)

    if new_member:
        return jsonify({"message": "Member Created Successfully!", "id": new_member.MemberId}), 201
    return jsonify({"message": "Error creating member."}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    member = login_manager.login(email, password)

    if member:
        return jsonify({"message": f"Login successful for: {member.name}"}), 200
    return jsonify({"message": "Invalid"})

@app.route('/amend', methods=['PUT'])
def amend():
    data = request.json
    email = data.get('email')
    name = data.get('name')
    password = data.get('password')

    updated_member = member_manager.update_member(email, name, password)
    if updated_member:
        return jsonify({"message": "member updated successfully!"}), 200
    return jsonify({"message": "Error updated member or member not found."}), 404

@app.route('/delete', methods=['DELETE'])
def delete():
    data = request.json
    email = data.get('email')

    if not email:
        return jsonify({"message": "Email is required"}), 400
    deleted = member_manager.delete_member(email)

    if deleted:
        return jsonify({"message": "Member deleted successfully!"}), 200
    return jsonify({"message": "Error deleting member or member not found"}), 404