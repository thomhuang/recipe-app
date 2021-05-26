from PyQt5.QtSql import (QSqlDatabase, QSqlQuery, QSqlQueryModel)
from PyQt5.QtWidgets import (QWidget, QApplication, QMenuBar, QLabel, QComboBox,QLineEdit, QTextEdit, QPushButton,
                             QMessageBox, QErrorMessage, QTableView)
from PyQt5.QtCore import (Qt)
from PyQt5.QtGui import (QFont)

class SearchWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.title_window = RecipeTitleWindow()
        self.initUI()  # Initialize our UI elements

    def initUI(self):
        """
        PURPOSE
        -----
        This function works to create and place all necessary elements for the Search Window onto our 'QWidget'

        We have a ...
        - menu-bar 'help_menu' to give instructions on how to query for recipes (search_help)
        and how to view recipes once queried (view_help)
        - combobox 'search_combobox' containing the various categories that you could query under
        - Text edit 'search_text_edit' to allow users to type their query
        - Button 'search_button' for when they want to finally search

        OUTPUT
        -----
        No return, but displays our window
        """

        self.setWindowTitle("Recipe Application")
        # Set geometry + fix size
        self.setGeometry(0, 0, 500, 140)
        self.setFixedSize(self.width(), self.height())

        # Add menu widgets
        menu_bar = QMenuBar(self)
        help_menu = menu_bar.addMenu("Help")
        search_help = help_menu.addAction("Search")
        view_help = help_menu.addAction("View")

        # Add label
        instruction_label = QLabel("Please input each search item separated by a comma!", self)  # Instruction label
        instruction_label.move(120, 20)

        # Add combobox + info within combobox
        self.search_combobox = QComboBox(self)
        self.search_combobox.addItem("Recipe Title")
        self.search_combobox.addItem("Author")
        self.search_combobox.addItem("Cuisine")
        self.search_combobox.addItem("Ingredients")
        self.search_combobox.addItem("Tags")
        self.search_combobox.move(50, 60)

        # Add text edit
        self.search_text_edit = QLineEdit(self)  # Text box to insert ingredients-to-be-queried
        self.search_text_edit.move(150, 50)
        self.search_text_edit.resize(300, 40)

        # Add button to search
        search_button = QPushButton('Search Recipes', self)  # Button to search for recipes
        search_button.move(200, 100)

        # Add functionality to desired widgets
        search_button.clicked.connect(self.pass_info)  # Connect button to function to query
        search_help.triggered.connect(self.searchHelpPopup)
        view_help.triggered.connect(self.viewHelpPopup)

        self.show()

    def searchHelpPopup(self):
        """
        PURPOSE
        -----
        Displays a pop-up to instruct users how to query for ingredients

        OUTPUT
        -----
        displays a popout with message
        """

        help_dialog = QMessageBox() # Create message box
        help_dialog.setText( # Set text of message box
            "Please choose the desired category and input what you want to search for separated by commas, such as: " +
            "\n\n" + "item1,item2,item3,item4,..." + "\n")
        help_dialog.setStandardButtons(QMessageBox.Ok) # Add okay button
        help_dialog.setWindowTitle("How to search for recipes!") # Window title
        help_dialog.exec_() # Show box

    def viewHelpPopup(self):
        """
        PURPOSE
        -----
        Displays a pop-up to instruct users how to view recipes from recipe table

        OUTPUT
        -----
        displays a popout with message
        """
        # Same idea as above
        help_dialog = QMessageBox()
        help_dialog.setText("Double-click on the desired recipe title and it will view all the recipe information!")
        help_dialog.setStandardButtons(QMessageBox.Ok)
        help_dialog.setWindowTitle("How to view recipes!")
        help_dialog.exec_()

    def pass_info(self):
        """
        PURPOSE
        -----
        To pass user information to query in next window, 'RecipeTitleWindow'

        OUTPUT
        -----
        calls function within RecipeTitleWindow object we create in __init()__

        """
        self.title_window.search_category = str(self.search_combobox.currentText()) # Get category from combobox

        self.title_window.search_text = self.search_text_edit.text() # Get text from text edit

        self.title_window.recipe_search()

class RecipeTitleWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.search_text = ""
        self.search_category = ""

        self.recipe_window = RecipeWindow()

        # Create connection with SQlite3 language
        self.conn = QSqlDatabase.addDatabase("QSQLITE")
        self.conn.setDatabaseName("recipes.db")

    def recipe_search(self):
        """
        PURPOSE
        -----
        To search and display the recipes from the desired query from the user using sqlite3 on a table-view

        OUTPUT
        -----
        Displays a table of rows containing recipe titles that the user can double click on to view information about it

        """
        self.conn.open() # Open our connection to database
        self.setWindowTitle("Recipe Application")

        if len(self.search_text.strip(' ')) == 0: # If the query is empty, throw an error message
            error_dialog = QErrorMessage()
            error_dialog.showMessage(
                f"It seems you haven't input anything to search for the {self.search_category.lower()}'s associated recipes! Please try again.")
            error_dialog.exec_()
        else: # Otherwise we proceed as normally

            self.search_list = self.search_text.split(',')  # Create an array of desired ingredients

            recipe_query = ""  # Empty string to construct our query
            for elements in self.search_list:
                # Here we construct our query through a for-loop
                # There shouldn't be many elements in our array in the first place, so no worries of efficiency
                recipe_query += f"`{self.search_category}` LIKE '%" + elements + "%' AND "

            if len(recipe_query) > 5:  # On the off chance that there is nothing input into the text box, throw error
                recipe_query = recipe_query[:len(recipe_query) - 5]  # to remove last AND

            cmd = \
                f"""
                SELECT `Recipe Title` FROM recipes R WHERE {recipe_query}
                """

            title_query = QSqlQuery(self.conn)  # Establish our query, prepare, and execute it
            title_query.prepare(cmd)
            title_query.exec_()

            title_model = QSqlQueryModel()  # Adds our queried information into a read-only model
            title_model.setQuery(title_query)

            if title_model.rowCount() == 0: # If no recipes return, throw error message saying there exists no recipe
                                            # with their desired information
                empty_error_dialog = QErrorMessage()
                empty_error_dialog.showMessage(
                    f"It appears that there are no recipes pertaining to your search. Please try again!")
                empty_error_dialog.exec_()
            else:
                title_view = QTableView(self)  # Adds information from out query model to a QTableView to be seen
                title_view.setModel(title_model)
                title_view.setWindowTitle("Recipe List")

                title_view.doubleClicked.connect(lambda: self.pass_info(title_view.selectionModel().currentIndex()))
                # Adds functionality of view_recipe when double clicking cell

                title_view.setMaximumHeight(500) # Set max height of table + window
                self.setMaximumHeight(500)

                title_view.resizeColumnToContents(0) # Sets size of column to contents, i.e. longest recipe title

                # Each cell is ~ 30 pixels, so we make our window slightly smaller than the rows can fit if it
                # is less than 16 cells (which populates ~ 500 pixel height) to keep width consistent w/ scroll bar
                # and to make sure we have no empty space in our window
                title_view.resize(title_view.columnWidth(0) + 40, 25*title_model.rowCount())
                self.resize(title_view.columnWidth(0) + 40, 25*title_model.rowCount())

                self.show()

    def pass_info(self, index):  # Get current indexed position from click
        """
        PURPOSE
        -----
        To pass recipe information in next window, 'RecipeWindow'

        INPUT
        -----
        index: The index of the row+col selected by the user when they double click the recipe view

        OUTPUT
        -----
        calls function within RecipeWindow object we create in __init()__
        """

        cell_val = index.sibling(index.row(), index.column()).data()  # Get cell value from the cell itself
        self.recipe_window.recipe_title = cell_val # Sets information in RecipeWindow object

        self.hide() # Hides our current window
        self.recipe_window.view_recipe(self.recipe_window.obtain_recipe())


class RecipeWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.recipe_title = ""

        self.conn = QSqlDatabase.addDatabase("QSQLITE")
        self.conn.setDatabaseName("recipes.db")

        self.initUI()

    def initUI(self):
        """
        PURPOSE
        -----
        To pass create all QWidgets to be displayed on our window.
        All class instances are changed dynamically, i.e. title, author, etc.
        All non-class instances are static widgets that will not be moved

        OUTPUT
        -----
        Nothing
        """
        self.setWindowTitle("Recipe Application")

        self.title = QLabel(self)
        self.title.setWordWrap(True)  # Enables word wrap for specific label
        self.title.setFont(QFont('Arial', 20, QFont.Bold))
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setFixedWidth(600)
        self.title.move(150, 10)

        author_label = QLabel("Author: ", self)
        author_label.move(45, 120)
        author_label.setFont(QFont('Arial', 10, QFont.Bold))

        self.author = QLabel(self)
        self.author.move(95, 120)
        self.author.setFixedWidth(165)
        self.author.setFont(QFont('Arial', 10))

        cuisine_label = QLabel("Cuisine: ", self)
        cuisine_label.move(265, 120)
        cuisine_label.setFont(QFont('Arial', 10, QFont.Bold))

        self.cuisine = QLabel(self)
        self.cuisine.move(320, 120)
        self.cuisine.setFixedWidth(160)
        self.cuisine.setFont(QFont('Arial', 10))

        tag_label = QLabel("Tags: ", self)
        tag_label.move(485, 120)
        tag_label.setFont(QFont('Arial', 10, QFont.Bold))

        self.tags = QLabel(self)
        self.tags.setFixedWidth(330)
        self.tags.setWordWrap(True)
        self.tags.move(525, 115)
        self.tags.setFont(QFont('Arial', 10))

        ingredients_label = QLabel("Ingredients: ", self)
        ingredients_label.setFont(QFont('Arial', 10, QFont.Bold))
        ingredients_label.move(45, 170)

        self.ingredients = QTextEdit(self)
        self.ingredients.setReadOnly(True)
        self.ingredients.setFixedWidth(200)
        self.ingredients.setFixedHeight(300)
        self.ingredients.move(30, 200)
        self.ingredients.setFont(QFont('Arial', 10))

        recipe_label = QLabel("Recipe Procedure: ", self)
        recipe_label.setFont(QFont('Arial', 10, QFont.Bold))
        recipe_label.move(265, 170)

        self.recipe = QTextEdit(self)
        self.recipe.setReadOnly(True)
        self.recipe.setFixedWidth(610)
        self.recipe.setFixedHeight(300)
        self.recipe.move(250, 200)
        self.recipe.setFont(QFont('Arial', 10))

        website_url_label = QLabel("If you'd like to see full details of this recipe click here: ", self)
        website_url_label.setFont(QFont('Arial', 10, QFont.Bold))
        website_url_label.move(35, 540)

        self.website_url = QLabel(self)
        self.website_url.setOpenExternalLinks(True)  # Allows us to click on hyperlink
        self.website_url.setFixedWidth(500)
        self.website_url.setWordWrap(True)  # Set word wrap
        self.website_url.move(385, 540)
        self.website_url.setFont(QFont('Arial', 10))

        self.title_view_label = QLabel("Below are potentially some related recipes! :", self)
        self.title_view_label.setFont(QFont('Arial', 10))

    def obtain_recipe(self):
        """
        PURPOSE
        -----
        To obtain all information pertaining to the recipe clicked on by user, i.e. title, author, cuisine, etc. and
        create a model to store that information

        OUTPUT
        -----
        The model with the stored information
        """
        recipe_info_cmd = \
            f"""
        SELECT R.`Recipe Title`, R.Author, R.Cuisine, R.Ingredients, R.`Recipe Procedure`, R.Tags, R.'Website URL'
        FROM recipes R
        WHERE R.`Recipe Title` = "{self.recipe_title}"
        """
        # Query to get title, author, ingredients, and recipe procedure from desired recipe title
        recipe_query = QSqlQuery(self.conn)  # Same process as the title_query
        recipe_query.prepare(recipe_info_cmd)
        recipe_query.exec_()

        recipe_model = QSqlQueryModel()
        recipe_model.setQuery(recipe_query)

        return recipe_model

    def view_recipe(self, model):
        """
        PURPOSE
        -----
        To obtain all information pertaining to the recipe clicked on by user, i.e. title, author, cuisine, etc. from
        the model parameter and set the information to our widgets create in the initUI() function declared previously

        Then takes the tags from said recipe to view other recipes with one of its tags in view_related_recipes()

        INPUT
        -----
        model: QSqlQueryModel() containing recipe information

        OUTPUT
        -----
        Calls view_related_recipes() with array of tag values
        """

        # All values taken from QSqlQuery returned in obtain_recipe() function
        recipe_title = model.record(0).value(0)  # Recipe title
        recipe_author = model.record(0).value(1)  # Recipe author
        recipe_cuisine = model.record(0).value(2)  # Recipe cuisine
        recipe_ingredients = model.record(0).value(3)  # Recipe ingredients
        recipe_steps = model.record(0).value(4)  # Recipe steps
        recipe_tags = model.record(0).value(5)  # Recipe tags
        recipe_website = model.record(0).value(6)  # Recipe website

        self.setGeometry(0, 0, 900, 780)  # Set our window size
        self.setFixedSize(self.width(), self.height())

        # Everything done below is pretty self explanatory; create label/textedit, populate, move, etc.
        self.title.setText(recipe_title)
        self.title.repaint()

        self.author.setText(recipe_author)
        self.author.repaint()

        self.cuisine.setText(recipe_cuisine)
        self.cuisine.repaint()

        self.tags.setText(recipe_tags)
        self.tags.repaint()

        self.ingredients.setText(recipe_ingredients)
        self.ingredients.repaint()

        self.recipe.setText(recipe_steps)
        self.recipe.repaint()

        self.website_url.setText('<a href="' + recipe_website + '/">' + recipe_title + '</a>')  # Creates hyperlink
        self.website_url.repaint()

        self.view_related_recipes(recipe_tags.split(","))

    def view_related_recipes(self, tag_list):
        """
        PURPOSE
        -----
        To create a QTableView() with all recipes with like-tags of the already shown recipe

        INPUT
        -----
        tag_list: list containing tag information

        OUTPUT
        -----
        Displays full window containing recipe information + related recipes
        """

        recipe_query = ""  # Empty string to construct our query
        for elements in tag_list:
            # Here we construct our query through a for-loop
            # There shouldn't be many elements in our array in the first place, so no worries of efficiency
            recipe_query += f"Tags LIKE '%" + elements + "%' OR "

        recipe_query = recipe_query[:len(recipe_query) - 4]  # to remove last OR + extra space

        cmd = \
            f"""
            SELECT `Recipe Title` FROM recipes R WHERE {recipe_query}
            """
        title_query = QSqlQuery(self.conn)  # Establish our query, prepare, and execute it
        title_query.prepare(cmd)
        title_query.exec_()

        title_model = QSqlQueryModel()  # Adds our queried information into a read-only model
        title_model.setQuery(title_query)

        # Adds information from out query model to a QTableView to be seen
        self.title_view = QTableView(self)
        self.title_view.setModel(title_model)
        self.title_view.resizeColumnToContents(0)  # Modifying sizing of our QTableView

        new_title_width = self.title_view.columnWidth(0) + 45

        self.title_view_label.move(int((self.width() - new_title_width) / 2), 580)

        self.title_view.resize(new_title_width, 130)
        self.title_view.move(int((self.width() - new_title_width) / 2), 605)

        self.title_view.doubleClicked.connect(lambda: self.pass_info(
            self.title_view.selectionModel().currentIndex()))  # Allow users to go to new related recipe

        self.show()

    def pass_info(self, index):
        """
        PURPOSE
        -----
        To pass related recipe information in next window

        INPUT
        -----
        index: The index of the row+col selected by the user when they double click the recipe view

        OUTPUT
        -----
        calls function within RecipeWindow object we create in __init()__
        """
        # Get current indexed position from click
        cell_val = index.sibling(index.row(), index.column()).data()  # Get cell value from the cell itself
        self.recipe_title = cell_val
        self.title_view.hide()
        self.hide()
        self.view_recipe(self.obtain_recipe())

def main():
    app = QApplication([])
    w = SearchWindow()
    app.exec_()


if __name__ == "__main__":
    main()