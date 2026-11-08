import qtawesome as qta
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame, QPushButton,
    QGridLayout, QScrollArea, QLineEdit,
    QComboBox, QButtonGroup,
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize


class ProjectCardModern(QFrame):
    """Современная карточка проекта с анимацией"""

    open_project = pyqtSignal(str)

    def __init__(
            self, project_id, project_name,
            desc, price, config,
            parent=None
    ):
        super().__init__(parent)
        self.project_id = project_id
        self.setObjectName("ProjectCardModern")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMouseTracking(True)

        self._build_ui(project_name, desc, price, config)

    def _build_ui(self, project_name, desc, price, config):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        # Верх: иконка + название
        header_layout = QHBoxLayout()
        header_layout.setSpacing(10)

        icon = QLabel()
        icon.setPixmap(
            qta.icon("fa6s.box-open", color="#0078d7").pixmap(QSize(24, 24))
        )
        header_layout.addWidget(icon)

        title = QLabel(project_name)
        title.setObjectName("ProjectCardTitle")
        title.setWordWrap(True)
        header_layout.addWidget(title, stretch=1)

        layout.addLayout(header_layout)

        # Описание
        desc_label = QLabel(desc)
        desc_label.setObjectName("ProjectCardDesc")
        desc_label.setWordWrap(True)
        desc_label.setMaximumHeight(60)
        layout.addWidget(desc_label)

        # Конфигурация (кратко)
        config_preview = config.split(" | ")[0] if " | " in config else config
        config_label = QLabel(f"💻 {config_preview}")
        config_label.setObjectName("ProjectCardConfig")
        config_label.setWordWrap(True)
        layout.addWidget(config_label)

        layout.addStretch()

        # Низ: цена + кнопка
        footer_layout = QHBoxLayout()
        footer_layout.setSpacing(10)

        try:
            price_formatted = f"{int(price):,}₽".replace(",", " ")
        except Exception:
            price_formatted = price

        price_label = QLabel(price_formatted)
        price_label.setObjectName("ProjectCardPrice")
        footer_layout.addWidget(price_label)

        footer_layout.addStretch()

        details_btn = QPushButton("Открыть →")
        details_btn.setObjectName("ProjectCardButton")
        details_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        details_btn.setFixedSize(80, 30)
        details_btn.clicked.connect(
            lambda: self.open_project.emit(self.project_id)
        )
        footer_layout.addWidget(details_btn)

        layout.addLayout(footer_layout)

    def enterEvent(self, event):
        self.setProperty("hovered", True)
        self.style().unpolish(self)
        self.style().polish(self)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setProperty("hovered", False)
        self.style().unpolish(self)
        self.style().polish(self)
        super().leaveEvent(event)


