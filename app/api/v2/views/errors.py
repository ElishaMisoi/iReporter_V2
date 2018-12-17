from flask import jsonify

def permission_Error():
    return jsonify({
        "status": 403,
        "message": "You do not have permissions to access this record"
    }), 403


def admin_permission_Error():
    return jsonify({
        "errors": "Administrator cannot create an incident record",
        "status": 403}), 403

def emptyPayload():
    return jsonify({
        "errors": "The payload is empty",
        "status": 400}), 400