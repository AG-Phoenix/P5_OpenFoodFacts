"""Contains class Product."""

from tabulate import tabulate
from colorama import Style
from config import misc


class Product:
    """A class representing products.

    Attributes:
        id: The id of the product. This is the same as in the db.
        name: The product name.
        url: The openfoodfacts url of the product.
        nutrition_grade: The nutrition grade (either A, B, C, D, or E).
        category_off_id: The id of the category of the product.
        stores: The stores in which the product may be found.
    """

    def __init__(self, dict_product):
        """Inits a product.

        Args:
            dict_product: A dict containing attributes of the product
                fetched from OpenFoodFacts.
            category: The category which the product belongs to
        """
        self.id = dict_product['id']
        self.french_name = dict_product['french_name']
        self.url = dict_product['url']
        self.nutrition_grades = dict_product['nutrition_grades']
        self.stores_list = []
        self.brands_list = []
        self.substitute_registry = []
        self.substitute_page_buffer = []
        self.categories_list = []
        self.stores_loaded = False
        self.brands_loaded = False
        self.buffer_added = False

    def print_product(self):
        """prints the attributes of a product."""

        print("\n========================")
        print(f"Name : {self.french_name}")
        print(f"Grade : {self.nutrition_grades}")
        print(f"Url : {self.url}")
        for elt in self.categories_list:
            print(f"Category : {elt.french_name}")
        print("\nBrands:")
        print("============")
        for elt in self.brands_list:
            print(f"{elt.name}")
        print("========================\n")

    def add_substitute(self, substitute):
        """Adds substitute to either the buffer or the registry.

        Args:
            substitute: The substitute to add.
        """

        # Fill page buffer as long as it is under the page size
        if len(self.substitute_page_buffer) < misc.PAGE_SIZE:
            self.substitute_page_buffer.append(substitute)
        # Once a page is full we add it to the registry
        else:
            self.substitute_registry.append(self.substitute_page_buffer)
            self.substitute_page_buffer = []
            self.substitute_page_buffer.append(substitute)

    def print_substitute_registry_page(self, page):
        """Prints a page from the registry of substitutes.

        Args:
            page: The page to print
        """

        # We add the page buffer if it is not empty.
        # this is to prevent not printing substitutes if buffer is not full.
        if page == len(self.substitute_registry):
            self.buffer_check()
        table = [['n°', 'Name', 'Brands', 'Nutriscore']]
        i = 1
        for elt in self.substitute_registry[page]:
            brands_to_print = ""
            name_to_print = elt.french_name
            if len(elt.french_name) > misc.NAME_SIZE:
                name_to_print = f"{elt.french_name[:misc.NAME_SIZE]}" \
                                f"{Style.DIM}...{Style.RESET_ALL}"
            if len(elt.brands_list) == 1:
                brands_to_print += f"{elt.brands_list[0].name}"
            else:
                brands_to_print += f"{elt.brands_list[0].name} " \
                                   f"{Style.DIM}" \
                                   f"+ {len(elt.brands_list) - 1} more..." \
                                   f"{Style.RESET_ALL}"
            table.append([i, name_to_print,
                          brands_to_print, elt.nutrition_grades])
            i += 1
        print(tabulate(table, headers="firstrow", tablefmt="pretty"))

    def buffer_check(self):
        """Appends a buffer to the registry.

        This is to make sure that all items are printed to the user.

        """

        if not self.buffer_added:
            self.substitute_registry.append(self.substitute_page_buffer)
            self.buffer_added = True
