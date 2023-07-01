import jwt
import datetime
import os
from flask import Flask, request
from flask_mysqldb import MySQL

server = Flask(__name__)
mysql = MySQL(server)

# configs
server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"] = os.environ.get("MYSQL_PORT")


@server.route("/login", methods=["POST"])
def login():
    auth = request.authorization

    if not auth:
        return "missing credentials", 401

    # check if user exists
    cur = mysql.connection.cursor()
    res = cur.execute(
        "SELECT email, password FROM user WHERE email = %s and password ", (auth.username))

    if res > 0:
        user_row = cur.fetchone()
        email, password = user_row[0], user_row[1]

        if auth.username != email and auth.password != password:
            return "invalid credentials", 401
        else:
            return createJWT(auth.username, os.environ.get("JWT_SECRET_KEY"), True)
    else:
        return "Invalid credentials", 404


@server.route("/validate", methods=["POST"])
def validate():
    encoded_jwt = request.headers.get("Authorization")

    if not encoded_jwt:
        return "missing credentials", 401

    encoded_jwt = encoded_jwt.split(" ")[1]

    try:
        decoded_jwt = jwt.decode(encoded_jwt, os.environ.get(
            "JWT_SECRET_KEY"), algorithms=["HS256"])

    except:
        return "not authorized", 403

    return decoded_jwt, 200


def createJWT(username, secret, is_admin):
    return jwt.encode({"username": username, "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1), "iat": datetime.datetime.utcnow(), "admin": is_admin}, secret, algorithm="HS256")


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000)