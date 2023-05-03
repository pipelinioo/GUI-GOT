import sys
import pandas as pd
from PyQt6.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QComboBox, QTableWidget, QTableWidgetItem

class SearchWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Muertes Game of Thrones")
        self.resize(800, 600)

        # Importar la base de datos
        self.df = pd.read_csv(r"C:\Users\fidja\Desktop\Codigosss\tpa\GUI GOT\character_deaths.csv")
        # Widgets de búsqueda
        self.name_input = QLineEdit()
        self.loyalty_combo = QComboBox()
        self.year_input = QLineEdit()
        self.book_input = QLineEdit()
        self.chapter_input = QLineEdit()
        self.gender_combo = QComboBox()
        self.nobility_combo = QComboBox()

        # Configurar opciones de ComboBox
        self.loyalty_combo.addItem("Todos")
        self.df["Allegiances"] = self.df["Allegiances"].astype(str)
        self.loyalty_combo.addItems(self.df["Allegiances"].unique())
        self.gender_combo.addItem("Todos")
        self.df["Gender"] = self.df["Gender"].astype(str)
        self.gender_combo.addItems(self.df["Gender"].unique())
        self.nobility_combo.addItem("Todos")
        self.nobility_combo.addItem("Noble")
        self.nobility_combo.addItem("Común")

        # Botón de búsqueda
        self.search_button = QPushButton("Buscar")
        self.search_button.clicked.connect(self.search)

        # Tabla de resultados
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(6)
        self.result_table.setHorizontalHeaderLabels(["Nombre", "Lealtad", "Año de muerte", "Libro", "Capítulo", "Nobleza"])
        self.result_table.setRowCount(0)

        # Layouts
        search_layout = QVBoxLayout()
        search_layout.addWidget(QLabel("Nombre:"))
        search_layout.addWidget(self.name_input)
        search_layout.addWidget(QLabel("Lealtad:"))
        search_layout.addWidget(self.loyalty_combo)
        search_layout.addWidget(QLabel("Año de muerte:"))
        search_layout.addWidget(self.year_input)
        search_layout.addWidget(QLabel("Libro:"))
        search_layout.addWidget(self.book_input)
        search_layout.addWidget(QLabel("Capítulo:"))
        search_layout.addWidget(self.chapter_input)
        search_layout.addWidget(QLabel("Género:"))
        search_layout.addWidget(self.gender_combo)
        search_layout.addWidget(QLabel("Nobleza:"))
        search_layout.addWidget(self.nobility_combo)
        search_layout.addWidget(self.search_button)

        main_layout = QHBoxLayout()
        main_layout.addLayout(search_layout)
        main_layout.addWidget(self.result_table)

        self.setLayout(main_layout)

    def search(self):
        name = self.name_input.text().lower()
        loyalty = self.loyalty_combo.currentText()
        year = self.year_input.text()
        book = self.book_input.text()
        chapter = self.chapter_input.text()
        gender = self.gender_combo.currentText()
        nobility = self.nobility_combo.currentText()

        # Filtrar la base de datos
        query_str = f"Name.str.lower().str.contains('{name}')"
        if loyalty != "Todos":
            query_str += f" and Allegiances == '{loyalty}'"
        if year != "":
            query_str += f" and `Death Year` == {year}"
        if book != "":
            query_str += f" and `Book of Death` == {book}"
        if chapter != "":
            query_str += f" and `Death Chapter` == {chapter}"
        if gender != "Todos":
            query_str += f" and Gender == '{gender}'"
        if nobility != "Todos":
            if nobility == "Noble":
                query_str += " and Nobility == 1"
            elif nobility == "Común":
                query_str += " and Nobility == 0"

        filtered_df = self.df.query(query_str)

        # Mostrar los resultados en la tabla
        self.result_table.setRowCount(len(filtered_df))
        for i, row in filtered_df.iterrows():
            name_item = QTableWidgetItem(row["Name"])
            loyalty_item = QTableWidgetItem(row["Allegiances"])
            year_item = QTableWidgetItem(str(row["Death Year"]))
            book_item = QTableWidgetItem(str(row["Book of Death"]))
            chapter_item = QTableWidgetItem(str(row["Death Chapter"]))
            nobility_item = QTableWidgetItem("Sí" if row["Nobility"] else "No")

            self.result_table.setItem(i, 0, name_item)
            self.result_table.setItem(i, 1, loyalty_item)
            self.result_table.setItem(i, 2, year_item)
            self.result_table.setItem(i, 3, book_item)
            self.result_table.setItem(i, 4, chapter_item)
            self.result_table.setItem(i, 5, nobility_item)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SearchWindow()
    window.show()
    sys.exit(app.exec())
