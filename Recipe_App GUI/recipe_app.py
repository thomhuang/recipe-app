from PyQt5.QtSql import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import sqlite3


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.conn = QSqlDatabase.addDatabase("QSQLITE")
        self.conn.setDatabaseName("recipes.db")

        self.initUI()  # Initialize our UI elements

    def initUI(self):
        self.setWindowTitle("Recipe Application")
        self.setGeometry(0, 0, 400, 140)
        self.setFixedSize(self.width(), self.height())

        self.instruction_label = QLabel("Please input your ingredients separated by commas!", self)  # Instruction label
        self.instruction_label.move(70, 20)

        self.ingredient_text = QLineEdit(self)  # Text box to insert ingredients-to-be-queried
        self.ingredient_text.move(50, 50)
        self.ingredient_text.resize(300, 40)

        self.search_button = QPushButton('Search Recipes', self)  # Button to search for recipes
        self.search_button.move(150, 100)
        self.search_button.clicked.connect(self.ingredient_search)  # Connect button to function to query

        self.show()

    def drawWindow(self, qp):
        qp.drawRect(0, 0, self.width(), self.height())

    def ingredient_search(self):
        self.conn.open()

        ingredient_text = self.ingredient_text.text()  # Obtain text from our QLineEdit

        if len(ingredient_text.strip(' ')) == 0:
            error_dialog = QErrorMessage()
            error_dialog.showMessage("It seems you have input no ingredients! Please try again")
            error_dialog.exec_()
        else:

            ingredient_list = ingredient_text.split(',')  # Create an array of desired ingredients

            ingred_query = ""  # Empty string to construct our query
            for ingredients in ingredient_list:
                # Here we construct our query through a for-loop
                # There shouldn't be many elements in our array in the first place, so no worries of efficiency
                ingred_query += "ingredients LIKE '%" + ingredients + "%' AND "

            if len(ingred_query) > 5:  # On the off chance that there is nothing input into the text box, throw error
                ingred_query = ingred_query[:len(ingred_query) - 5]

            cmd = \
                f"""
                SELECT title FROM recipes R WHERE {ingred_query}
                """

            title_query = QSqlQuery(self.conn)  # Establish our query, prepare, and execute it
            title_query.prepare(cmd)
            title_query.exec()

            title_model = QSqlQueryModel()  # Adds our queried information into a read-only model
            title_model.setQuery(title_query)

            self.title_view = QTableView()  # Adds information from out query model to a QTableView to be seen
            self.title_view.setModel(title_model)
            self.title_view.setColumnWidth(0, self.width())
            self.title_view.resizeColumnToContents(0)

            self.title_view.doubleClicked.connect(self.view_recipe)

            self.title_view.show()
            # Adds functionality of view_recipe when double clicking cell

    def view_recipe(self):
        index = (self.title_view.selectionModel().currentIndex())  # Get current indexed position from click
        cell_val = index.sibling(index.row(), index.column()).data()  # Get cell value from the cell itself

        recipe_info_cmd = \
            f"""
        SELECT R.title, R.author, R.ingredients, R.'recipe procedure'
        FROM recipes R
        WHERE R.title = "{cell_val}"
        """
        # Query to get title, author, ingredients, and recipe procedure from desired recipe title

        recipe_query = QSqlQuery(self.conn)  # Same process as the title_query
        recipe_query.prepare(recipe_info_cmd)
        recipe_query.exec()

        recipe_model = QSqlQueryModel()
        recipe_model.setQuery(recipe_query)

        self.recipe_view = QTableView()
        self.recipe_view.setModel(recipe_model)

        self.recipe_view.resizeColumnToContents(0)  # Resize all of our columns to fit the contents
        self.recipe_view.resizeColumnToContents(1)
        self.recipe_view.resizeColumnToContents(2)
        self.recipe_view.resizeColumnToContents(3)

        self.title_view.hide()

        self.recipe_view.show()


def main():
    app = QApplication([])
    w = MyWidget()
    app.exec_()


if __name__ == "__main__":
    main()
