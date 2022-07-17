"""SQL Queries"""

EMPTY_TABLE = 'DELETE FROM {}'
RST_INDEX = 'ALTER TABLE {} AUTO_INCREMENT = 1'

INS_BRAND = 'INSERT INTO brands(name, url) \
    VALUES (%s, %s)'

INS_STORE = 'INSERT INTO stores(name, url) \
    VALUES (%s, %s)'

INS_CAT = 'INSERT INTO categories(name, url) \
    VALUES (%s, %s)'

INS_PROD = 'INSERT INTO products(french_name, url, nutrition_grades) \
    VALUES (%s, %s, %s)'

INS_CAT_PROD = 'INSERT INTO category_products(category_id, product_id)' \
               'VALUES (%s, %s)'

INS_PROD_FAV = 'INSERT INTO product_favorites(product_id, favorite_id)' \
               'VALUES (%s, %s)'

INS_PROD_BRANDS = 'INSERT INTO product_brands(product_id, brand_id)' \
               'VALUES (%s, %s)'

INS_PROD_STORES = 'INSERT INTO product_stores(product_id, store_id)' \
               'VALUES (%s, %s)'

GET_CAT = 'SELECT * FROM categories;'

INS_SAVED = 'INSERT INTO favorites (original_id, french_name, \
                   url, nutrition_grades) \
    SELECT {0}, "{1}", "{2}", "{3}" '

GET_PROD_BY_ID = 'SELECT * FROM products WHERE id = {}'

GET_SAVED = "SELECT * from favorites;"

DEL_SAVED = " DELETE FROM favorites WHERE original_id = {};"

FIND_SUBST = "SELECT * FROM products " \
             "RIGHT JOIN category_products " \
             "ON products.id = category_products.product_id " \
             "LEFT JOIN categories " \
             "ON category_products.category_id = categories.id " \
             "WHERE categories.id = %s " \
             "AND LOWER(nutrition_grades) <= %s" \
             "AND NOT products.french_name = %s;"

QUERY_PROD_FROM_CAT = "SELECT * FROM products " \
                      "RIGHT JOIN category_products " \
                      "ON products.id = category_products.product_id " \
                      "LEFT JOIN categories " \
                      "ON category_products.category_id = categories.id " \
                      "WHERE categories.name = %s; " \

QUERY_PROD_FROM_FAV = "SELECT * FROM products " \
                        "LEFT JOIN product_favorites " \
                        "ON products.id = product_favorites.product_id " \
                        "RIGHT JOIN favorites " \
                        "ON product_favorites.favorite_id = favorites.id " \
                        "WHERE favorites.id = %s; " \

QUERY_BRAND_FROM_PROD = "SELECT * FROM brands " \
                        "RIGHT JOIN product_brands " \
                        "ON brands.id = product_brands.brand_id " \
                        "LEFT JOIN products " \
                        "ON product_brands.product_id = products.id " \
                        "WHERE products.id = %s; " \

QUERY_STORE_FROM_PROD = "SELECT * FROM stores " \
                        "RIGHT JOIN product_stores " \
                        "ON stores.id = product_stores.store_id " \
                        "LEFT JOIN products " \
                        "ON product_stores.product_id = products.id " \
                        "WHERE products.id = %s " \

QUERY_BRAND = "SELECT * FROM brands;"

QUERY_STORE = "SELECT * FROM stores;"

QUERY_MAX = "SELECT MAX( id ) FROM favorites;"

DEL_PROD_FAV = "DELETE FROM product_favorites " \
               "WHERE product_id = %s " \
               "AND favorite_id = %s;"
