import sys
from PyQt6.QtGui import QFontDatabase, QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
    QVBoxLayout,
    QStackedWidget,
    QDialog,
)
from PyQt6.QtCore import Qt

from app_paths import get_icon_path, get_db_path, get_font_path
from qt_widgets.project_page import ProjectPage
from qt_widgets.dashboard_page import DashboardPage
from managers.project_manager import ProjectManager
from qt_widgets.create_project_dialog import CreateProjectDialog
from qt_widgets.config_dialog import ConfigDialog
from managers.component_manager import ComponentManager
from qt_widgets.projects_list_page import ProjectsListPage
from styles import get_stylesheet


class PcBuilder(QMainWindow):
    def __init__(self):
        super().__init__()
        self.project_manager = ProjectManager()
        self.component_manager = ComponentManager(get_db_path())
        self.initUI()

    def initUI(self):
        self.setWindowTitle("PC Builder")
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)

        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack)

        self.dashboard_page = DashboardPage(self.project_manager)
        self.dashboard_page.open_project.connect(self.open_project_page)
        self.dashboard_page.create_project.connect(self.create_new_project)
        self.dashboard_page.view_all_projects.connect(self.show_all_projects)
        self.stack.addWidget(self.dashboard_page)

        self.projects_list_page = ProjectsListPage(self.project_manager)
        self.projects_list_page.open_project.connect(self.open_project_page)
        self.projects_list_page.go_back.connect(self.show_dashboard)
        self.projects_list_page.create_project.connect(self.create_new_project)
        self.stack.addWidget(self.projects_list_page)

        self.project_page = ProjectPage(
            self.project_manager,
            self.component_manager
        )
        self.project_page.go_back.connect(self.show_dashboard)
        self.project_page.project_deleted.connect(self._on_project_deleted)
        self.project_page.project_renamed.connect(self._on_project_renamed)
        self.stack.addWidget(self.project_page)

        self.stack.setCurrentIndex(0)
        self.setCentralWidget(central_widget)

    def open_project_page(self, project_id):
        project_data = self.project_manager.get_project(project_id)
        if project_data:
            self.project_page.load_project(project_data)
            self.stack.setCurrentIndex(2)
        else:
            print(f"Проект №{project_id} не найден!")

    def show_all_projects(self):
        self.stack.setCurrentIndex(1)
        self.projects_list_page.refresh()

    def show_dashboard(self):
        self.stack.setCurrentIndex(0)
        self.dashboard_page.refresh()

    def create_new_project(self):
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

    def _on_project_deleted(self, project_id: str):
        """Обработчик удаления проекта"""
        print(f"Проект {project_id} удалён")

    def _on_project_renamed(self, project_id: str, new_name: str):
        """Обработчик переименования проекта"""
        print(f"Проект {project_id} переименован в '{new_name}'")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    nunito_id = QFontDatabase.addApplicationFont(get_font_path("Nunito.ttf"))
    jetbrains_id = QFontDatabase.addApplicationFont(
        get_font_path("JetBrainsMono.ttf"),
    )

    nunito_family = (
        QFontDatabase.applicationFontFamilies(
            nunito_id
        )[0] if nunito_id != -1 else ""
    )
    jetbrains_family = (
        QFontDatabase.applicationFontFamilies(jetbrains_id)[0]
        if jetbrains_id != -1
        else ""
    )

    if not nunito_family:
        print("Ошибка: не удалось загрузить шрифт Nunito!")
    if not jetbrains_family:
        print("Ошибка: не удалось загрузить шрифт JetBrainsMono")

    app.setStyleSheet(get_stylesheet(nunito_family, jetbrains_family))

    app.setWindowIcon(QIcon(str(get_icon_path())))

    window = PcBuilder()
    window.setWindowState(Qt.WindowState.WindowMaximized)
    window.show()
    sys.exit(app.exec())
