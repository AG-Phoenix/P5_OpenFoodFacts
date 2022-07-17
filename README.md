# OpenFoodFacts

This terminal app allows users to find healthier substitutes to food.
Comparision between products is made based on their nutrition grades.
Nutrition Data is pulled from the [OpenFoodFacts Database](https://world.openfoodfacts.org/).

# Prerequisites

* python3
* python virtual env
* pip
* a working and running mariadb or mysql server

# Setup

Change database creds in the config/database_connection.py file according to your needs.
Change database name accordingly in the db creation script as well.

```bash
# Clone this git repo
git clone https://git.tohunga.me/ax/P5-Open-Food-Facts
cd P5-Open-Food-Facts

# Setup a python virtual environment and activate it.
python3 -m venv env
source /env/bin/activage

# Install required libs
pip install -r requirements.txt 
```

# Usage

```bash
python3 app.py
```
