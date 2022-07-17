"""Contains the class Entity."""

from config import misc


class Entity:
    """Class representing entity which can be linked to a product.

    This class is not used directly by the program.
    Brand and Store both inherit from this class.

    Args:
        entity_dict: dict, All the entity attributes which need to be
            processed.

    Attributes:
        id: int, The id of the entity.
        name: str, the entity name.
        product_registry: list of list, products are stored in the
            registry. Each page is composed of tweenty-five products
            and saved in the registry as a list.
        product_page_buffer: list, A list getting filled with products
            until it reaches a specified page_size.

    """

    def __init__(self, entity_dict):
        self.id = entity_dict['id']
        self.name = entity_dict['name']
        self.product_page_buffer = []
        self.product_registry = []

    def add_product(self, product):
        """Adds a product to the entity.

        Args:
            product: The product to add.
        """

        # Fill page buffer as long as it is under the page size
        if len(self.product_page_buffer) < misc.PAGE_SIZE:
            self.product_page_buffer.append(product)
        # Once a page is full we add it to the registry
        else:
            self.product_registry.append(self.product_page_buffer)
            self.product_page_buffer = []
            self.product_page_buffer.append(product)
