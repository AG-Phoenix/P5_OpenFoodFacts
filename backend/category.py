"""Contains the class Category."""

from tabulate import tabulate
from colorama import Style
from config import misc


class Category:
    """Class used to represent categories of product.

    Attributes:
        id: The category's id as stored in the db.
        french_name: The french name of the category.
        url: The OpenFoodFacts url of the product.
        product_registry: list of list, products are stored in the
            registry. Each page is composed of tweenty-five products
            and saved in the registry as a list.
        product_page_buffer: list, A list getting filled with products
            until it reaches a specified page_size.
        buffer_added: A swith to check if the current buffer has been
            appended to the registry in order to print all products.
    """

    def __init__(self, dict_category):
        """Inits a category.

        Args:
            dict_category: A dict containing the attributes of the
                category fetched from OpenFoodFacts.
        """
        self.id = dict_category['id']
        self.french_name = dict_category['name']
        self.url = dict_category['url']
        self.product_registry = []
        self.product_page_buffer = []
        self.buffer_added = False

    def print_category(self):
        """Prints the attributes of a category."""

        print(f"my id : {self.id}")
        print(f"my french_name : {self.french_name}")
        print(f"my url : {self.url}")

    def add_product(self, product):
        """Adds a product to the category;

        Args:
            product: The product to add.
        """

        # Fill page buffer as long as it is under the page size
        if len(self.product_page_buffer) < misc.PAGE_SIZE:
            self.product_page_buffer.append(product)
        # Once a page is full we add it to the registry
        else:
            self.product_registry.append(self.product_page_buffer)
            del self.product_page_buffer
            self.product_page_buffer = []
            self.product_page_buffer.append(product)

    def avoid_empty_registry(self):
        """Makes sure the registry is not empty for printing."""

        if len(self.product_page_buffer) > 0 \
           and len(self.product_registry) == 0:
            self.product_registry.append(self.product_page_buffer)
            self.product_page_buffer = []

    def print_product_registry_page(self, page):
        """Prints a page from the registry of product.

        Args:
            page: The page to print
        """

        # We add the page buffer if it is not empty.
        # this is to prevent not printing products if buffer is not full.
        table = [['n°', 'Name', 'Brands', 'Nutriscore']]
        i = 1
        for elt in self.product_registry[page]:
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
            self.product_registry.append(self.product_page_buffer)
            self.buffer_added = True
