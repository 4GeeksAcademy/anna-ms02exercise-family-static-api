from flask import Flask, jsonify, request
from datastructures import jackson_family

app = Flask(__name__)

@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    print(f"Received request to get member with ID: {member_id}")  # Depuración
    member = jackson_family.get_member(member_id)
    if member:
        print(f"Member found: {member}")  # Depuración
        return jsonify(member), 200
    else:
        print("Member not found")  # Depuración
        return jsonify({"error": "Member not found"}), 404


@app.route('/member', methods=['POST'])
def add_member():
    data = request.get_json()
    print(f"Received data: {data}")  # Mensaje de depuración
    if not data or not data.get('first_name') or not data.get('age') or not isinstance(data.get('lucky_numbers'), list):
        print("Invalid member data")  # Mensaje de depuración
        return jsonify({"error": "Invalid member data"}), 400
    jackson_family.add_member(data)
    return jsonify(data), 200


@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    print(f"Attempting to delete member with ID: {member_id}")  # Debugging line
    member = jackson_family.get_member(member_id)
    if member:
        print(f"Member found: {member}")  # Debugging line
        jackson_family.delete_member(member_id)
        return jsonify({"done": True}), 200
    else:
        print("Member not found")  # Debugging line
        return jsonify({"error": "Member not found"}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)