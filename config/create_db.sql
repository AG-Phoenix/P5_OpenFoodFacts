CREATE DATABASE IF NOT EXISTS changeme;
USE changeme;

-- Table categories : categories pulled from OFF
CREATE TABLE IF NOT EXISTS categories (
    id int UNSIGNED NOT NULL AUTO_INCREMENT,
    name varchar(500) NULL,
    url varchar(500) NULL,
    CONSTRAINT id PRIMARY KEY (id)
);

-- Table products : relevant data for products pulled from OFF
CREATE TABLE IF NOT EXISTS products (
    id int UNSIGNED NOT NULL AUTO_INCREMENT,
    french_name varchar(500) NULL,
    url varchar(500) NULL,
    nutrition_grades char(1) NULL,
    CONSTRAINT id PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS category_products (
    category_id int UNSIGNED NOT NULL,
    product_id int UNSIGNED NOT NULL,
    CONSTRAINT fk_cp_category_id FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE,
    CONSTRAINT fk_cp_product_id FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- Table saved_products: all products saved by the user
CREATE TABLE IF NOT EXISTS favorites (
    id int UNSIGNED NOT NULL AUTO_INCREMENT,
    original_id int UNSIGNED NOT NULL,
    french_name varchar(500) NULL,
    url varchar(500) NULL,
    nutrition_grades char(1) NULL,
    CONSTRAINT id PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS product_favorites (
    product_id int UNSIGNED NOT NULL,
    favorite_id int UNSIGNED NOT NULL,
    CONSTRAINT fk_pf_product_id FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    CONSTRAINT fk_pf_favorite_id FOREIGN KEY (favorite_id) REFERENCES favorites(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS brands (
    id int UNSIGNED NOT NULL AUTO_INCREMENT,
    name varchar(500) NULL,
    url varchar(500) NULL,
    CONSTRAINT id PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS stores (
    id int UNSIGNED NOT NULL AUTO_INCREMENT,
    name varchar(500) NULL,
    url varchar(500) NULL,
    CONSTRAINT id PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS product_stores (
    product_id int UNSIGNED NOT NULL,
    store_id int UNSIGNED NOT NULL,
    CONSTRAINT fk_ps_product_id FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    CONSTRAINT fk_ps_stores_id FOREIGN KEY (store_id) REFERENCES stores(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS product_brands (
    product_id int UNSIGNED NOT NULL,
    brand_id int UNSIGNED NOT NULL,
    CONSTRAINT fk_pb_product_id FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    CONSTRAINT fk_pb_brand_id FOREIGN KEY (brand_id) REFERENCES brands(id) ON DELETE CASCADE
);
