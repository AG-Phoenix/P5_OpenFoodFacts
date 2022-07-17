"""Contains the class APISocket."""

import requests as r
from config import api_downloads as api


class APISocket:
    """This class acts as a socket with the openfoodfacts API.

    Class leverages requests library in order to query APIs over HTTP.
        See requests documentation for additional information. In the
        present case requests are made to the OpenFoodFacts API.
        requests and url are defined in the requests file inside the
        config folder. Refer to OpenFoodFacts API documentation for
        further information :
        https://documenter.getpostman.com/view/8470508/SVtN3Wzy
    """

    def __init__(self):
        """Inits an instance of APISocket."""

        self.raw_categories = []
        self.raw_products = []
        self.cleaned_products = []

    def request_categories(self):
        """Fetches relevant categories from the openfoodfacts API.

        The list of relevant categories is defined in the api downloads
            config file.

        Returns:
            raw_data: The categories retrieved from openfoodfacts.
        """

        print("Requesting categories from the OpenFoodFacts API")
        self.raw_categories = (r.get(f"{api.off_urls['categories']}")).json()
        print("Data received")
        return self.raw_categories

    def request_products(self, category_url):
        """Fetches products from a specific category.

        Args:
            category_url: The url of the specified category.

        Returns:
            raw_data: The list of products retrieved from the API.
        """

        raw_data = (r.get(f"{category_url}.json()&page_size="
                          f"{api.PAGE_SIZE}&fields={api.PROD_FIELDS}")).json()
        self.raw_products = raw_data["products"]

    def cleaning(self):
        """Cleans all products form off using clean_product."""

        for elt in self.raw_products:
            self.clean_product(elt)

    def clean_product(self, elt):
        """Cleans a specified product.

        Makes sure all fields are not empty.
        Gets rid as much as possible of ambiguous or unsupported
            characters.
        Enforeces consistency of capitalization.

        Args:
            elt: The product to parse.
        """

        if "nutrition_grades" \
                and "product_name_fr" \
                and "stores" and "brands" in elt:
            for attribute in elt:
                attribute.lower().strip().capitalize().replace("é", "e")
                attribute.replace("'", " ")
            try:
                if elt["stores"] and elt["brands"] \
                        and elt["nutrition_grades"] and elt["product_name_fr"]:
                    if self.cleaned_products:
                        if self.not_in_clean(elt):
                            self.cleaned_products.append(elt)
                    else:
                        self.cleaned_products.append(elt)
            except KeyError:
                pass

    def not_in_clean(self, elt):
        """Checks if a product is already in the cleaned_product list.

        Args:
            elt: The product to check.

        Returns:
            True if product is NOT in the list.

        """
        for saved in self.cleaned_products:
            if elt["product_name_fr"] == saved["product_name_fr"]\
               and elt["brands"] == saved["brands"]:
                return False
        return True

    def request_cleaned_products(self, category_url):
        """Requests products from OFF and cleans them.

        Args:
            category_url: The url of the categroy from which products
                will be requested.
        """

        self.cleaned_products = []
        self.request_products(category_url)
        self.cleaning()