class ProjectsListPage(QWidget):
    """Современная страница со всеми проектами"""

    open_project = pyqtSignal(str)
    go_back = pyqtSignal()
    create_project = pyqtSignal()

    def __init__(self, project_manager, parent=None):
        super().__init__(parent)
        self.project_manager = project_manager
        self.setObjectName("ProjectsListPage")
        self.current_view = "grid"
        self._build_ui()

    def _build_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        top_panel = self._build_top_panel()
        main_layout.addWidget(top_panel)

        control_panel = self._build_control_panel()
        main_layout.addWidget(control_panel)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setObjectName("ProjectsScroll")

        self.content = QWidget()
        self.content.setObjectName("ProjectsContent")
        self.projects_layout = QVBoxLayout(self.content)
        self.projects_layout.setSpacing(15)
        self.projects_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        scroll.setWidget(self.content)
        main_layout.addWidget(scroll, stretch=1)

        self._load_projects()

    def _build_top_panel(self):
        panel = QFrame()
        panel.setObjectName("TopPanel")
        layout = QHBoxLayout(panel)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(15)

        back_button = QPushButton()
        back_button.setIcon(qta.icon("fa6s.arrow-left", color="white"))
        back_button.setIconSize(QSize(20, 20))
        back_button.setObjectName("BackButton")
        back_button.setCursor(Qt.CursorShape.PointingHandCursor)
        back_button.setFixedSize(44, 44)
        back_button.clicked.connect(self.go_back.emit)
        layout.addWidget(back_button)

        title_label = QLabel("Все проекты")
        title_label.setObjectName("PageTitle")
        layout.addWidget(title_label, stretch=1)

        create_btn = QPushButton("Создать проект")
        create_btn.setObjectName("ActionButton")
        create_btn.setIcon(qta.icon("fa6s.plus", color="white"))
        create_btn.setIconSize(QSize(20, 20))
        create_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        create_btn.clicked.connect(self.create_project.emit)
        layout.addWidget(create_btn)

        return panel

    def _build_control_panel(self):
        panel = QFrame()
        panel.setObjectName("ControlPanel")
        layout = QHBoxLayout(panel)
        layout.setContentsMargins(15, 12, 15, 12)
        layout.setSpacing(12)

        # Поиск
        search_icon = QLabel()
        search_icon.setPixmap(
            qta.icon(
                "fa6s.magnifying-glass",
                color="#8a8d91"
            ).pixmap(QSize(16, 16))
        )
        layout.addWidget(search_icon)

        self.search_input = QLineEdit()
        self.search_input.setObjectName("SearchInput")
        self.search_input.setPlaceholderText("Поиск проектов...")
        self.search_input.textChanged.connect(self._filter_projects)
        layout.addWidget(self.search_input, stretch=1)

        # Сортировка
        sort_label = QLabel("Сортировка:")
        sort_label.setObjectName("ControlLabel")
        layout.addWidget(sort_label)

        self.sort_combo = QComboBox()
        self.sort_combo.setObjectName("SortCombo")
        self.sort_combo.addItems([
            "По дате (новые)",
            "По дате (старые)",
            "По цене (дорогие)",
            "По цене (дешёвые)",
            "По названию (А-Я)",
        ])
        self.sort_combo.currentIndexChanged.connect(self._load_projects)
        layout.addWidget(self.sort_combo)

        # Переключатель вида
        view_label = QLabel("Вид:")
        view_label.setObjectName("ControlLabel")
        layout.addWidget(view_label)

        self.view_group = QButtonGroup(self)

        grid_btn = QPushButton()
        grid_btn.setIcon(qta.icon("fa6s.grip", color="white"))
        grid_btn.setIconSize(QSize(18, 18))
        grid_btn.setObjectName("ViewButton")
        grid_btn.setCheckable(True)
        grid_btn.setChecked(True)
        grid_btn.setFixedSize(36, 36)
        grid_btn.clicked.connect(lambda: self._switch_view("grid"))
        self.view_group.addButton(grid_btn)
        layout.addWidget(grid_btn)

        list_btn = QPushButton()
        list_btn.setIcon(qta.icon("fa6s.list", color="white"))
        list_btn.setIconSize(QSize(18, 18))
        list_btn.setObjectName("ViewButton")
        list_btn.setCheckable(True)
        list_btn.setFixedSize(36, 36)
        list_btn.clicked.connect(lambda: self._switch_view("list"))
        self.view_group.addButton(list_btn)
        layout.addWidget(list_btn)

        return panel

    def _switch_view(self, view):
        self.current_view = view
        self._load_projects()

    def _filter_projects(self):
        self._load_projects()

    def _load_projects(self):
        while self.projects_layout.count():
            item = self.projects_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        projects = self.project_manager.get_all_projects()
        search_text = self.search_input.text().lower()

        # Фильтрация
        filtered = {}
        for pid, pdata in projects.items():
            if (
                search_text in pdata["name"].lower() or
                search_text in pdata["description"].lower()
            ):
                filtered[pid] = pdata

        # Сортировка
        sort_index = self.sort_combo.currentIndex()
        items = list(filtered.items())

        if sort_index == 0:  # По дате (новые)
            items.sort(key=lambda x: int(x[0]), reverse=True)
        elif sort_index == 1:  # По дате (старые)
            items.sort(key=lambda x: int(x[0]))
        elif sort_index == 2:  # По цене (дорогие)
            items.sort(key=lambda x: int(x[1].get("price", 0)), reverse=True)
        elif sort_index == 3:  # По цене (дешёвые)
            items.sort(key=lambda x: int(x[1].get("price", 0)))
        elif sort_index == 4:  # По названию
            items.sort(key=lambda x: x[1]["name"])

        if not items:
            empty_label = QLabel("Проекты не найдены")
            empty_label.setObjectName("EmptyLabel")
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.projects_layout.addWidget(empty_label)
            return

        if self.current_view == "grid":
            # Если грид сетка
            grid = QGridLayout()
            grid.setSpacing(15)

            for i, (pid, pdata) in enumerate(items):
                row = i // 3  # 3 колонки
                col = i % 3

                config = (
                    f"{pdata['config'].get('cpu', '—')} | "
                    f"{pdata['config'].get('gpu', '—')}"
                )

                card = ProjectCardModern(
                    project_id=pid,
                    project_name=pdata["name"],
                    desc=pdata["description"],
                    price=pdata["price"],
                    config=config,
                )
                card.open_project.connect(self.open_project.emit)
                grid.addWidget(card, row, col)

            self.projects_layout.addLayout(grid)
        else:
            # Если список
            for pid, pdata in items:
                config = (
                    f"{pdata['config'].get('cpu', '—')} | "
                    f"{pdata['config'].get('gpu', '—')}"
                )

                card = ProjectCardModern(
                    project_id=pid,
                    project_name=pdata["name"],
                    desc=pdata["description"],
                    price=pdata["price"],
                    config=config,
                )
                card.open_project.connect(self.open_project.emit)
                self.projects_layout.addWidget(card)

    def refresh(self):
        self._load_projects()
