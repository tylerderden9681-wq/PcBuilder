import sys
from PyQt6.QtGui import QFontDatabase
from PyQt6.QtWidgets import (
    QApplication, QWidget, QMainWindow,
    QVBoxLayout, QStackedWidget, QDialog,
)
from PyQt6.QtCore import Qt

from qt_widgets.project_page import ProjectPage
from qt_widgets.dashboard_page import DashboardPage
from managers.project_manager import ProjectManager
from qt_widgets.create_project_dialog import CreateProjectDialog
from qt_widgets.config_dialog import ConfigDialog
from managers.component_manager import ComponentManager
from qt_widgets.projects_list_page import ProjectsListPage


class PcBuilder(QMainWindow):
    def __init__(self):
        super().__init__()

        self.project_manager = ProjectManager()
        self.component_manager = ComponentManager()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("PC Builder")
        central_widget = QWidget()

        main_layout = QVBoxLayout(central_widget)

        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack)

        # Страница 0: Дашборд
        self.dashboard_page = DashboardPage(self.project_manager)
        self.dashboard_page.open_project.connect(self.open_project_page)
        self.dashboard_page.create_project.connect(self.create_new_project)
        self.dashboard_page.view_all_projects.connect(self.show_all_projects)
        self.stack.addWidget(self.dashboard_page)

        # Страница 1: Все проекты
        self.projects_list_page = ProjectsListPage(self.project_manager)
        self.projects_list_page.open_project.connect(self.open_project_page)
        self.projects_list_page.go_back.connect(self.show_dashboard)
        self.projects_list_page.create_project.connect(self.create_new_project)
        self.stack.addWidget(self.projects_list_page)

        # Страница 2: Детали проекта
        self.project_page = ProjectPage(
            self.project_manager, self.component_manager
        )
        self.project_page.go_back.connect(self.show_dashboard)
        self.stack.addWidget(self.project_page)

        self.stack.setCurrentIndex(0)

        self.setCentralWidget(central_widget)

    def open_project_page(self, project_id):
        """
        Обработчик клика на проект
        Загружает данные проекта и переключает на страницу деталей.
        """
        project_data = self.project_manager.get_project(project_id)
        if project_data:
            self.project_page.load_project(project_data)
            self.stack.setCurrentIndex(2)
        else:
            print(f"Проект №{project_id} не найден!")

    def show_all_projects(self):
        """Показывает страницу со всеми проектами"""
        self.stack.setCurrentIndex(1)
        self.projects_list_page.refresh()

    def show_dashboard(self):
        """Возврат к дашборду"""
        self.stack.setCurrentIndex(0)
        self.dashboard_page.refresh()

    def create_new_project(self):
        """Открывает диалог создания проекта, затем диалог конфигурации"""

        create_dialog = CreateProjectDialog(self)
        if create_dialog.exec() != QDialog.DialogCode.Accepted:
            return

        basic_data = create_dialog.get_data()

        config_dialog = ConfigDialog(
            basic_data["name"], self.component_manager, parent=self
        )
        config_dialog.exec()

        config_data = config_dialog.get_config_data()

        new_id = self.project_manager.get_next_id()
        full_project_data = {
            "name": basic_data["name"],
            "description": basic_data["description"],
            "price": config_data.get("price", "0"),
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
        self.show_dashboard()
        self.open_project_page(new_id)


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

        /* ===== Дашборд ===== */
        QWidget#DashboardPage {
            background-color: #18191a;
        }

        QFrame#WelcomeFrame {
            background-color: #242526;
            border: 2px solid #3a3b3c;
            border-radius: 10px;
        }

        QLabel#GreetingLabel {
            color: white;
            font-size: 28px;
            font-weight: bold;
        }

        QLabel#DateLabel {
            color: #8a8d91;
            font-size: 14px;
        }

        QLabel#WelcomeDesc {
            color: #b0b3b8;
            font-size: 16px;
        }

        QFrame#SectionFrame {
            background-color: #242526;
            border: 2px solid #3a3b3c;
            border-radius: 10px;
        }

        QLabel#SectionHeader {
            color: white;
            font-size: 18px;
            font-weight: bold;
        }

        QFrame#StatCard {
            background-color: #1e1f20;
            border: 2px solid #3a3b3c;
            border-radius: 6px;
        }

        QFrame#StatCard:hover {
            border: 1px solid #0078d7;
            background-color: #2d2f31;
        }

        QLabel#StatTitle {
            color: #8a8d91;
            font-size: 12px;
        }

        QLabel#StatValue {
            color: white;
            font-size: 18px;
            font-weight: bold;
            font-family: 'JetBrains Mono';
        }

        QPushButton#ActionButton {
            background-color: #0078d7;
            color: white;
            border: none;
            padding: 12px 20px;
            font-weight: bold;
            font-size: 14px;
            border-radius: 6px;
        }

        QPushButton#ActionButton:hover {
            background-color: #005a9e;
        }

        QPushButton#ActionButtonSecondary {
            background-color: #242526;
            color: white;
            border: 2px solid #3a3b3c;
            padding: 12px 20px;
            font-weight: bold;
            font-size: 14px;
            border-radius: 6px;
        }

        QPushButton#ActionButtonSecondary:hover {
            background-color: #2d2f31;
            border: 1px solid #0078d7;
        }

        QFrame#LinkCard {
            background-color: #1e1f20;
            border: 2px solid #3a3b3c;
            border-radius: 6px;
        }

        QFrame#LinkCard:hover {
            background-color: #2d2f31;
            border: 1px solid #0078d7;
        }

        QLabel#LinkTitle {
            color: white;
            font-size: 13px;
            font-weight: 600;
        }

        QLabel#LinkArrow {
            color: #0078d7;
            font-size: 16px;
            font-weight: bold;
        }

        QFrame#ProjectCardMini {
            background-color: #1e1f20;
            border: 2px solid #3a3b3c;
            border-radius: 6px;
        }

        QFrame#ProjectCardMini:hover {
            background-color: #2d2f31;
            border: 1px solid #0078d7;
        }

        QLabel#MiniProjectName {
            color: white;
            font-size: 14px;
            font-weight: 600;
        }

        QLabel#MiniProjectPrice {
            color: #4dc8ff;
            font-size: 13px;
            font-family: 'JetBrains Mono';
        }

        QLabel#EmptyProjectsLabel {
            color: #8a8d91;
            font-size: 14px;
            font-style: italic;
            padding: 20px;
        }

        /* ===== Страница проекта ===== */
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
            padding: 15px;
        }

        QFrame#PriceBlock {
            background-color: white;
            border: 3px solid #2e7d32;
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
        }

        #ExportButton:hover {
            background-color: rgba(128, 236, 255, 0.15);
        }

        #ExportButton:pressed {
            background-color: rgba(128, 236, 255, 0.25);
        }

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
        }

        #DialogButtonSecondary {
            color: white;
            background-color: transparent;
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

        #ConfigTabs {
            background-color: #242526;
            border: 1px solid #3a3b3c;
            border-top: none;
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

        QLineEdit#ConfigSearchInput {
            background-color: #1e1f20;
            color: white;
            border: 2px solid #3a3b3c;
            padding: 8px 12px;
            font-size: 13px;
        }

        QLineEdit#ConfigSearchInput:focus {
            border: 2px solid #0078d7;
        }

        QListWidget#ComponentList {
            background-color: #1e1f20;
            border: 2px solid #3a3b3c;
            padding: 4px;
            outline: none;
        }

        QListWidget#ComponentList::item {
            background-color: #242526;
            border: 2px solid #3a3b3c;
            margin: 4px 0px;
            padding: 0px;
        }

        QListWidget#ComponentList::item:hover {
            background-color: #2d2d2d;
            border: 2px solid #0078d7;
        }

        QListWidget#ComponentList::item:selected {
            background-color: #0078d7;
            border: 1px solid #005a9e;
        }

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

        QFrame#SummaryPanel {
            background-color: #0078d7;
            padding: 5px;
        }

        QLabel#SummaryLabel {
            color: white;
            font-size: 18px;
            font-weight: bold;
        }

        QLabel#TotalPriceLabel {
            color: white;
            font-size: 20px;
            font-weight: bold;
            font-family: 'JetBrains Mono';
        }

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

        /* ===== Футер ===== */
        QFrame#FooterFrame {
            background-color: #1e1f20;
            border: 2px solid #3a3b3c;
            margin-top: 10px;
            border-radius: 10px;
        }

        QPushButton#FooterLink {
            background-color: transparent;
            border: 2px solid white;
            border-radius: 6px;
            padding: 4px;
        }

        QPushButton#FooterLink:hover {
            background-color: #2d2f31;
        }

        QLabel#FooterLinkText {
            color: white;
            font-size: 12px;
        }

        QPushButton#FooterLink:hover QLabel#FooterLinkText {
            color: #0078d7;
        }

        QFrame#FooterLink {
            background-color: transparent;
            border-radius: 6px;
            border: 2px solid #3a3b3c;
        }

        QFrame#FooterLink:hover {
            background-color: #2d2f31;
        }

        QLabel#FooterLinkText {
            color: white;
            font-size: 14px;
            font-weight: 500;
        }

        QFrame#FooterLink:hover QLabel#FooterLinkText {
            color: #747474;
        }

        QLabel#FooterVersion {
            color: #4dc8ff;
            font-size: 12px;
            font-weight: bold;
            font-family: 'JetBrains Mono';
        }

        QLabel#FooterAuthor {
            color: #8a8d91;
            font-size: 12px;
            font-weight: 600;
        }

        QLabel#FooterYear {
            color: #8a8d91;
            font-size: 12px;
        }

        QLabel#FooterDot {
            color: #3a3b3c;
            font-size: 12px;
        }

        /* ===== Страница всех проектов ===== */
        QWidget#ProjectsListPage {
            background-color: #18191a;
        }

        QLabel#PageTitle {
            color: white;
            font-size: 24px;
            font-weight: bold;
        }

        QPushButton#ViewAllButton {
            background-color: #0078d7;
            color: white;
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 13px;
            font-weight: 600;
        }

        QPushButton#ViewAllButton:hover {
            background-color: #005a9e;
            color: white;
        }

        QLabel#EmptyLabel {
            color: #8a8d91;
            font-size: 16px;
            font-style: italic;
            padding: 40px;
        }

        #ProjectsScroll, #ProjectsContent {
            background-color: transparent;
        }

        /* ===== Карточки проектов ===== */
    `    QFrame#ProjectCard {
            background-color: #242526;
            border: 1px solid #3a3b3c;
            border-radius: 10px;
            padding: 15px;
            margin: 5px 0;
        }

        QFrame#ProjectCard:hover {
            border: 1px solid #0078d7;
            background-color: #2d2f31;
        }

        QLabel#ProjectTitle {
            font-weight: bold;
            font-size: 16px;
            color: #0078d7;
        }

        QLabel#ProjectDesc {
            color: #b0b3b8;
            background-color: #1e1f20;
            border-radius: 6px;
            padding: 6px 12px;
            font-size: 13px;
        }

        QLabel#ProjectConfig {
            color: #8a8d91;
            font-size: 12px;
            margin-top: 5px;
        }

        QLabel#ProjectPrice {
            font-weight: bold;
            color: #2e7d32;
            font-size: 14px;
            font-family: 'JetBrains Mono';
        }

        QLabel#PriceIcon {
            padding-top: 2px;
        }

        QLabel#DetailsLink {
            font-weight: 600;
            color: #0078d7;
        }

        QLabel#DetailsLink:hover {
            color: #4dc8ff;
        }

        /* ===== Панель управления ===== */
        QFrame#ControlPanel {
            background-color: #242526;
            border: 1px solid #3a3b3c;
            border-radius: 10px;
        }

        QLabel#ControlLabel {
            color: #8a8d91;
            font-size: 13px;
            font-weight: 600;
        }

        QLineEdit#SearchInput {
            background-color: #1e1f20;
            color: white;
            border: 1px solid #3a3b3c;
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 14px;
        }

        QLineEdit#SearchInput:focus {
            border: 1px solid #0078d7;
        }

        QComboBox#SortCombo {
            background-color: #1e1f20;
            color: white;
            border: 1px solid #3a3b3c;
            border-radius: 6px;
            padding: 6px 12px;
            font-size: 13px;
            min-width: 150px;
        }

        QPushButton#ViewButton {
            background-color: #1e1f20;
            border: 1px solid #3a3b3c;
            border-radius: 6px;
        }

        QPushButton#ViewButton:checked {
            background-color: #0078d7;
            border: 1px solid #005a9e;
        }

        QPushButton#ViewButton:hover {
            background-color: #2d2f31;
        }

        /* ===== Современная карточка проекта ===== */
        QFrame#ProjectCardModern {
            background-color: #242526;
            border: 2px solid #3a3b3c;
            border-radius: 12px;
            min-height: 200px;
        }

        QFrame#ProjectCardModern:hover {
            border: 2px solid #0078d7;
            background-color: #2d2f31;
        }

        QLabel#ProjectCardTitle {
            color: white;
            font-size: 16px;
            font-weight: bold;
        }

        QLabel#ProjectCardDesc {
            color: #b0b3b8;
            font-size: 13px;
            line-height: 1.4;
        }

        QLabel#ProjectCardConfig {
            color: #8a8d91;
            font-size: 12px;
            font-family: 'JetBrains Mono';
        }

        QLabel#ProjectCardPrice {
            color: #2e7d32;
            font-size: 18px;
            font-weight: bold;
            font-family: 'JetBrains Mono';
        }

        QPushButton#ProjectCardButton {
            background-color: #0078d7;
            color: white;
            border: none;
            border-radius: 6px;
            font-weight: 600;
            font-size: 13px;
        }

        QPushButton#ProjectCardButton:hover {
            background-color: #005a9e;
        }

        /* ===== Страница информации ===== */
        QWidget#InfoPage {
            background-color: #18191a;
        }

        QFrame#InfoCard {
            background-color: #242526;
            border: 1px solid #3a3b3c;
            border-radius: 12px;
        }

        QLabel#InfoCardTitle {
            color: white;
            font-size: 18px;
            font-weight: bold;
        }

        QLabel#InfoCardContent {
            color: #b0b3b8;
            font-size: 14px;
            line-height: 1.6;
        }

        QPushButton#FooterInfoButton {
            background-color: transparent;
            color: #747474;
            border: 2px solid #3a3b3c;
            padding: 8px 16px;
            font-size: 13px;
            font-weight: 600;
            border-radius: 6px;
        }

        QPushButton#FooterInfoButton:hover {
            background-color: #2d2f31;
        }

        #InfoScroll, #InfoContent {
            background-color: transparent;
        }

        /* ===== Карточки компонентов на странице проекта ===== */
        QFrame#ComponentCard {
            background-color: #242526;
            border: 2px solid #3a3b3c;
            border-radius: 12px;
            min-height: 80px;
        }

        QFrame#ComponentCard:hover {
            border: 2px solid #0078d7;
            background-color: #2d2f31;
        }

        QLabel#ComponentCardType {
            color: #8a8d91;
            font-size: 14px;
            font-weight: 600;
        }

        QLabel#ComponentCardName {
            color: white;
            font-size: 15px;
            font-weight: 600;
        }

        QLabel#ComponentCardPrice {
            color: #00B615;
            font-size: 16px;
            font-weight: bold;
            font-family: 'JetBrains Mono';
            min-width: 100px;
        }

        QLabel#EmptyComponentLabel {
            color: #8a8d91;
            font-size: 14px;
            font-style: italic;
            padding: 15px;
            background-color: #1e1f20;
            border-radius: 8px;
        }

        QLabel#SectionHeader {
            color: white;
            font-size: 20px;
            font-weight: bold;
            padding-bottom: 10px;
        }

        /* ===== Кнопки экспорта ===== */
        QPushButton#ExportButton {
            background-color: #242526;
            color: white;
            border: 1px solid #3a3b3c;
            border-radius: 8px;
        }

        QPushButton#ExportButton:hover {
            background-color: #2d2f31;
            border: 1px solid #0078d7;
        }

        QPushButton#ExportButton:pressed {
            background-color: #1e1f20;
        }
    """

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
            #DetailsLink, #ProjectPageTitle, #BlockHeader,
            #PriceBlockHeader, #StatValue, #MiniProjectPrice,
            #TotalPriceLabel, #TabTotalPriceLabel, #ConfigRowPrice,
            #DetailPrice {{
                font-family: '{jetbrains_family}';
            }}
        """

    app.setStyleSheet(global_styles)

    window = PcBuilder()
    window.setWindowState(Qt.WindowState.WindowMaximized)
    window.show()
    sys.exit(app.exec())
