"""API Downloads

This file contains variables for interacting with the OpenFoodFacts API.
"""

off_categories = {}
PAGE_SIZE = 500

off_urls = {
    'categories':
    'https://fr.openfoodfacts.org/categories.json',
    'products':
    'https://fr.openfoodfacts.org/cgi/search.pl?action=process&tagtype_0='
    'countries&tag_contains_0=contains&tag_0=fr&page_size=1000&page={}&json=1'
    '&fields=brands,nutrition_grades,product_name_fr,stores,url',
    'cat_aliment_boisson_vege':
    'https://fr.openfoodfacts.org/categorie/'
    'aliments-et-boissons-a-base-de-vegetaux.json&page_size=5000'
}

PROD_FIELDS = 'brands,nutrition_grades,product_name_fr,stores,url'
STORE_URL = "https://world.openfoodfacts.org/store/"
BRAND_URL = "https://world.openfoodfacts.org/brand/"

BASE_CAT_URL = "https://fr.openfoodfacts.org/categorie/"

CAT_ENDPOINT = [
    "biscuits", "viandes-fraiches", "cremes-dessert", "yaourts",
    "barres-de-cereales", "boissons-energisantes",
    "sodas", "charcuteries", "cereales pour petit-dejeuner", "jus-de-fruits"
]
