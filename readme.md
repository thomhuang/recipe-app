# **How to use our webscraper**

1. Download the scraper folder from this repositiory

2. Open Terminal/Command Line and change directory to the scraper folder by typing `cd /address_of_folder` in the Terminal

3. Type `conda activate base` in order to enable the base Python environment in `Anaconda` 

    (Note: You may need to download `Anaconda` if your do not have it). 

4. Type `pip install Scrapy` to install the `Scrapy` package. 

    Type `Scrapy -v` to check for correct installation.

5. To activate the scraper and get the data in CSV format in a file called my_file.csv, type:

    `scrapy crawl ultra -o my_file.csv`

    where `ultra` is the name of the scraper we need to run. 

# **How to use our application**

To run the application, if you don't have it installed, please install the `PyQt5` package in your environment. Then, place the `recipe_app_gui.py` file in the `src\app GUI` folder as well as the `recipes.db` file in the `data` folder in your desired location. Once done, go into your terminal, path to the location you placed both files in and enter `python3 recipe_app_gui.py`. This should display the application.

If you would like the general idea of what we aim to do with our application, please refer to the `proposal.md` file. Our application contains a number of recipes and its information to be searched for by the user. In particular, there are three aspects to our user interface:

1. Search window
2. Recipe list window
3. Recipe information window

How each are supposed to be used will be described in their own sections.

## **Search Window**

There are 4 main aspects to this window.

1. **`Help` menu button**

Pressing this will provide a drop-down menu with two options, namely `Search` and `View`.

`Search` gives a pop-up message giving information on how you should input your desired search if there are multiple items.

`View` gives a pop-up message giving information on how you should view your desired recipe in the Recipe list window.

1. **The combobox**

Defaulted to `Recipe Title`, if the user clicks on this box they will be met by a dropdown menu with four other options, namely: `Author`, `Cuisine`, `Ingredients`, and `Tags`. Selecting one of these will search under those specific categories between the recipes.

1. **The text edit**

This is where the user will type in their desired query.

For example:

* if you choose `Author` and search `J. Kenji López-Alt`, you will be provided all the recipes written by J. Kenji López-Alt.
* if you choose `Cuisine` and search `African`, you will be provided all recipes deemed by SeriousEats to be African cuisine
* If you choose `Ingredients` and search `chicken,garlic,ginger`, you will be provided all recipes that contain chicken, garlic, and ginger

And so on.

1. **The `Search Recipes` button**

Once the user has input their desired query, they should press this button to see the recipes.

If the text edit is empty or there are no recipes associated with the query, there will be an error message that pops up.

## **Recipe List Window**

Once the users have successfully searched for their recipes, this table-view window will show up with the search window still available in the background.

With the list of recipes shown, if the user double clicks on the desired recipe cell, it will open up the Recipe Information Window

## **Recipe Information Window**

Once the user has successfully double clicked on their desired recipe, all the information pertaining to the recipe will show.

In particular, it will show:

* Author name
* Cuisine category
* Tags
* Ingredient list
* Recipe procedure
* Website hyperlink
* Table containing similar recipes

The table containing similar recipes has the same functionality as the Recipe List Window.
