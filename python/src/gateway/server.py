import os
from flask import Flask, request, send_file
from flask_pymongo import PyMongo
import gridfs
import pika
import json
from auth import validate
from auth_svc import access
from storage import util
import logging
from bson.objectid import ObjectId

server = Flask(__name__)


mongo_video = PyMongo(
    server, uri="mongodb://host.minikube.internal:27017/videos")
mongo_mp3 = PyMongo(server, uri="mongodb://host.minikube.internal:27017/mp3s")

fs_videos = gridfs.GridFS(mongo_video.db)
fs_mp3s = gridfs.GridFS(mongo_mp3.db)

connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()


@server.route("/login", methods=["POST"])
def login():
    print("login request received")

    token, err = access.login(request)

    if not err:
        server.logger.info("login successful")
        return token, 200
    else:
        logging.error("Login error")
        return err


@server.route("/upload", methods=["POST"])
def upload():
    access, err = validate.token(request)

    if err:
        return err

    access = json.loads(access)

    if access["admin"]:

        if len(request.files) > 1 or len(request.files) < 1:
            return "exactly one file required", 400

        for _, f in request.files.items():
            err = util.upload_file(f, fs_videos, channel, access)

            if err:
                return err

        return "success!", 200

    else:
        return "not authorized", 401


@server.route("/download", methods=["GET"])
def download():
    access, err = validate.token(request)

    if err:
        return err

    access = json.loads(access)

    if access["admin"]:
        fid_string = request.args.get("fid")

        if not fid_string:
            return "fid required", 400

        try:
            out = fs_mp3s.get(ObjectId(fid_string))
            return send_file(out, download_name=fid_string + ".mp3")

        except Exception as err:
            logging.error("Error: ", err)
            return "internal server error", 500

    return "not authorized", 401


if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO)
        server.run(host="0.0.0.0", port=8080, debug=True)
    except Exception as err:
        print(err)
