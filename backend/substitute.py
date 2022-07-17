"""Contains class Substitute."""

from backend.product import Product


class Substitute(Product):
    """A class representing substitutes.

    Inherits from Product.

    Attributes:
        substitute_to: Products that are replaced by this substitute.
        subst_loaded: True if substitutes are loaded in memory.
        original_id: Id of the product in the products table in db.
    """

    def __init__(self, dict_product, original_id):
        """Inits a product.

        Args:
            dict_product: A dict containing attributes of the product
                fetched from OpenFoodFacts.
            category: The category which the product belongs to
        """
        self.substitute_to = []
        self.subst_loaded = False
        self.original_id = original_id
        super().__init__(dict_product)

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
        print("========================\n")
