"""Contains the class DBSocket"""

import pymysql
from config import sql_queries as sql
from config import database_connection as db_info
from config import colorama_cfg as color


class DBSocket:
    """Class representing a software component managing database.

    This class handles all operations related to database be it
        connections or queries.
    This class interacts with a mariadb/mysql database. All connection
        information can be found in the database config file inside the
        config folder.
    Class leverages pymysql library for handling SQL queries and
        database connection. Refer to pymysql documentation for further
        information.
    All queries are defined in the SQL Query file inside the config
        folder

    Attributes:
        connection: A pymysql connection object. Represents a socket
            with a mysql/mariadb server. Establishes connection with the
            database.
        cursor: A pymysql cursor object. This is the object used to
            interact with the database.
        db_is_empty: Boolean True if db is empty False otherwise.

    """

    def __init__(self, script):
        """Inits an instance of DBSocket.

        A check is made to verify prior existence to a database and if
            connection to it can be established otherwise database is
            created.
        An SQL script is run to create desired database architecture.
            The script can be found in the config folder.

        Args:
            script: SQL script containing the database architecture.
        """

        create_db = bool()
        self.connection, create_db = self.check_db()
        self.cursor = self.connection.cursor()
        if create_db:
            self.setup_db(script)
            self.db_is_empty = True
        else:
            self.check_if_db_is_empty()

    @staticmethod
    def check_db():
        """Checks whether a database exists if not, creates it.

        Connection information can be found in config folder.

        Returns:
            connection: a pymysql connection object.

        Raises:
            pymysql.err.OperationalError: Connection to a database
                could not be established.

        """

        print("Checking for pre existing database....")
        try:
            connection = pymysql.connect(
                host=db_info.mariadb['host'],
                user=db_info.mariadb['user'],
                password=db_info.mariadb['password'],
                db=db_info.mariadb['db'],
                charset=db_info.mariadb['charset'],
                cursorclass=db_info.mariadb['cursorclass'])
            print("Database detected and connection successful.")
            create_db = False
            input("Press enter key...")
        except pymysql.err.OperationalError:
            print("No database detected.")
            connection = pymysql.connect(
                host=db_info.mariadb['host'],
                user=db_info.mariadb['user'],
                password=db_info.mariadb['password'],
                charset=db_info.mariadb['charset'],
                cursorclass=db_info.mariadb['cursorclass'])
            create_db = True
            input("Press enter key...")
        return connection, create_db

    def check_if_db_is_empty(self):
        """Returns a boolean telling if database is empty or not."""
        cat = self.get_categories()
        if not cat:
            self.db_is_empty = True
        else:
            self.db_is_empty = False

    def setup_db(self, script):
        """Sets the database up by running an SQL script.

        Args:
            script: The SQL script to be run.
        """

        print("Creating a new database \"p5_openfoodfacts\"")
        # Execute sql script
        statement = ""
        with open(script, 'r', encoding="utf-8") as sql_script:
            for line in sql_script:
                if line.strip().startswith('--'):  # ignore sql comment lines
                    continue
                if not line.strip().endswith(
                        ';'):  # keep appending lines that don't end in ';'
                    statement = statement + line
                else:  # line ending in ';' > exec statement and reset for next
                    statement = statement + line
                    self.cursor.execute(statement)
                    statement = ""

    def cat_insertion_v2(self, category):
        """inserts data in table category.

        Args:
            category: The category to insert.
        """

        self.cursor.execute(sql.INS_CAT,
                            (category.french_name,
                             category.url))
        self.connection.commit()

    def product_insertion_v2(self, product):
        """Inserts a specified product into table products.

        The method ignores product with names containing unsupported
            chars or missing keys.

        Args:
            product: The product object to insert.

        Raises:
            KeyError: Some required fields are not in the product
                pulled from OpenFoodFacts.
            pymysql.err.DataError: Input from the API could not be
                processed.

        Returns:
            Bool: True if insertion successful, false otherwise.
        """

        try:
            self.cursor.execute(
                sql.INS_PROD,
                (product.french_name, product.url, product.nutrition_grades))
            return True
        except pymysql.err.DataError:
            return False
        except KeyError:
            return False

    def cat_prod_insertion(self, category, product):
        """Insert a link between a category and a product in db.

        Args:
            category: The category to insert.
            product: The product to insert.
        """

        self.cursor.execute(sql.INS_CAT_PROD, (category.id, product.id))

    def prod_stores_insertion(self, product, store):
        """Insert a link between a store and a product in db.

        Args:
            store: The store to insert.
            product: The product to insert.
        """

        self.cursor.execute(sql.INS_PROD_STORES, (product.id, store.id))

    def prod_fav_insertion(self, product_id, favorite_id):
        """Insert a link between a favorite and a product in db.

        Args:
            favorite_id: The favorite to insert.
            product_id: The product to insert.
        """

        try:
            self.cursor.execute(sql.INS_PROD_FAV, (product_id, favorite_id))
        except pymysql.err.IntegrityError as error:
            print("Fatal error. Check query using cursor._last_executed.")
            print(error)
        self.connection.commit()

    def prod_fav_del(self, product, fav):
        """Deletes an entry in the products_favorite table."""

        self.cursor.execute(sql.DEL_PROD_FAV, (product.id, fav.id))
        self.connection.commit()

    def prod_brands_insertion(self, product, brand):
        """Insert a link between a brand and a product in db.

        Args:
            brand: The brand to insert.
            product: The product to insert.
        """
        self.cursor.execute(sql.INS_PROD_BRANDS, (product.id, brand.id))

    def store_insertion(self, store):
        """Adds a store to the database."""

        try:
            self.cursor.execute(sql.INS_STORE, (store.name, store.url))
            return True
        except pymysql.err.DataError:
            self.cursor.execute(sql.INS_STORE, ("n/a", "n/a"))
            return False

    def brand_insertion(self, brand):
        """Adds a brand to the database."""

        try:
            self.cursor.execute(sql.INS_BRAND, (brand.name, brand.url))
            return True
        except pymysql.err.DataError:
            self.cursor.execute(sql.INS_BRAND, ("n/a", "n/a"))
            return False

    def get_max_id_from_fav(self):
        """Returns the maximum id from the favorites table"""

        self.cursor.execute(sql.QUERY_MAX)
        return self.cursor.fetchall()

    def clear_table(self, *table):
        """Clears specific tables.

        Args:
            *table: list of tables to clear.
        """

        i = 0
        while i < len(table):
            print(f"{color.minus_prfx} Deleting {table[i]}")
            self.cursor.execute(sql.EMPTY_TABLE.format(table[i]))
            self.cursor.execute(sql.RST_INDEX.format(table[i]))
            i += 1
        self.connection.commit()

    def get_categories(self):
        """Returns all categories from the program database."""

        self.cursor.execute(sql.GET_CAT)
        return self.cursor.fetchall()

    def get_brands_from_prod(self, product_id):
        """Returns all products from a specified category.

        Args:
            category: the category user wants the product from.

        Returns:
            self.cursor.fetchall(): list containing products.
        """

        self.cursor.execute(sql.QUERY_BRAND_FROM_PROD, product_id)
        return self.cursor.fetchall()

    def get_stores_from_prod(self, product_id):
        """Returns all products from a specified category.

        Args:
            category: the category user wants the product from.

        Returns:
            self.cursor.fetchall(): list containing products.
        """

        self.cursor.execute(sql.QUERY_STORE_FROM_PROD, product_id)
        return self.cursor.fetchall()

    def get_products_from_cat(self, category):
        """Returns all products from a specified category.

        Args:
            category: the category user wants the product from.

        Returns:
            self.cursor.fetchall(): list containing products.
        """

        self.cursor.execute(sql.QUERY_PROD_FROM_CAT, category.french_name)
        return self.cursor.fetchall()

    def get_prod_from_fav(self, favorite_id):
        """Returns products linked to a favorite."""

        self.cursor.execute(sql.QUERY_PROD_FROM_FAV, favorite_id)
        return self.cursor.fetchall()

    def get_saved_products_v2(self):
        """Returns all products previously saved by user in database."""

        self.cursor.execute(sql.GET_SAVED)
        return self.cursor.fetchall()

    def get_brands(self):
        """Returns all products previously saved by user in database."""

        self.cursor.execute(sql.QUERY_BRAND)
        return self.cursor.fetchall()

    def get_stores(self):
        """Returns all products previously saved by user in database."""

        self.cursor.execute(sql.QUERY_STORE)
        return self.cursor.fetchall()

    def get_saved_products(self):
        """Returns all products previously saved by user in database."""

        self.cursor.execute(sql.GET_SAVED)
        return self.cursor.fetchall()

    def get_substitutes_v2(self, product):
        """Returns all substitutes of a specified product.

        Args:
            product: the product which user wants substitutes from.

        Returns:
            self.cursor.fetchall(): list containing products.

        """

        self.cursor.execute(sql.FIND_SUBST,
                            (product.categories_list[0].id,
                             product.nutrition_grades, product.french_name))
        return self.cursor.fetchall()

    def delete_saved_substitute(self, subst):
        """Deletes a product from the saved_products table.

        Args:
            subst: The product to delete.
        """

        # Match in the database is made using the original id.
        self.cursor.execute(sql.DEL_SAVED.format(subst.original_id))
        self.connection.commit()

    def save_to_db_v2(self, subst):
        """Inserts a subst into the saved_products table.

        Args:
            subst: The subst to save to the database.
        """
        try:
            self.cursor.execute(sql.INS_SAVED.format(subst.original_id,
                                                     subst.french_name,
                                                     subst.url,
                                                     subst.nutrition_grades,
                                                     ))
        except:
            print("Insertion error. Check cursor._last_executed.")
        self.connection.commit()
