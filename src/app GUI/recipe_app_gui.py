from PyQt5.QtSql import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class SearchWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.title_window = RecipeTitleWindow()
        self.initUI()  # Initialize our UI elements

    def initUI(self):
        self.setWindowTitle("Recipe Application")
        self.setGeometry(0, 0, 500, 140)
        self.setFixedSize(self.width(), self.height())

        self.instruction_label = QLabel("Please input each search item separated by a comma!",
                                        self)  # Instruction label
        self.instruction_label.move(120, 20)

        self.search_combobox = QComboBox(self)
        self.search_combobox.addItem("Recipe Title")
        self.search_combobox.addItem("Author")
        self.search_combobox.addItem("Cuisine")
        self.search_combobox.addItem("Ingredients")
        self.search_combobox.addItem("Tags")
        self.search_combobox.move(50, 60)

        self.search_text_edit = QLineEdit(self)  # Text box to insert ingredients-to-be-queried
        self.search_text_edit.move(150, 50)
        self.search_text_edit.resize(300, 40)

        self.search_button = QPushButton('Search Recipes', self)  # Button to search for recipes
        self.search_button.move(200, 100)

        self.search_button.clicked.connect(self.pass_info)  # Connect button to function to query

        self.show()

    def pass_info(self):
        self.title_window.search_category = str(self.search_combobox.currentText())

        self.title_window.search_text = self.search_text_edit.text()

        self.title_window.initSearch()

class RecipeTitleWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.search_text = ""
        self.search_category = ""

        self.recipe_window = RecipeWindow()

        self.conn = QSqlDatabase.addDatabase("QSQLITE")
        self.conn.setDatabaseName("recipes.db")

    def initSearch(self):
        self.recipe_search()

    def recipe_search(self):
        self.conn.open()

        if len(self.search_text.strip(' ')) == 0:
            error_dialog = QErrorMessage()
            error_dialog.showMessage(
                f"It seems you haven't input anything to search for the {self.search_category.lower()}'s associated recipes! Please try again.")
            error_dialog.exec_()
        else:

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

            self.title_view = QTableView()  # Adds information from out query model to a QTableView to be seen
            self.title_view.setModel(title_model)
            self.title_view.setWindowTitle("Recipe List")

            self.title_view.doubleClicked.connect(self.pass_info)

            self.title_view.resizeColumnToContents(0)
            self.title_view.resize(self.title_view.columnWidth(0) + 45, 500)
            self.title_view.show()

            # Adds functionality of view_recipe when double clicking cell

    def pass_info(self):
        index = (self.title_view.selectionModel().currentIndex())  # Get current indexed position from click
        cell_val = index.sibling(index.row(), index.column()).data()  # Get cell value from the cell itself
        self.recipe_window.recipe_title = cell_val

        self.title_view.hide()
        self.recipe_window.view_recipe(self.recipe_window.obtain_recipe())


class RecipeWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.recipe_title = ""

        self.conn = QSqlDatabase.addDatabase("QSQLITE")
        self.conn.setDatabaseName("recipes.db")

    def obtain_recipe(self):
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
        # All values taken from QSqlQuery returned in obtain_recipe() function
        recipe_title = model.record(0).value(0)  # Recipe title
        recipe_author = model.record(0).value(1)  # Recipe author
        recipe_cuisine = model.record(0).value(2)  # Recipe cuisine
        recipe_ingredients = model.record(0).value(3)  # Recipe ingredients
        recipe_steps = model.record(0).value(4)  # Recipe steps
        self.recipe_tags = model.record(0).value(5)  # Recipe tags
        recipe_website = model.record(0).value(6)  # Recipe website

        self.setGeometry(0, 0, 900, 700)

        # Everything done below is pretty self explanatory; create label/textedit, populate, move, etc.

        title = QLabel(self)
        title.setText("")
        title.setText(recipe_title)
        title.setWordWrap(True)  # Enables word wrap for specific label
        title.setFont(QFont('Arial', 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setFixedWidth(600)
        title.move(150, 10)

        author_label = QLabel("Author: ", self)
        author_label.move(45, 90)
        author_label.setFont(QFont('Arial', 10, QFont.Bold))

        author = QLabel(self)
        author.setText(recipe_author)
        author.move(95, 90)
        author.setFont(QFont('Arial', 10))

        cuisine_label = QLabel("Cuisine: ", self)
        cuisine_label.move(265, 90)
        cuisine_label.setFont(QFont('Arial', 10, QFont.Bold))

        cuisine = QLabel(self)
        cuisine.setText(recipe_cuisine)
        cuisine.move(320, 90)
        cuisine.setFont(QFont('Arial', 10))

        tag_label = QLabel("Tags: ", self)
        tag_label.move(485, 90)
        tag_label.setFont(QFont('Arial', 10, QFont.Bold))

        tags = QLabel(self)
        tags.setFixedWidth(330)
        tags.setText(self.recipe_tags)
        tags.setWordWrap(True)
        tags.move(525, 90)
        tags.setFont(QFont('Arial', 10))

        ingredients_label = QLabel("Ingredients: ", self)
        ingredients_label.setFont(QFont('Arial', 10, QFont.Bold))
        ingredients_label.move(45, 140)

        ingredients = QTextEdit(self)
        ingredients.setText(recipe_ingredients)
        ingredients.setFixedWidth(200)
        ingredients.setFixedHeight(300)
        ingredients.move(30, 170)
        ingredients.setFont(QFont('Arial', 10))

        recipe_label = QLabel("Recipe Procedure: ", self)
        recipe_label.setFont(QFont('Arial', 10, QFont.Bold))
        recipe_label.move(265, 140)

        recipe = QTextEdit(self)
        recipe.setText(recipe_steps)
        recipe.setFixedWidth(610)
        recipe.setFixedHeight(300)
        recipe.move(250, 170)
        recipe.setFont(QFont('Arial', 10))

        website_url_label = QLabel("If you'd like to see full details of this recipe click here: ", self)
        website_url_label.setFont(QFont('Arial', 10, QFont.Bold))
        website_url_label.move(35, 510)

        website_url = QLabel(self)
        website_url.setText('<a href="' + recipe_website + '/">' + recipe_title + '</a>')  # Creates hyperlink
        website_url.setOpenExternalLinks(True)  # Allows us to click on hyperlink
        website_url.move(385, 510)
        website_url.setFont(QFont('Arial', 10))

        self.show()


def main():
    app = QApplication([])
    w = SearchWindow()
    app.exec_()


if __name__ == "__main__":
    main()
