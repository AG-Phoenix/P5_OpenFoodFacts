"""Contains class Brain which handles non-user facing operations."""

from tabulate import tabulate
from colorama import Style, Fore
from backend.category import Category
from backend.product import Product
from backend.brand import Brand
from backend.store import Store
from backend.substitute import Substitute
from backend.favorite import Favorite
from backend.api_socket import APISocket
from backend.db_socket import DBSocket
from config import database_connection as db_info
from config import api_downloads as api
from config import misc


class Brain:
    """Class handling all operations which are not user facing.

   This Class leverages api_socket module to establish connections to
    the API as well as db_socket to perform operations on the database.

    Attributes:
        - apis: An instance of APISocket
        - dbs: An instance of DBSocket
        - categories_list: a list containing categories.
        - saved_sub_buf: a list of saved substitutes.
        - subst_reg: A list of saved_sub_buf.
        - latest_saved_id: The id of the latest favorites in db.
        - Stores list: a list of stores
        - Brands list: a list of brands
    """

    def __init__(self):
        """Inits an instance of the program backend.

        Sockets are open with both the api and the database.
        If the database is not empty, fills program memory with data
            form the db.
        """

        self.dbs = DBSocket(db_info.mariadb['sql_file'])
        self.apis = APISocket()
        self.categories_list = []
        self.saved_sub_buf = []
        self.last_saved_id = 0
        self.subst_reg = []
        self.stores_list = []
        self.brands_list = []
        self.buffer_added = False
        if not self.dbs.db_is_empty:
            self.fill_from_db()

    def add_substitute_to_saved_list(self, fav):
        """Saves saved substitutes in a list.

        Args:
            substitute: The substitute to save.
        """

        # Fill page buffer as long as it is under the page size
        # fav = Favorite(substitute)
        if len(self.saved_sub_buf) < misc.PAGE_SIZE:
            if self.subst_reg:
                len_registry = len(self.subst_reg)
                if len(self.subst_reg[len_registry - 1]) < misc.PAGE_SIZE:
                    self.subst_reg[len_registry - 1].append(fav)
                else:
                    self.saved_sub_buf.append(fav)
                    self.buffer_added = False
            else:
                self.saved_sub_buf.append(fav)
                self.buffer_added = False
        # Once a page is full we add it to the registry
        else:
            self.subst_reg.append(self.saved_sub_buf)
            self.saved_sub_buf = []
            self.saved_sub_buf.append(fav)
            self.buffer_added = False
        return fav

    def print_subst_reg_page(self, page):
        """Prints the saved substitutes from a specified page.

        Args:
            page: int, Index of the page to print.
        """

        # We add the page buffer if it is not empty.
        # this is to prevent not printing substitutes if buffer is not full.
        table = [['n°', 'Name', 'Brands', 'Nutriscore', 'Substitute to']]
        i = 1
        for elt in self.subst_reg[page]:
            self.fetch_prod_from_fav(elt)
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
            sb_to_prt = ""
            # Just assigning a shorter name.
            subs = elt.substitute_to
            if len(subs) == 1:
                if len(subs[0].french_name) > misc.NAME_SIZE:
                    sb_to_prt += f"{subs[0].french_name[:misc.NAME_SIZE]}" \
                                 f"{Style.DIM}...{Style.RESET_ALL}"
                else:
                    sb_to_prt += f"{subs[0].french_name}"
            else:
                if len(subs[0].french_name) > misc.NAME_SIZE:
                    sb_to_prt += f"{subs[0].french_name[:misc.NAME_SIZE]} " \
                                 f"{Style.DIM}" \
                                 f"+ {len(subs) - 1} more..." \
                                 f"{Style.RESET_ALL}"
                else:
                    sb_to_prt += f"{subs[0].french_name} " \
                                 f"{Style.DIM}" \
                                 f"+ {len(subs) - 1} more..." \
                                 f"{Style.RESET_ALL}"
            table.append([i, name_to_print, brands_to_print,
                          elt.nutrition_grades, sb_to_prt])
            i += 1
        print(tabulate(table, headers="firstrow", tablefmt="pretty"))

    def buffer_check(self):
        """Appends a buffer to the registry.

        This is to make sure that all items are printed to the user.

        """

        if not self.buffer_added:
            self.subst_reg.append(self.saved_sub_buf)
            self.buffer_added = True

    def fill_saved_product_from_db_v2(self):
        """Fills saved product in memory with data from db."""

        rows = self.dbs.get_saved_products()
        for row in rows:
            favorite = Favorite(row)
            self.fetch_brands_from_fav(favorite)
            self.fetch_stores_from_fav(favorite)
            self.fetch_prod_from_fav(favorite)
            self.add_substitute_to_saved_list(favorite)
        if self.saved_sub_buf or self.subst_reg:
            result = self.dbs.get_max_id_from_fav()
            for line in result:
                self.last_saved_id = line['MAX( id )']

    def add_subst_to_saved_list(self, subst):
        fav = Favorite(subst)
        self.add_substitute_to_saved_list(fav)

    def fill_categories_from_off_v2(self):
        """Fills the category table in the database"""

        # get request openfoodfacts for categories.json
        # raw_data = self.apis.request_categories()

        print("Inserting data into DB")
        dict_category = {}
        for elt in api.CAT_ENDPOINT:
            dict_category["id"] = len(self.categories_list) + 1
            dict_category['name'] = elt.replace("-", " ").capitalize()
            dict_category["url"] = api.BASE_CAT_URL + elt
            category = Category(dict_category)
            self.dbs.cat_insertion_v2(category)
            self.categories_list.append(category)

    def fill_categories_from_db(self):
        """Fills the categories from database.

        The method makes use of method get_categories() from class
            DBSocket to get categories from the program database.
        The method creates instances of class Category with each
            category it gathers.
        Refer to get_categories() documentation inside DBSocket and
            class Category documentation for additional information.
        """

        print("Database is not empty. Filling it.")
        rows = self.dbs.get_categories()
        for row in rows:
            self.categories_list.append(Category(row))
            self.fill_products_from_db()

    def fill_products_from_db(self):
        """Fills product in memory with data from the database."""

        for category in self.categories_list:
            products = self.dbs.get_products_from_cat(category)
            for product_raw in products:
                product = Product(product_raw)
                category.add_product(product)
                product.categories_list.append(category)

    def fill_brands_from_db(self):
        """Fills brands in memory with data from the db."""

        rows = self.dbs.get_brands()
        for row in rows:
            self.brands_list.append(Brand(row))

    def fill_stores_from_db(self):
        """Fills stores in memory with data from the db."""
        rows = self.dbs.get_stores()
        for row in rows:
            self.stores_list.append(Store(row))

    def fill_products_from_off_v3(self):
        """Fills product in database and memory with data from off."""

        i = 1
        store_i = 1
        brand_i = 1
        for category in self.categories_list:
            print(f"Downloading {category.french_name}...")
            self.apis.request_cleaned_products(category.url)
            print("data received")
            for elt in self.apis.cleaned_products:
                elt["french_name"] = elt["product_name_fr"]
                elt["id"] = i
                product = Product(elt)
                if self.dbs.product_insertion_v2(product):
                    i += 1
                    category.add_product(product)
                    self.dbs.cat_prod_insertion(category, product)
                    product.categories_list.append(category)
                    stores_tags = elt["stores"]
                    for off_store in stores_tags.split(','):
                        dict_store = {
                            'id': store_i,
                            'name': off_store.strip().lower(),
                            'url': ""
                        }
                        self.store_saving(Store(dict_store), product)
                    brand_tags = elt["brands"]
                    for off_brand in brand_tags.split(','):
                        dict_brand = {
                            'id': brand_i,
                            'name': off_brand.strip().lower(),
                            'url': ""
                        }
                        self.brand_saving(Brand(dict_brand), product)
        self.dbs.connection.commit()

    def store_saving(self, store, product):
        """Adds stores pulled from the api in memory and in db.

        Args:
            store: The store to handle.
            product: Product that can be found in the store.
        """

        i = 0
        store_exists = False
        for elt in self.stores_list:
            if store.name == elt.name:
                product.stores_list.append(self.stores_list[i])
                self.stores_list[i].add_product(product)
                self.dbs.prod_stores_insertion(product, self.stores_list[i])
                store_exists = True
            i += 1
        if not store_exists:
            store.id = len(self.stores_list) + 1
            product.stores_list.append(store)
            store.add_product(product)
            self.dbs.store_insertion(store)
            self.dbs.prod_stores_insertion(product, store)
            self.stores_list.append(store)
        product.stores_loaded = True

    def brand_saving(self, brand, product):
        """Adds brands pulled from the api in memory and in db.

        Args:
            brand: The brand to handle.
            product: Product that can be found in the brand.
        """

        i = 0
        brand_exists = False
        for elt in self.brands_list:
            if brand.name == elt.name:
                product.brands_list.append(self.brands_list[i])
                self.brands_list[i].add_product(product)
                self.dbs.prod_brands_insertion(product, self.brands_list[i])
                brand_exists = True
            i += 1
        if not brand_exists:
            brand.id = len(self.brands_list) + 1
            product.brands_list.append(brand)
            brand.add_product(product)
            self.dbs.brand_insertion(brand)
            self.dbs.prod_brands_insertion(product, brand)
            self.brands_list.append(brand)
        product.brands_loaded = True

    def fetch_prod_from_fav(self, fav):
        """Fetch products in fatabase for a given favorite.

        Args:
            fav: The chosen favorite.
        """

        if not fav.subst_loaded:
            db_prods = self.dbs.get_prod_from_fav(fav.id)
            for prod in db_prods:
                fav.substitute_to.append(Product(prod))
            fav.subst_loaded = True

    def fetch_prod_from_fav_page(self, page):
        """Run fetch_prod_from_fav on a whole page of favorites.

        Args:
            page: The page to process.
        """

        for fav in self.subst_reg[page]:
            self.fetch_prod_from_fav(fav)

    def fetch_stores_from_fav(self, fav):
        """Fetches stores in database linked to a given favorite.

        Args:
            fav: The chosen favorite.
        """

        if not fav.stores_loaded:
            db_stores = self.dbs.get_stores_from_prod(fav.original_id)
            for store in db_stores:
                fav.stores_list.append(self.stores_list[store['id'] - 1])
            fav.stores_loaded = True

    def fetch_stores_from_product(self, product):
        """Fetches stores in database linked to a given product.

        Args:
            product: The chosen product.
        """

        if not product.stores_loaded:
            db_stores = self.dbs.get_stores_from_prod(product.id)
            for store in db_stores:
                product.stores_list.append(self.stores_list[store['id'] - 1])
                self.stores_list[store['id'] - 1].add_product(product)
            product.stores_loaded = True

    def fetch_brands_from_fav(self, fav):
        """Fetches brands in db linked to a given favorite.

        Args:
            fav: Favorite object, the chosen favorite.
        """

        if not fav.brands_loaded:
            db_brands = self.dbs.get_brands_from_prod(fav.original_id)
            for brand in db_brands:
                fav.brands_list.append(self.brands_list[brand['id'] - 1])
            fav.brands_loaded = True

    def fetch_brands_from_product(self, product):
        """Fetches brands for a given product

        Args:
            product: The given product.
        """

        if not product.brands_loaded:
            db_brands = self.dbs.get_brands_from_prod(product.id)
            for brand in db_brands:
                product.brands_list.append(self.brands_list[brand['id'] - 1])
                self.brands_list[brand['id'] - 1].add_product(product)
            product.brands_loaded = True

    def fetch_brands_from_product_page(self, page, category):
        """Fetches brands for all products in a page from a category.

        Args:
            page: int, The page to print.
            category: The category the products belong to.
        """

        category.buffer_check()
        for product in category.product_registry[page]:
            self.fetch_brands_from_product(product)

    def fetch_stores_from_subst(self, subst):
        """Fetches stores for a given substitute.

        Args:
            subst: The given substitute.
        """
        if not subst.stores_loaded:
            db_stores = self.dbs.get_stores_from_prod(subst.original_id)
            for store in db_stores:
                subst.stores_list.append(self.stores_list[store['id'] - 1])
                self.stores_list[store['id'] - 1].add_product(subst)
            subst.stores_loaded = True

    def fetch_brands_from_subst_page(self, page, product):
        """Fetches brands for all substitutes in a page.

        Args:
            page: int, The page to print.
            product: The product to be replaced.
        """

        product.buffer_check()
        for subst in product.substitute_registry[page]:
            if not subst.brands_loaded:
                db_brands = self.dbs.get_brands_from_prod(subst.original_id)
                for brand in db_brands:
                    subst.brands_list.append(self.brands_list[brand['id'] - 1])
                    self.brands_list[brand['id'] - 1].add_product(subst)
                subst.brands_loaded = True

    def get_substitutes_to_product(self, product):
        """Fetches substitutes to a product from db.

        The substitutes are added to the product substitutes list.

        Args:
            product: product object, the product for which substitutes
                are fetched.
        """

        # check if there is already data loaded in memory!
        results = self.dbs.get_substitutes_v2(product)
        for result in results:
            subst = Substitute(result, result['id'])
            cat = self.categories_list[product.categories_list[0].id - 1]
            og_prod = self.find_item_in_registry(subst.original_id,
                                                 misc.PAGE_SIZE,
                                                 cat.product_registry,
                                                 cat.product_page_buffer)
            if og_prod.brands_loaded:
                subst.brands_list = og_prod.brands_list
                subst.brands_loaded = True
            if og_prod.stores_loaded:
                subst.stores_list = og_prod.stores_list
                subst.stores_loaded = True
            product.add_substitute(subst)

    @staticmethod
    def find_item_in_registry(item_id, page_size, registry, buffer):
        """Finds an item in a registry.

        Args:
            item_id: int, The index of the item.
            page_size: int, the size of a page and of a filled-buffer.
            registry: list of list, The registry
            buffer: list, The buffer

        Returns: The found item.

        """

        page = (item_id - registry[0][0].id) // page_size
        i = (item_id - registry[0][0].id) % page_size
        if (item_id - registry[0][0].id) > len(registry) * page_size:
            return buffer[i - 1]
        return registry[page][i]

    def save_substitute_v2(self, substitute, product):
        """Saves a substitute to program memory and db.

        Checks if the substitute is already saved using
            saving_is_possible.

        Args:
            substitute: product object, the substitute to save.
            product: The product to be replaced.

        Returns:
            True: If the product has been saved.
            False: If the product has not been saved.

        """

        is_present, can_be_saved, elt = self.saving_is_possible_v2(substitute,
                                                                   product)
        breakpoint()
        if can_be_saved:
            if is_present:
                elt.substitute_to.append(product)
                elt.subst_loaded = True
                # modify substitute
                self.dbs.prod_fav_insertion(product.id, elt.id)
                return True
            elt.subst_loaded = True
            fav = Favorite(elt)
            fav.substitute_to.append(product)
            fav.id = self.last_saved_id + 1
            self.last_saved_id += 1
            self.add_substitute_to_saved_list(fav)
            self.dbs.save_to_db_v2(fav)
            self.dbs.prod_fav_insertion(product.id, fav.id)
            return True
        return False

    def saving_is_possible_v2(self, substitute, product):
        """Checks if a substitute to a product is already saved.

        A substitute can be saved several times if it is the substitute
            to different products.

        Args:
            substitute: product object, The substitute to check.
            product: product object, The product getting replaced.

        Returns:
            is_present: True if favorite is already present
            can_be_saved: True if favorite is not already present and
                not already linked to give product.
            fav: The favorite.

        """

        is_present = False
        can_be_saved = True
        fav = substitute
        for elt in self.saved_sub_buf:
            if substitute.original_id == elt.original_id:
                fav = elt
                is_present = True
                for subst_to in fav.substitute_to:
                    if product.id == subst_to.id:
                        can_be_saved = False
                        return is_present, can_be_saved, fav
        for page in self.subst_reg:
            for elt in page:
                if substitute.original_id == elt.original_id:
                    is_present = True
                    fav = elt
                    for subst_to in elt.substitute_to:
                        if product.id == subst_to.id:
                            can_be_saved = False
                            return is_present, can_be_saved, fav
        return is_present, can_be_saved, fav

    def del_all_in_fav(self, fav):
        """Deletes all "substitutes to of a favorite.

        Args:
            fav: The given favorite.
        """

        #for subst in fav.substitute_to:
        #    self.dbs.prod_fav_del(subst, fav)
        self.dbs.delete_saved_substitute(fav)
        fav.substitute_to = []
        self.delete_item_in_registry(fav, self.subst_reg,
                                     self.saved_sub_buf)
        input(f"{Fore.MAGENTA}Removed {fav.french_name} from favorites."
              f" {Style.RESET_ALL}Press enter to continue.")
        breakpoint()
        del fav

    def del_one_in_fav(self, fav, user_choice):
        """Deletes only one substitute of a favorite.

        Args:
            fav: The given favorite.
            user_choice: The chosen substitute to.
        """

        self.dbs.prod_fav_del(fav.substitute_to[user_choice - 1],
                              fav)
        deld = fav.substitute_to.pop(user_choice - 1)
        input(f"{Fore.MAGENTA}Removed {fav.french_name} as a substitute to"
              f" {deld.french_name}."
              f" {Style.RESET_ALL}Press enter to continue.")
        if len(fav.substitute_to) == 0:
            self.dbs.delete_saved_substitute(fav)
            fav.substitute_to = []
            self.delete_item_in_registry(fav,
                                         self.subst_reg,
                                         self.saved_sub_buf)
            del fav

    @staticmethod
    def delete_item_in_registry(item, registry, buffer):
        """Deletes and item in a registry.

        Args:
            item: The item to delete.
            registry: The registry to search in.
            buffer: The buffer to search in.
        """
        try:
            buffer.remove(item)
        except ValueError:
            for buf in registry:
                buf.remove(item)

    def clear_db(self):
        """Clears the whole database by using clear_table() method."""

        self.dbs.clear_table("categories", "products", "favorites")
        del self.subst_reg
        del self.saved_sub_buf
        del self.categories_list
        self.categories_list = []
        self.saved_sub_buf = []
        self.subst_reg = []
        self.last_saved_id = 0

    def clear_saved_substitutes(self):
        """Removes all substitutes from db and program memory."""

        self.dbs.clear_table("favorites", "product_favorites")
        del self.subst_reg
        del self.saved_sub_buf
        self.saved_sub_buf = []
        self.subst_reg = []
        self.last_saved_id = 0

    def update_db(self):
        """Clears then reload the database."""

        self.clear_db()
        self.fill_from_off()

    def fill_from_off(self):
        """Fills the program memory with data from openfoodfacts API."""

        self.fill_categories_from_off_v2()
        self.fill_products_from_off_v3()

    def fill_from_db(self):
        """Fills the program memory with data from the db."""

        self.fill_brands_from_db()
        self.fill_stores_from_db()
        self.fill_categories_from_db()
        self.fill_products_from_db()
        self.fill_saved_product_from_db_v2()
