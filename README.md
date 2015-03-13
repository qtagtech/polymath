# polymath
Python implementation for getting a list of categories from eBay
Usage: python getCategories.py [options]
Options:
-r ..., --render=... Render specifi category from the API
-R, --rebuild Update local SQLite3 Database fetching all values from the API
-h, --help show this help info
Examples:
getCategories.py generates a "no arguments exception".
getCategories.py -r 14567 generates an html file called 14567.html with the category information from ebay.
getCategories.py --rebuild calls the ebay getCategory API and updates the local database with the values fetched.
getCategories.py -h shows this help info
Database Structure
Category Category Relationships
________________ __________________________
id INT category_id INT (foreignkey references Category.id)
name VARCHAR child_id INT (foreignkey references Category.id)
level INT
BestOfferEnabled BOOLEAN
The Tree Structure looks like this:
cat1
/ | \\
cat2__cat3 cat4
| \\ |
cat5 cat6
Calls to the eBay API are optimized by first retrieving level=1 categories and saving it to the local db if it doesn't exist
Then, for each category of level=1 a request to the API is made to fetch all children categories from level=[2..6], and every time
a children is fetched, which at the same time is a category, is saved in the local db as long as it doesn't exist yet.
Like this, every time a categroy is iterated, less categories will be saved in the database but the relationships will be still recorded.
This program is developed for Polymath Ventures LLC as part of the Polymath Challenge.
Developed by Juan David Arroyave using python3.
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
::::::::::::::::::: Juan David Arroyave :::::::::::::::::::
::::::::::::: http://www.juandavidarroyave.com ::::::::::::
::::::::::::::::: me@juandavidarroyave.com ::::::::::::::::
::::::::::::::::::::::::::: 2015 ::::::::::::::::::::::::::
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
"""
__author__ = "Juan David Arroyave (me@juandavidarroyave.com)"
__version__ = "$Revision: 0.1 $"
__date__ = "$Date: 2015/07/03 20:03:30 $"
__copyright__ = "Copyright (c) 2015 Juan David Arroyave"
__license__ = "Python"
