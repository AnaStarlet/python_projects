import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Телефонный справочник ФМиИ")
        self.setGeometry(100, 100, 1300, 750)

        self.currentRow = -1
        self.setupDatabase()
        self.setupUI()
        self.setupModels()
        self.applyPinkStyle()

    def setupDatabase(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("phonebook.db")

        if not self.db.open():
            QMessageBox.critical(self, "Ошибка", "Не удалось открыть базу данных")
            sys.exit(1)

        query = QSqlQuery()
        query.exec("""
            CREATE TABLE IF NOT EXISTS phonebook (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                department TEXT,
                position TEXT,
                contact TEXT
            )
        """)

        query.exec("SELECT COUNT(*) FROM phonebook")
        query.next()
        if query.value(0) == 0:
            test_data = [
                # Кафедра математического анализа, дифференциальных уравнений и алгебры
                ("Бабич Елена Романовна", "Кафедра математического анализа, дифференциальных уравнений и алгебры",
                 "Старший преподаватель", ""),
                ("Белько Ольга Николаевна", "Кафедра математического анализа, дифференциальных уравнений и алгебры",
                 "Старший преподаватель", ""),
                ("Гринь Александр Александрович",
                 "Кафедра математического анализа, дифференциальных уравнений и алгебры", "Заведующий кафедрой",
                 "+375 152 396479"),
                ("Детченя Людмила Викторовна", "Кафедра математического анализа, дифференциальных уравнений и алгебры",
                 "Доцент", ""),
                ("Лукша Ирина Лешековна", "Кафедра математического анализа, дифференциальных уравнений и алгебры",
                 "Старший преподаватель", ""),
                ("Немец Владимир Стефанович", "Кафедра математического анализа, дифференциальных уравнений и алгебры",
                 "Доцент", ""),
                ("Павлючик Павел Болеславович", "Кафедра математического анализа, дифференциальных уравнений и алгебры",
                 "Доцент", ""),
                ("Пецевич Виктор Михайлович", "Кафедра математического анализа, дифференциальных уравнений и алгебры",
                 "Доцент", ""),
                (
                "Трифонова Ирина Владимировна", "Кафедра математического анализа, дифференциальных уравнений и алгебры",
                "Доцент", ""),
                ("Тыщенко Валентин Юрьевич", "Кафедра математического анализа, дифференциальных уравнений и алгебры",
                 "Доцент", ""),

                # Кафедра системного программирования и компьютерной безопасности
                ("Ващило Владимир Витольдович", "Кафедра системного программирования и компьютерной безопасности",
                 "Старший преподаватель", ""),
                ("Дирвук Евгений Владимирович", "Кафедра системного программирования и компьютерной безопасности",
                 "Доцент", ""),
                ("Зайкова Светлана Алексеевна", "Кафедра системного программирования и компьютерной безопасности",
                 "Доцент", ""),
                ("Кадан Александр Михайлович", "Кафедра системного программирования и компьютерной безопасности",
                 "Заведующий кафедрой", ""),
                ("Ливак Елена Николаевна", "Кафедра системного программирования и компьютерной безопасности", "Доцент",
                 ""),
                ("Марковская Наталья Вацлавовна", "Кафедра системного программирования и компьютерной безопасности",
                 "Доцент", ""),
                ("Просвирнина Ирина Борисовна", "Кафедра системного программирования и компьютерной безопасности",
                 "Доцент", ""),
                ("Разова Елена Леонидовна", "Кафедра системного программирования и компьютерной безопасности", "Доцент",
                 ""),
                ("Середа Елена Владимировна", "Кафедра системного программирования и компьютерной безопасности",
                 "Старший преподаватель", ""),

                # Кафедра современных технологий программирования
                ("Банюкевич Елена Викторовна", "Кафедра современных технологий программирования",
                 "Старший преподаватель", ""),
                ("Гуща Юлия Вальдемаровна", "Кафедра современных технологий программирования", "Старший преподаватель",
                 ""),
                ("Деева Наталия Владимировна", "Кафедра современных технологий программирования",
                 "Старший преподаватель", ""),
                ("Дейцева Анна Геннадьевна", "Кафедра современных технологий программирования", "Доцент", ""),
                ("Ермак Иван Валерьевич", "Кафедра современных технологий программирования", "Преподаватель", ""),
                ("Карканица Анна Викторовна", "Кафедра современных технологий программирования", "Заведующий кафедрой",
                 ""),
                (
                "Курьян Николай Николаевич", "Кафедра современных технологий программирования", "Старший преподаватель",
                ""),
                ("Куц Александр Иванович", "Кафедра современных технологий программирования", "Старший преподаватель",
                 ""),
                ("Макарова Нина Петровна", "Кафедра современных технологий программирования", "Доцент", ""),
                ("Мисник Марина Владимировна", "Кафедра современных технологий программирования",
                 "Старший преподаватель", ""),
                ("Родченко Вадим Григорьевич", "Кафедра современных технологий программирования", "Доцент", ""),
                ("Статкевич Святослав Эдуардович", "Кафедра современных технологий программирования", "Доцент", ""),
                ("Тарасевич Юрий Георгиевич", "Кафедра современных технологий программирования", "Доцент", ""),
                (
                "Урбан Ольга Ивановна", "Кафедра современных технологий программирования", "Старший преподаватель", ""),
                ("Хирьнов Иван Дмитриевич", "Кафедра современных технологий программирования", "Преподаватель-стажер",
                 ""),
                ("Шушкевич Геннадий Чеславович", "Кафедра современных технологий программирования", "Профессор", ""),

                # Кафедра фундаментальной и прикладной математики
                ("Вувуникян Юрий Микиртычевич", "Кафедра фундаментальной и прикладной математики", "Профессор",
                 "vuv@grsu.by"),
                ("Гончарова Марина Николаевна", "Кафедра фундаментальной и прикладной математики", "Доцент",
                 "m.gonchar@grsu.by"),
                ("Кузьмич Андрей Викторович", "Кафедра фундаментальной и прикладной математики", "Заведующий кафедрой",
                 "kuzmich_av@grsu.by"),
                ("Кулеш Елена Евгеньевна", "Кафедра фундаментальной и прикладной математики", "Доцент",
                 "kulesh@grsu.by"),
                ("Мисюк Виктор Романович", "Кафедра фундаментальной и прикладной математики", "Доцент",
                 "misiuk@grsu.by"),
                ("Мусафиров Эдуард Владимирович", "Кафедра фундаментальной и прикладной математики", "Доцент", ""),
                ("Поцейко Павел Геннадьевич", "Кафедра фундаментальной и прикладной математики", "Доцент",
                 "pahamatby@gmail.com"),
                ("Ровба Евгений Алексеевич", "Кафедра фундаментальной и прикладной математики", "Профессор",
                 "+375 152 740674"),
                ("Семенчук Наталья Владимировна", "Кафедра фундаментальной и прикладной математики", "Доцент",
                 "senata155@gmail.com"),
                ("Сетько Елена Александровна", "Кафедра фундаментальной и прикладной математики", "Доцент",
                 "setkoe@rambler.ru"),
                ("Смотрицкий Константин Анатольевич", "Кафедра фундаментальной и прикладной математики", "Доцент",
                 "k_smotritski@mail.ru"),
            ]

            for row in test_data:
                query.prepare("INSERT INTO phonebook (full_name, department, position, contact) VALUES (?, ?, ?, ?)")
                for val in row:
                    query.addBindValue(val)
                query.exec()

    def setupUI(self):
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Верхняя панель с поиском
        search_widget = QWidget()
        search_layout = QHBoxLayout(search_widget)
        search_layout.setSpacing(10)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Введите текст для поиска (ФИО, кафедра, должность, контакты)...")
        self.search_input.setMinimumHeight(35)

        self.search_category = QComboBox()
        self.search_category.addItems([
            "Поиск по всем полям",
            "Поиск по ФИО",
            "Поиск по кафедре",
            "Поиск по должности",
            "Поиск по контактам"
        ])
        self.search_category.setMinimumHeight(35)

        self.search_btn = QPushButton("🔍 Найти")
        self.search_btn.setMinimumHeight(35)
        self.search_btn.clicked.connect(self.on_search)

        self.refresh_btn = QPushButton("🔄 Обновить")
        self.refresh_btn.setMinimumHeight(35)
        self.refresh_btn.clicked.connect(self.on_refresh)

        search_layout.addWidget(self.search_input, 3)
        search_layout.addWidget(self.search_category, 2)
        search_layout.addWidget(self.search_btn, 1)
        search_layout.addWidget(self.refresh_btn, 1)

        # Таблица
        self.table = QTableView()
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.clicked.connect(self.on_table_click)

        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        # Нижняя панель с кнопками
        buttons_widget = QWidget()
        buttons_layout = QHBoxLayout(buttons_widget)
        buttons_layout.setSpacing(10)

        self.add_btn = QPushButton("➕ Добавить запись")
        self.add_btn.setMinimumHeight(40)
        self.add_btn.clicked.connect(self.on_add)

        self.delete_btn = QPushButton("🗑️ Удалить запись")
        self.delete_btn.setMinimumHeight(40)
        self.delete_btn.clicked.connect(self.on_delete)

        # Статистика
        self.stats_label = QLabel()
        self.stats_label.setMinimumHeight(40)
        self.stats_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        buttons_layout.addWidget(self.add_btn)
        buttons_layout.addWidget(self.delete_btn)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.stats_label)

        main_layout.addWidget(search_widget)
        main_layout.addWidget(self.table, 1)
        main_layout.addWidget(buttons_widget)

    def setupModels(self):
        self.model = QSqlTableModel(self, self.db)
        self.model.setTable("phonebook")
        self.model.setHeaderData(1, Qt.Orientation.Horizontal, "ФИО")
        self.model.setHeaderData(2, Qt.Orientation.Horizontal, "Кафедра")
        self.model.setHeaderData(3, Qt.Orientation.Horizontal, "Должность")
        self.model.setHeaderData(4, Qt.Orientation.Horizontal, "Контакты")
        self.model.select()

        self.proxy = QSortFilterProxyModel(self)
        self.proxy.setSourceModel(self.model)
        self.proxy.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)

        self.table.setModel(self.proxy)
        self.table.hideColumn(0)

        self.table.setColumnWidth(1, 380)
        self.table.setColumnWidth(2, 400)
        self.table.setColumnWidth(3, 200)

        self.update_stats()

    def update_stats(self):
        count = self.model.rowCount()
        self.stats_label.setText(f"📊 Всего записей: {count}")

    def applyPinkStyle(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #ffe4ec; }
            QTableView { 
                background-color: #fff0f3; 
                alternate-background-color: #ffe0e8; 
                selection-background-color: #ffb6c1; 
                gridline-color: #ffc0cb;
                font-size: 12px;
                border: 1px solid #ffc0cb;
            }
            QTableView::item { padding: 8px; }
            QTableView::item:selected { background-color: #ffb6c1; color: #8b3c4c; font-weight: bold; }
            QHeaderView::section { 
                background-color: #ffd0d8; 
                padding: 10px; 
                border: 1px solid #ffc0cb; 
                font-weight: bold; 
                color: #8b3c4c;
                font-size: 12px;
            }
            QPushButton { 
                background-color: #ffb6c1; 
                border: none; 
                padding: 10px 20px; 
                border-radius: 10px; 
                color: #8b3c4c; 
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover { background-color: #ff9eb0; }
            QPushButton:pressed { background-color: #ff8aa0; }
            QLineEdit { 
                border: 2px solid #ffc0cb; 
                border-radius: 8px; 
                padding: 8px; 
                background-color: #fff0f3; 
                color: #8b3c4c;
                font-size: 12px;
            }
            QLineEdit:focus { border-color: #ff9eb0; }
            QComboBox { 
                border: 2px solid #ffc0cb; 
                border-radius: 8px; 
                padding: 8px; 
                background-color: #fff0f3; 
                color: #8b3c4c;
                font-size: 12px;
            }
            QLabel { 
                color: #8b3c4c; 
                font-weight: bold;
                font-size: 12px;
            }
        """)

    def on_add(self):
        row = self.model.rowCount()
        self.model.insertRow(row)
        self.model.submitAll()
        self.table.scrollToBottom()
        self.update_stats()

    def on_delete(self):
        if self.currentRow >= 0:
            reply = QMessageBox.question(self, "Удаление", "Удалить выбранную запись?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                src_idx = self.proxy.mapToSource(self.proxy.index(self.currentRow, 0))
                self.model.removeRow(src_idx.row())
                self.model.submitAll()
                self.currentRow = -1
                self.update_stats()
        else:
            QMessageBox.warning(self, "Внимание", "Выберите запись для удаления")

    def on_table_click(self, index):
        self.currentRow = index.row()

    def on_search(self):
        text = self.search_input.text()
        if not text:
            self.proxy.setFilterRegularExpression(QRegularExpression())
            return

        search_type = self.search_category.currentIndex()

        if search_type == 0:
            self.proxy.setFilterKeyColumn(-1)
        elif search_type == 1:
            self.proxy.setFilterKeyColumn(1)
        elif search_type == 2:
            self.proxy.setFilterKeyColumn(2)
        elif search_type == 3:
            self.proxy.setFilterKeyColumn(3)
        elif search_type == 4:
            self.proxy.setFilterKeyColumn(4)

        regex = QRegularExpression(text, QRegularExpression.PatternOption.CaseInsensitiveOption)
        self.proxy.setFilterRegularExpression(regex)

    def on_refresh(self):
        self.model.select()
        self.search_input.clear()
        self.proxy.setFilterRegularExpression(QRegularExpression())
        self.search_category.setCurrentIndex(0)
        self.currentRow = -1
        self.update_stats()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())