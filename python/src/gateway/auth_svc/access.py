import os
import requests
import logging


def login(request):

    auth = request.authorization

    if not auth:
        return None, ("missing credentials", 401)

    basicAuth = (auth.username, auth.password)

    logging.error("Sending request to auth service at: " +
                  os.environ.get("AUTH_SVC_ADDRESS") + "/login")

    response = requests.post(
        f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/login", auth=basicAuth)

    logging.error("Response from the auth service: ")
    logging.error(response)

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)
