from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    """To get alll pictures"""
    if data:
        return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """To get a picture by ID"""
    for picture in data:
        if picture["id"] == id:
            return picture, 200
    return {"message": "ID not found"}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    """To create a picture"""
    obj = request.json

    for element in data:
        if obj["id"] == element["id"]:
            return {"Message": f"picture with id {element['id']} already present"}, 302
    data.append(obj)
    return obj, 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    """To update a picture"""
    obj = request.json

    for index, element in enumerate(data):
        if element["id"] == id:
            data[index] = obj
            return element, 201
    return {"message": "picture not found"}, 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    """To delete a picture by ID"""
    for picture in data:
        if picture['id'] == id:
            data.remove(picture)
            return "", 204
        else:
            return {"message": "picture not found"}, 404
