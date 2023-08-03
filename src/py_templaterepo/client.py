import datetime
from typing import Optional, List

import requests as r
import logging
from . import constants
from .constants import Constants
from .model import *


class Client(object):
    def __init__(self, username: str, password: str, host: Optional[str] = None):
        self.username: str = username
        self.password: str = password
        self.logger: logging.Logger = logging.getLogger("py_templaterepo")
        self.auth_token: str = ""
        self.auth_expiration: Optional[datetime.datetime] = None
        self.items: Optional[Items] = None
        self.constants: Constants = Constants(host)

    def __authenticate(self) -> bool:
        if self.auth_token and self.auth_expiration:
            auth_minutes_remaining = (self.auth_expiration - datetime.datetime.now()).total_seconds() / 60
            if datetime.datetime.now() + datetime.timedelta(minutes=self.constants.auth_expiry_buffer_minutes) > self.auth_expiration:
                self.logger.info(f"The Auth token expires in {auth_minutes_remaining} min, which shorter than the "
                                 f"configured buffer of {self.constants.auth_expiry_buffer_minutes} min, need to refresh")
                self.auth_token = ""
                self.auth_expiration = None
            else:
                return True
        else:
            self.logger.info("Using credentials to authenticate")

        body = {
            "username": self.username,
            "password": self.password
        }

        url = ""
        try:
            url = f"{self.constants.uri_base}{constants.API_PATH_AUTH}"
            headers = self.constants.headers_auth
            response = r.post(url, headers=headers, json=body)
        except Exception as e:
            self.logger.error("Unable to authenticate to %s: %s", url, e)
            return False

        if response.status_code != 200:
            self.logger.error("Auth response code was %s: %s", response.status_code, response.reason)
            return False

        try:
            auth_response = response.json()
        except Exception as e:
            self.logger.error("Could not parse json from auth response: %s. %s", response.content, e)
            return False

        if "data" in auth_response:
            data = auth_response["data"]

            if "token" in data:
                self.auth_token = data["token"]
            if "expiresIn" in data:
                self.auth_expiration = datetime.datetime.now() + datetime.timedelta(milliseconds=data["expiresIn"])
            if "items" in data:
                self.items: Optional[Items] = Items(data["items"])

        if self.auth_token:
            return True
        else:
            self.logger.error("Could not find auth token in response from auth endpoint")
            return False

    def get_devices(self) -> Items:
        self.__authenticate()
        return self.items

    def __get_api(self, klass, **kwargs):
        self.__authenticate()

        path = klass.get_path(**kwargs)

        url = ""
        try:
            url = f"{self.constants.uri_base}{path}"
            headers = self.constants.headers_api.copy()
            headers["authorization"] = f"Bearer {self.auth_token}"

            response = r.get(url, headers=headers)
        except Exception as e:
            self.logger.error("Unable to authenticate to %s: %s", url, e)
            return False

        if response.status_code != 200:
            self.logger.error("Response code was %s: %s", response.status_code, response.reason)
            return False

        try:
            response_json = response.json()
        except Exception as e:
            self.logger.error("Could not parse json from response: %s. %s", response.content, e)
            return False

        if "data" in response_json:
            return klass(api=response_json["data"])
        else:
            return None


if __name__ == "__main__":
    import sys, os

    date_strftime_format = "%y-%b-%d %H:%M:%S"
    message_format = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(format=message_format, datefmt=date_strftime_format, stream=sys.stdout)

    username = os.getenv("ACCOUNT_USERNAME")
    password = os.getenv("ACCOUNT_PASSWORD")
    client = Client(username, password)

    # test methods on client here during development
