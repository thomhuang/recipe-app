from PyQt5.QtSql import *
from PyQt5.QtWidgets import *

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
        self.recipe_window.initView()


class RecipeWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.recipe_title = ""

        self.conn = QSqlDatabase.addDatabase("QSQLITE")
        self.conn.setDatabaseName("recipes.db")

    def initView(self):
        self.view_recipe()

    def view_recipe(self):
        recipe_info_cmd = \
            f"""
        SELECT R.`Recipe Title`, R.Author, R.Cuisine, R.Ingredients, R.`Recipe Procedure`, R.Tags
        FROM recipes R
        WHERE R.`Recipe Title` = "{self.recipe_title}"
        """
        # Query to get title, author, ingredients, and recipe procedure from desired recipe title
        recipe_query = QSqlQuery(self.conn)  # Same process as the title_query
        recipe_query.prepare(recipe_info_cmd)
        recipe_query.exec_()

        recipe_model = QSqlQueryModel()
        recipe_model.setQuery(recipe_query)

        self.recipe_view = QTableView()
        self.recipe_view.setModel(recipe_model)

        self.recipe_view.show()

        def initUI():
            self.setGeometry(0, 0, 900, 500)
            self.show()


def main():
    app = QApplication([])
    w = SearchWindow()
    app.exec_()


if __name__ == "__main__":
    main()
