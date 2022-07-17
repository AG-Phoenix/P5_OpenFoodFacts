"""Contains the class Store."""

from backend.entity import Entity
from config import api_downloads as api


class Store(Entity):
    """Class represeting stores.

    Inherits from Entity.

    """

    def __init__(self, store_dict):
        super().__init__(store_dict)
        if store_dict["url"] == "":
            self.url = api.STORE_URL + \
                       self.name.lower().replace(" ", "-").replace("'", "-")
        else:
            self.url = store_dict['url']
