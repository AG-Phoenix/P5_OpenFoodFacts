"""Contains the class Brand."""

from backend.entity import Entity
from config import api_downloads as api


class Brand(Entity):
    """Class represeting brands.

    Inherits from Entity.

    """

    def __init__(self, brand_dict):
        super().__init__(brand_dict)
        if brand_dict["url"] == "":
            self.url = api.BRAND_URL + self.name.lower().replace(" ", "-")
        else:
            self.url = brand_dict['url']
