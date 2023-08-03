import logging

from typing import List, Optional

from . import constants

logger = logging.getLogger("py_templaterepo")


class ApiResponse(object):
    """A base class object representing an API response."""

    def __init__(self):
        pass

    @staticmethod
    def get_path(**kwargs) -> Optional[str]:
        return None


class ApiResponseObject(ApiResponse):
    """An object representing an API response.
    Parameters
    ----------
    api : `dict`
        A python dict generated from `response.json()`
    """

    def __init__(self, api: dict = None):
        super().__init__()


class ApiResponseObjectList(ApiResponse):
    """An object representing an API response that is a list of objects.
    Parameters
    ----------
    api : `list`
        A python list generated from `response.json()`
    """

    def __init__(self, api: list = None):
        super().__init__()


class Items(ApiResponseObjectList):
    """An object representing a list of API Items
    Parameters
    ----------
    api : `list`
        A python list generated from `response.json()`
    """
    def __init__(self, api: list = None):
        super().__init__(api)

        self.items: List[Item] = []

        if api:
            for item in api:
                if item:
                    self.items.append(Item(item))

    @staticmethod
    def get_path(**kwargs) -> Optional[str]:
        return constants.API_PATH_ITEMS


class Item(ApiResponseObject):
    """API Item
    Parameters
    ----------
    api : `dict`
        API Response object as a python dict.
    """

    def __init__(self, api: dict = None):
        super().__init__(api)

        if api:
            self.id: str = api["id"] if "id" in api else None

    @staticmethod
    def get_path(**kwargs) -> Optional[str]:
        id = kwargs["id"] if "id" in kwargs else None

        if not id:
            logger.error("id parameter is not specified")
            return None

        # noinspection PyStringFormat
        return f"{constants.API_PATH_ITEM}" % id


