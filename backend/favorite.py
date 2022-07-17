"""Contains the Class Favorite."""

from backend.substitute import Substitute


class Favorite(Substitute):
    """A class representing favorites.

    Inherits from Substitute.

    Attributes:
        id: The id of the product. This is the same as in the db.
        name: The product name.
        url: The openfoodfacts url of the product.
        nutrition_grade: The nutrition grade (either A, B, C, D, or E).
        category_off_id: The id of the category of the product.
        stores: The stores in which the product may be found.
    """

    def __init__(self, source):
        """Inits a product.

        Args:
            dict_product: A dict containing attributes of the product
                fetched from OpenFoodFacts.
            category: The category which the product belongs to
        """
        if isinstance(source, dict):
            super().__init__(source, source['original_id'])
            self.substitute_to = []
            self.subst_loaded = False
            self.original_id = source['original_id']
        else:
            self.id = source.id
            self.french_name = source.french_name
            self.url = source.url
            self.nutrition_grades = source.nutrition_grades
            self.stores_list = source.stores_list
            self.brands_list = source.brands_list
            self.categories_list = source.categories_list
            self.stores_loaded = source.stores_loaded
            self.brands_loaded = source.brands_loaded
            self.substitute_to = source.substitute_to
            # self.substitute_to = []
            self.subst_loaded = source.subst_loaded
            self.original_id = source.original_id

    def print_product(self):
        """prints the attributes of a product."""

        print("\n========================")
        print(f"Name : {self.french_name}")
        print(f"Grade : {self.nutrition_grades}")
        print(f"Url : {self.url}")
        for elt in self.categories_list:
            print(f"Category : {elt.name}")
        print("\nStores:")
        print("============")
        for elt in self.stores_list:
            print(f"{elt.name}")
        print("\nBrands:")
        print("============")
        for elt in self.brands_list:
            print(f"{elt.name}")
        print("\nSubstitue to:")
        print("============")
        i = 1
        for elt in self.substitute_to:
            print(f"{i}: {elt.french_name}")
            i += 1
        print("========================\n")
