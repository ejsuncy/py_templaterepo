API_HOST = "api.templaterepo.com"
API_PATH_AUTH = "v1/auth/signin"
API_PATH_ITEMS = "v1/items"
API_PATH_ITEM = "v1/item/%s"

API_HEADERS = {
    "connection": "keep-alive",
    "accept": "application/json, text/plain, */*",
    "user-agent": "iQua/3 CFNetwork/1333.0.4 Darwin/21.5.0",
    "accept-language": "en-us",
    "accept-encoding": "gzip, deflate, br"
}


class Constants(object):
    def __init__(self, host=API_HOST):
        self.host = host if host else API_HOST
        self.uri_base = f"https://{self.host}/"
        self.headers_api = API_HEADERS.copy()
        self.headers_api["host"] = self.host
        self.headers_auth = API_HEADERS.copy()
        self.headers_auth["content-type"] = "application/json;charset=utf-8"
        self.auth_expiry_buffer_minutes = 10
