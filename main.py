import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFontDatabase
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
    QVBoxLayout,
    QLabel,
    QFrame,
    QPushButton,
    QScrollArea,
    QStackedWidget,
    QDialog,
)

from qt_widgets.project_card import ProjectCard
from qt_widgets.project_page import ProjectPage
from managers.project_manager import ProjectManager
from qt_widgets.create_project_dialog import CreateProjectDialog
from qt_widgets.config_dialog import ConfigDialog
from qt_widgets.component_manager import ComponentManager


class PcBuilder(QMainWindow):
    def __init__(self):
        super().__init__()

        self.project_manager = ProjectManager()
        self.component_manager = ComponentManager()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Выбор проекта:")
        self.setFixedHeight(700)
        self.setFixedWidth(800)
        central_widget = QWidget()

        main_layout = QVBoxLayout(central_widget)

        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack)

        self.list_page = self._build_list_page()
        self.stack.addWidget(self.list_page)

        self.project_page = ProjectPage(self.project_manager)
        self.project_page.go_back.connect(self.show_list_page)
        self.stack.addWidget(self.project_page)

        self.stack.setCurrentIndex(0)

        self.setCentralWidget(central_widget)

    def _build_list_page(self):
        """Эта функция "собирает" начальную страницу"""
        page = QWidget()
        layout = QVBoxLayout(page)

        blue_gradient_text = (
            "Добро пожаловать в "
            "<span style='color:#0041a8;'>P</span>"
            "<span style='color:#0055c4;'>C</span>"
            "<span style='color:#006ae0;'>B</span>"
            "<span style='color:#0080ff;'>u</span>"
            "<span style='color:#1aa3ff;'>i</span>"
            "<span style='color:#33b5ff;'>l</span>"
            "<span style='color:#4dc8ff;'>d</span>"
            "<span style='color:#66daff;'>e</span>"
            "<span style='color:#80ecff;'>r</span>!"
        )

        welcome_title_label = QLabel(blue_gradient_text)
        welcome_title_label.setObjectName("WelcomeTitle")
        welcome_title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(welcome_title_label)

        welcome_desc_label = QLabel(
            "Выберите проект из предпложенного списка:"
        )
        welcome_desc_label.setObjectName("WelcomeDesc")
        welcome_desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(welcome_desc_label)

        scroll_area = QScrollArea()
        scroll_area.setObjectName("ProjectsScrollArea")
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn
        )

        # Создаем контейнер для списка карточек:
        scroll_content = QWidget()
        scroll_content.setObjectName("ScrollContent")
        self.cards_layout = QVBoxLayout(scroll_content)
        self.cards_layout.setSpacing(15)
        self.cards_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        all_projects = self.project_manager.get_all_projects()

        for pid, pd in all_projects.items():
            config = (
                f"{pd["config"]["cpu"]} | {pd["config"]["mat"]} | "
                f"{pd["config"]["gpu"]} | "
                f"{pd["config"]["pb"]}"
            )

            card = ProjectCard(
                project_id=pid,
                project_name=pd["name"],
                desc=pd["description"],
                price=pd["price"],
                config=config,
            )
            card.open_project.connect(self.open_project_page)

            self.cards_layout.addWidget(card)

        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)

        alter_title = QLabel("Или создайте новый проект")
        alter_title.setObjectName("AlterTitle")
        alter_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(alter_title)

        alter_button = QPushButton("+ Создать проект")
        alter_button.setObjectName("AlterButton")
        alter_button.setFixedWidth(180)
        alter_button.setCursor(Qt.CursorShape.PointingHandCursor)

        alter_button.clicked.connect(self.create_new_project)

        layout.addWidget(alter_button, alignment=Qt.AlignmentFlag.AlignCenter)

        return page

    def open_project_page(self, project_id):
        """
        Обработчик клика на ссылку "Подробнее"
        Загружает данные проекта и переключает на страницу деталей.
        """
        project_data = self.project_manager.get_project(project_id)
        if project_data:
            self.project_page.load_project(project_data)
            self.stack.setCurrentIndex(1)
        else:
            print(f"Проект №{project_id} не найден!")

    def show_list_page(self):
        """Возврат к списку проектов (обработчик go_back)"""
        # Переключаемся обратно на страницу с индексом 0:
        self.stack.setCurrentIndex(0)
        self.refresh_projects_list()

    def create_new_project(self):
        """Открывает диалог создания проекта, затем диалог конфигурации"""

        create_dialog = CreateProjectDialog(self)
        if create_dialog.exec() != QDialog.DialogCode.Accepted:
            return

        basic_data = create_dialog.get_data()

        config_dialog = ConfigDialog(
            basic_data["name"], self.component_manager, self
        )
        config_dialog.exec()

        config_data = config_dialog.get_config_data()

        new_id = self.project_manager.get_next_id()
        full_project_data = {
            "name": basic_data["name"],
            "description": basic_data["description"],
            "price": "0",
            "config": {
                "cpu": config_data["cpu"],
                "mat": config_data["mat"],
                "pb": config_data["pb"],
                "gpu": config_data["gpu"],
                "ram": config_data["ram"],
                "ssd": config_data["ssd"],
                "case": config_data["case"],
                "cooling": config_data["cooling"],
            },
        }

        self.project_manager.create_project(new_id, full_project_data)
        self.refresh_projects_list()
        self.open_project_page(new_id)

    def refresh_projects_list(self):
        """Очищает и заново строит список карточек проектов"""

        while self.cards_layout.count():
            item = self.cards_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        all_projects = self.project_manager.get_all_projects()

        for pid, pd in all_projects.items():
            config = (
                f"{pd["config"]["cpu"]} | {pd["config"]["mat"]} | "
                f"{pd["config"]["gpu"]} | {pd["config"]["pb"]}"
            )

            card = ProjectCard(
                project_id=pid,
                project_name=pd["name"],
                desc=pd["description"],
                price=pd["price"],
                config=config,
            )
            card.open_project.connect(self.open_project_page)
            self.cards_layout.addWidget(card)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    nunito_id = QFontDatabase.addApplicationFont("fonts/Nunito.ttf")
    jetbrains_id = QFontDatabase.addApplicationFont("fonts/JetBrainsMono.ttf")

    nunito_family = ""
    jetbrains_family = ""

    if nunito_id != -1:
        nunito_family = QFontDatabase.applicationFontFamilies(nunito_id)[0]
    else:
        print("Ошибка: не удалось загрузить шрифт Nunito!")

    if jetbrains_id != -1:
        jetbrains_family = QFontDatabase.applicationFontFamilies(
            jetbrains_id
        )[0]
    else:
        print("Ошибка: не удалось загрузить шрифт JetBrainsMono")

    global_styles = """
        QMainWindow { background-color: #18191a; }

        #WelcomeTitle {
            font-size: 24px;
            color: white;
            font-weight: bold;
            margin-top: 10px;
            margin-bottom: 5px;
        }

        #WelcomeDesc {
            font-weight: 600;
            margin-bottom: 10px;
            font-size: 16px;
        }

        #ProjectsScrollArea, #ScrollContent {
            background-color: transparent;
        }

        QFrame#ProjectCard {
            background-color: white;
            border: 1px solid #ced4da;
            border-radius: 8px;
            padding: 10px;
        }

        QFrame#ProjectCard:hover {
            border: 1px solid #0078d7;
            background-color: #f4f9ff;
        }

        #ProjectTitle {
            font-weight: bold;
            font-size: 16px;
            color: #0078d7;
        }

        #ProjectDesc {
            color: black;
            background-color: #d9d9d9;
            border-radius: 5px;
            padding: 4px 10px;
        }

        #ProjectConfig {
            color: #555555;
            font-size: 12px;
            margin-top: 2px;
        }

        #ProjectPrice {
            font-weight: bold;
            color: #2e7d32;
            font-size: 14px;
        }

        #PriceIcon {
            padding-top: 2px;
        }

        #DetailsLink {
            font-weight: 600;
        }

        #AlterTitle {
            color: #e0e0e0;
            font-size: 18px;
            font-weight: 600;
            margin-top: 5px;
            margin-bottom: 5px;
        }

        /* Стили для кнопки "Создать проект" */
        QPushButton#AlterButton {
            background-color: #0078d7;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 8px 16px;
            font-weight: bold;
            font-size: 14px;
            margin-bottom: 12px;
        }

        QPushButton#AlterButton:hover {
            background-color: #005a9e;
        }

        QPushButton#AlterButton:pressed {
            background-color: #004578;
        }

        /* Стили для страницы о проекте */
        #ProjectPage {
            background-color: #18191a;
        }

        #ProjectScroll, #ProjectContent {
            background-color: transparent;
        }

        QPushButton#BackButton {
            background-color: transparent;
            color: white;
            border: 1px solid white;
            border-radius: 6px;
            padding: 6px 14px;
            font-weight: bold;
            font-size: 13px;
        }

        QPushButton#BackButton:hover {
            background-color: rgba(128, 236, 255, 0.1);
        }

        #ProjectPageTitle {
            font-size: 20px;
            font-weight: 700;
            color: white;
        }

        QFrame#InfoBlock {
            background-color: white;
            border: 1px solid #3a3b3c;
            border-radius: 10px;
            padding: 15px;
        }

        QFrame#PriceBlock {
            background-color: white;
            border: 3px solid #2e7d32;
            border-radius: 10px;
            padding: 8px 15px;
        }

        #BlockHeader, #PriceBlockHeader {
            font-size: 16px;
            font-weight: bold;
        }

        #BlockHeader {
            color: #0078d7;
        }

        #PriceBlockHeader {
            color: green;
        }

        #BlockText {
            color: black;
            font-size: 14px;
            line-height: 1.5;
        }

        #BigPrice {
            color: green;
            font-size: 22px;
            font-weight: bold;
        }

        #ExportButton {
            background-color: transparent;
            color: white;
            border: 1px solid white;
            padding: 4px 10px;
            font-weight: bold;
            border-radius: 6px;
        }

        #ExportButton:hover {
            background-color: rgba(128, 236, 255, 0.15);
        }

        #ExportButton:pressed {
            background-color: rgba(128, 236, 255, 0.25);
        }

        /* Стили для кнопки редактирования */
        QPushButton#EditButton {
            background-color: transparent;
            border: none;
            border-radius: 15px;
            padding: 4px;
        }

        QPushButton#EditButton:hover {
            background-color: rgba(0, 120, 215, 0.2);
        }

        QPushButton#EditButton:pressed {
            background-color: rgba(0, 120, 215, 0.3);
        }

        QPushButton#DeleteButton {
            background-color: transparent;
            border: none;
            border-radius: 15px;
            padding: 4px;
        }

        QPushButton#DeleteButton:hover {
            background-color: rgba(252, 28, 3, 0.2);
        }

        /* Стили для диалога редактирования */
        QDialog#EditDialog {
            background-color: #18191a;
        }

        QLabel#EditDialogLabel {
            color: white;
            font-size: 16px;
            font-weight: bold;
        }

        QTextEdit#EditDialogTextEdit {
            background-color: #242526;
            color: white;
            border: 1px solid #3a3b3c;
            border-radius: 8px;
            padding: 10px;
            font-size: 14px;
        }

        QTextEdit#EditDialogTextEdit:focus {
            border: 1px solid #0078d7;
        }

        QPushButton#EditDialogButton {
            background-color: #0078d7;
            color: white;
            border: none;
            border-radius: 6px;
            font-weight: bold;
            font-size: 13px;
        }

        QPushButton#EditDialogButton:hover {
            background-color: #005a9e;
        }

        QPushButton#EditDialogButton:pressed {
            background-color: #004578;
        }

                /* ===== Стили для диалога конфигурации ===== */
        QDialog#ConfigDialog {
            background-color: #18191a;
        }

        QLabel#ConfigDialogTitle {
            color: white;
            font-size: 18px;
            font-weight: bold;
        }

        QLabel#ConfigDialogHint {
            color: #888;
            font-size: 12px;
            font-style: italic;
            margin-bottom: 5px;
        }

        QLabel#ConfigDialogLabel {
            color: #e0e0e0;
            font-size: 13px;
            font-weight: 600;
        }

        QLineEdit#ConfigDialogInput {
            background-color: #242526;
            color: white;
            border: 1px solid #3a3b3c;
            border-radius: 6px;
            padding: 6px 10px;
            font-size: 13px;
        }

        QLineEdit#ConfigDialogInput:focus {
            border: 1px solid #0078d7;
        }

        #ConfigDialogScroll, #ConfigDialogFields {
            background-color: transparent;
        }

        #DialogTitle {
            color: white;
            padding: 4px 12px;
            font-weight: 700;
            font-size: 18px;
            border-radius: 6px;
        }

        #DialogLabel {
            font-weight: 600;
            font-size: 14px;
        }

        #DialogButtonPrimary {
            color: white;
            border: 2px solid white;
            background-color: transparent;
            border-radius: 10px;
        }

        #DialogButtonSecondary {
            color: white;
            background-color: transparent;
            border-radius: 10px;
            border: 2px solid white;
        }

        #DialogButtonSecondary:hover, #DialogButtonPrimary:hover {
            background-color: rgba(252, 252, 252, 0.2)
        }

        QComboBox#ConfigDialogInput {
            background-color: #242526;
            color: white;
            border: 1px solid #3a3b3c;
            border-radius: 6px;
            padding: 6px 10px;
            font-size: 13px;
            font-family: "Jetbrains Mono";
        }

        QComboBox#ConfigDialogInput:focus {
            border: 1px solid #0078d7;
        }

        QComboBox#ConfigDialogInput::drop-down {
            border: none;
            width: 20px;
        }

        QComboBox#ConfigDialogInput::down-arrow {
            image: none;
            border-left: 4px solid transparent;
            border-right: 4px solid transparent;
            border-top: 6px solid white;
            margin-right: 5px;
        }

        QComboBox QAbstractItemView {
            background-color: #242526;
            color: white;
            border: 1px solid #3a3b3c;
            selection-background-color: #0078d7;
        }

        /* ===== Стили для QTabWidget ===== */
        #ConfigTabs {
            background-color: #242526;
            border: 1px solid #3a3b3c;
            border-top: none;
            border-radius: 0 0 8px 8px;
        }

        QTabBar::tab {
            background-color: #1e1f20;
            color: #aaa;
            padding: 10px 16px;
            border: 1px solid #3a3b3c;
            border-bottom: none;
            border-radius: 0 0 0 0;
            margin-right: 2px;
            font-size: 12px;
            font-weight: 600;
        }

        QTabBar::tab:selected {
            background-color: #242526;
            color: white;
            border-bottom: 2px solid #0078d7;
        }

        QTabBar::tab:hover {
            background-color: #2d2d2d;
            color: white;
        }

        /* ===== Содержимое вкладок ===== */
        QWidget#ConfigTab {
            background-color: #242526;
        }

        QLabel#TabHeader {
            color: white;
            font-size: 18px;
            font-weight: bold;
        }

        QLabel#TabDescription {
            color: #888;
            font-size: 12px;
            font-style: italic;
        }

        /* ===== Поле поиска ===== */
        QLineEdit#ConfigSearchInput {
            background-color: #1e1f20;
            color: white;
            border: 1px solid #3a3b3c;
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 13px;
        }

        QLineEdit#ConfigSearchInput:focus {
            border: 1px solid #0078d7;
        }

        /* ===== Список компонентов ===== */
        QListWidget#ComponentList {
            background-color: #1e1f20;
            border: 1px solid #3a3b3c;
            border-radius: 6px;
            padding: 4px;
            outline: none;
        }

        QListWidget#ComponentList::item {
            background-color: #242526;
            border: 1px solid #3a3b3c;
            border-radius: 6px;
            margin: 4px 0px;
            padding: 0px;
        }

        QListWidget#ComponentList::item:hover {
            background-color: #2d2d2d;
            border: 1px solid #0078d7;
        }

        QListWidget#ComponentList::item:selected {
            background-color: #0078d7;
            border: 1px solid #005a9e;
        }

        /* ===== Кастомный виджет компонента ===== */
        QWidget#ComponentItem {
            background-color: transparent;
        }

        QLabel#ComponentName {
            color: white;
            font-size: 13px;
            font-weight: 600;
        }

        QLabel#ComponentSpecs {
            color: #888;
            font-size: 11px;
        }

        QLabel#ComponentPrice {
            color: #4dc8ff;
            font-size: 14px;
            font-weight: bold;
        }

        QListWidget#ComponentList::item:selected QLabel#ComponentName,
        QListWidget#ComponentList::item:selected QLabel#ComponentSpecs,
        QListWidget#ComponentList::item:selected QLabel#ComponentPrice {
            color: white;
        }

        /* ===== Поле цены ===== */
        QLineEdit#ConfigPriceInput {
            background-color: #1e1f20;
            color: white;
            border: 1px solid #3a3b3c;
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 14px;
        }

        QLineEdit#ConfigPriceInput:focus {
            border: 1px solid #0078d7;
        }

        /* ===== Панель итоговой цены (внизу диалога) ===== */
        QFrame#SummaryPanel {
            background-color: #0078d7;
            border-radius: 8px;
            padding: 5px;
        }

        QLabel#SummaryLabel {
            color: white;
            font-size: 14px;
            font-weight: bold;
        }

        QLabel#TotalPriceLabel {
            color: white;
            font-size: 18px;
            font-weight: bold;
            font-family: 'JetBrains Mono';
        }

        /* ===== Вкладка "Итог" ===== */
        QWidget#ConfigListContainer {
            background-color: #1e1f20;
            border: 1px solid #3a3b3c;
            border-radius: 6px;
            padding: 10px;
        }

        QLabel#EmptyConfigLabel {
            color: #888;
            font-size: 13px;
            font-style: italic;
            padding: 20px;
        }

        QLabel#ConfigRowType {
            color: #888;
            font-size: 12px;
            font-weight: 600;
            min-width: 140px;
        }

        QLabel#ConfigRowName {
            color: white;
            font-size: 13px;
            padding: 0 10px;
        }

        QLabel#ConfigRowPrice {
            color: #4dc8ff;
            font-size: 14px;
            font-weight: bold;
            font-family: 'JetBrains Mono';
            min-width: 80px;
        }

        QFrame#ConfigSeparator {
            background-color: #3a3b3c;
            max-height: 1px;
        }

        QLabel#ConfigTotalLabel {
            color: white;
            font-size: 16px;
            font-weight: bold;
        }

        QLabel#TabTotalPriceLabel {
            color: #4dc8ff;
            font-size: 20px;
            font-weight: bold;
            font-family: 'JetBrains Mono';
        }

        /* ===== Полноэкранный диалог конфигурации ===== */
        QDialog#ConfigDialog {
            background-color: #18191a;
        }

        QLabel#ConfigDialogTitle {
            color: white;
            font-size: 22px;
            font-weight: bold;
            padding-bottom: 5px;
        }

        QLabel#ConfigDialogHint {
            color: #888;
            font-size: 13px;
            font-style: italic;
            padding-bottom: 10px;
        }

        /* ===== Вкладки ===== */
        QTabWidget#ConfigTabs::pane {
            background-color: #242526;
            border: 1px solid #3a3b3c;
            border-top: none;
            border-radius: 0 0 8px 8px;
        }

        QTabBar::tab {
            background-color: #1e1f20;
            color: #aaa;
            padding: 12px 20px;
            border: 1px solid #3a3b3c;
            border-bottom: none;
            border-radius: 6px 6px 0 0;
            margin-right: 2px;
            font-size: 13px;
            font-weight: 600;
            min-width: 100px;
        }

        QTabBar::tab:selected {
            background-color: #242526;
            color: white;
            border-bottom: 2px solid #0078d7;
        }

        QTabBar::tab:hover {
            background-color: #2d2d2d;
            color: white;
        }

        /* ===== Содержимое вкладок ===== */
        QWidget#ConfigTab {
            background-color: #242526;
        }

        QLabel#TabHeader {
            color: white;
            font-size: 20px;
            font-weight: bold;
            padding-bottom: 5px;
        }

        QLabel#TabDescription {
            color: #888;
            font-size: 13px;
            padding-bottom: 10px;
        }

        /* ===== Поле поиска ===== */
        QLineEdit#ConfigSearchInput {
            background-color: #1e1f20;
            color: white;
            border: 1px solid #3a3b3c;
            border-radius: 6px;
            padding: 10px 14px;
            font-size: 14px;
        }

        QLineEdit#ConfigSearchInput:focus {
            border: 1px solid #0078d7;
        }

        QLineEdit#ConfigSearchInput::placeholder {
            color: #666;
        }

        /* ===== Список компонентов ===== */
        QListWidget#ComponentList {
            background-color: #1e1f20;
            border: 1px solid #3a3b3c;
            border-radius: 6px;
            padding: 6px;
            outline: none;
            font-size: 13px;
        }

        QListWidget#ComponentList::item {
            background-color: #242526;
            border: 1px solid #3a3b3c;
            border-radius: 6px;
            margin: 4px 0px;
            padding: 0px;
        }

        QListWidget#ComponentList::item:hover {
            background-color: #2d2d2d;
            border: 1px solid #0078d7;
        }

        QListWidget#ComponentList::item:selected {
            background-color: #0078d7;
            border: 1px solid #005a9e;
        }

        /* Альтернативные строки */
        QListWidget#ComponentList::item:nth-child(even) {
            background-color: #2a2b2c;
        }

        QListWidget#ComponentList::item:nth-child(even):hover {
            background-color: #2d2d2d;
        }

        /* ===== Кастомный виджет компонента ===== */
        QWidget#ComponentItem {
            background-color: transparent;
        }

        QLabel#ComponentName {
            color: white;
            font-size: 14px;
            font-weight: 600;
        }

        QLabel#ComponentSpecs {
            color: #888;
            font-size: 12px;
        }

        QLabel#ComponentPrice {
            color: #4dc8ff;
            font-size: 15px;
            font-weight: bold;
        }

        QListWidget#ComponentList::item:selected QLabel#ComponentName,
        QListWidget#ComponentList::item:selected QLabel#ComponentSpecs,
        QListWidget#ComponentList::item:selected QLabel#ComponentPrice {
            color: white;
        }

        /* ===== Панель итоговой цены ===== */
        QFrame#SummaryPanel {
            background-color: #0078d7;
            border-radius: 8px;
            padding: 5px;
            margin-top: 5px;
        }

        QLabel#SummaryLabel {
            color: white;
            font-size: 16px;
            font-weight: bold;
        }

        QLabel#TotalPriceLabel {
            color: white;
            font-size: 22px;
            font-weight: bold;
            font-family: 'JetBrains Mono';
        }

        /* ===== Вкладка "Итог" ===== */
        QFrame#ConfigListContainer {
            background-color: #1e1f20;
            border: 1px solid #3a3b3c;
            border-radius: 8px;
        }

        QLabel#EmptyConfigLabel {
            color: #888;
            font-size: 14px;
            font-style: italic;
            padding: 40px;
        }

        QLabel#ConfigRowType {
            color: #888;
            font-size: 13px;
            font-weight: 600;
        }

        QLabel#ConfigRowName {
            color: white;
            font-size: 14px;
            padding: 0 10px;
        }

        QLabel#ConfigRowPrice {
            color: #4dc8ff;
            font-size: 15px;
            font-weight: bold;
            font-family: 'JetBrains Mono';
        }

        QFrame#ConfigSeparator {
            background-color: #3a3b3c;
            max-height: 1px;
            margin: 10px 0;
        }

        QLabel#ConfigTotalLabel {
            color: white;
            font-size: 18px;
            font-weight: bold;
        }

        QLabel#TabTotalPriceLabel {
            color: #4dc8ff;
            font-size: 24px;
            font-weight: bold;
            font-family: 'JetBrains Mono';
        }

        /* ===== Диалог детальной информации о компоненте ===== */
        QDialog#ComponentDetailDialog {
            background-color: #18191a;
        }

        QFrame#DetailHeader {
            background-color: #242526;
            border: 1px solid #3a3b3c;
            border-radius: 12px;
        }

        QLabel#DetailName {
            color: white;
            font-size: 22px;
            font-weight: bold;
        }

        QLabel#DetailPrice {
            color: #4dc8ff;
            font-size: 20px;
            font-weight: bold;
            font-family: 'JetBrains Mono';
        }

        QScrollArea#DetailScroll, QWidget#DetailContent {
            background-color: transparent;
        }

        QFrame#DetailGroup {
            background-color: #242526;
            border: 1px solid #3a3b3c;
            border-radius: 10px;
        }

        QLabel#DetailGroupHeader {
            color: #0078d7;
            font-size: 16px;
            font-weight: bold;
            padding-bottom: 8px;
        }

        QFrame#DetailFieldRow {
            background-color: #1e1f20;
            border-radius: 6px;
        }

        QFrame#DetailFieldRow:hover {
            background-color: #2d2f31;
        }

        QLabel#DetailFieldLabel {
            color: #8a8d91;
            font-size: 13px;
            font-weight: 600;
            min-width: 180px;
        }

        QLabel#DetailFieldValue {
            color: white;
            font-size: 14px;
            padding: 0 10px;
        }

        QPushButton#DetailButtonPrimary {
            background-color: #0078d7;
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: bold;
            font-size: 14px;
            padding: 10px 20px;
        }

        QPushButton#DetailButtonPrimary:hover {
            background-color: #005a9e;
        }

        QPushButton#DetailButtonSecondary {
            background-color: #242526;
            color: white;
            border: 1px solid #3a3b3c;
            border-radius: 8px;
            font-weight: bold;
            font-size: 14px;
            padding: 10px 20px;
        }

        QPushButton#DetailButtonSecondary:hover {
            background-color: #2d2f31;
            border: 1px solid #0078d7;
        }
    """

    # Применяем шрифт Nunito глобально:
    if nunito_family:
        global_styles += f"""
            * {{
                font-family: '{nunito_family}';
                font-size: 13px;
            }}
        """

    if jetbrains_family:
        global_styles += f"""
            #BlockText, #BigPrice, #ProjectConfig, #ProjectTitle,
            #DetailsLink, #AlterButton, #ProjectPageTitle, #BlockHeader,
            #PriceBlockHeader {{
                font-family: '{jetbrains_family}';
            }}
        """

    app.setStyleSheet(global_styles)

    window = PcBuilder()
    window.show()
    sys.exit(app.exec())
