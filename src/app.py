"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

jackson_family.add_member( {"first_name": "John", "last_name":"Jackson", "age":33, "lucky_numbers": [7,13,22] }) 
jackson_family.add_member( {"first_name": "Jane", "last_name":"Jackson", "age":35, "lucky_numbers": [10,14,3] }) 
jackson_family.add_member( {"first_name": "Jimmy", "last_name":"Jackson", "age":5, "lucky_numbers": [1] }) 


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():
    membres = jackson_family.get_all_members()
    return jsonify(membres), 200

@app.route('/member/<int:member_id>', methods= ['GET'])
def handle_get_member(member_id):
    member = jackson_family.get_member(member_id)
    return jsonify (member), 200



@app.route('/member', methods=['POST'])
def handle_post ():
    data = request.json
    print (data)
    jackson_family.add_member(data)
    return jsonify(), 200


# def handle_post_member():   ////VALIDO TAMBIÉN
#     request_body = request.json
#     jackson_family.add_member(request_body)
#     return jsonify (), 200
           

@app.route('/member/int:member_id', methods=['DELETE'])
def handle_delete(member_id):
    jackson_family.delete_member(member_id)
    return jsonify({"body": {
        "done": True
    }}), 200




# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)








# from flask import Flask, jsonify, request
# from datastructures import jackson_family

# app = Flask(__name__)

# @app.route('/members', methods=['GET'])
# def get_all_members():
#     members = jackson_family.get_all_members()
#     return jsonify(members), 200

# @app.route('/member/<int:member_id>', methods=['GET'])
# def get_member(member_id):
#     print(f"Received request to get member with ID: {member_id}")  # Depuración
#     member = jackson_family.get_member(member_id)
#     if member:
#         print(f"Member found: {member}")  # Depuración
#         return jsonify(member), 200
#     else:
#         print("Member not found")  # Depuración
#         return jsonify({"error": "Member not found"}), 404


# @app.route('/member', methods=['POST'])
# def add_member():
#     data = request.get_json()
#     print(f"Received data: {data}")  # Mensaje de depuración
#     if not data or not data.get('first_name') or not data.get('age') or not isinstance(data.get('lucky_numbers'), list):
#         print("Invalid member data")  # Mensaje de depuración
#         return jsonify({"error": "Invalid member data"}), 400
#     jackson_family.add_member(data)
#     return jsonify(data), 200


# @app.route('/member/<int:member_id>', methods=['DELETE'])
# def delete_member(member_id):
#     print(f"Attempting to delete member with ID: {member_id}")  # Debugging line
#     member = jackson_family.get_member(member_id)
#     if member:
#         print("Member found: {member}")  # Debugging line
#         jackson_family.delete_member(member_id)
#         return jsonify({"done": True}), 200
#     else:
#         print("Member not found")  # Debugging line
#         return jsonify({"error": "Member not found"}), 404


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=3000, debug=True)