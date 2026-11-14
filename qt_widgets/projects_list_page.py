import qtawesome as qta
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QPushButton, QGridLayout, QScrollArea,
    QLineEdit, QComboBox
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize


class ProjectCardModern(QFrame):
    """Адаптивная карточка проекта (работает и в сетке, и в списке)"""

    open_project = pyqtSignal(str)

    def __init__(
            self, project_id, project_name,
            desc, price, config,
            is_list_view=False, parent=None
    ):
        super().__init__(parent)
        self.project_id = project_id
        self.setObjectName("ProjectCardModern")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.is_list_view = is_list_view

        self._build_ui(project_name, desc, price, config)

    def _build_ui(self, project_name, desc, price, config):
        # В режиме списка используем горизонтальный layout, в сетке - вертикальный
        main_layout = QHBoxLayout(self) if self.is_list_view else QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # 1. Левая часть: Иконка + Название + Описание
        left_layout = QVBoxLayout()
        left_layout.setSpacing(8)

        header_layout = QHBoxLayout()
        header_layout.setSpacing(10)
        
        icon = QLabel()
        icon.setPixmap(qta.icon("fa6s.box-open", color="#0078d7").pixmap(QSize(24, 24)))
        header_layout.addWidget(icon)

        title = QLabel(project_name)
        title.setObjectName("ProjectCardTitle")
        title.setWordWrap(True)
        header_layout.addWidget(title, stretch=1)
        
        left_layout.addLayout(header_layout)

        desc_label = QLabel(desc)
        desc_label.setObjectName("ProjectCardDesc")
        desc_label.setWordWrap(True)
        if not self.is_list_view:
            desc_label.setMaximumHeight(60) # Ограничиваем высоту только в сетке
        left_layout.addWidget(desc_label)

        main_layout.addLayout(left_layout, stretch=2 if self.is_list_view else 1)

        # Разделитель для режима списка
        if self.is_list_view:
            v_line = QFrame()
            v_line.setFrameShape(QFrame.Shape.VLine)
            v_line.setFrameShadow(QFrame.Shadow.Sunken)
            v_line.setStyleSheet("color: #3a3b3c;")
            main_layout.addWidget(v_line)

        # 2. Правая часть: Конфигурация + Цена + Кнопка
        right_layout = QVBoxLayout()
        right_layout.setSpacing(12)

        # Конфигурация (теперь с иконками)
        config_layout = QHBoxLayout()
        config_layout.setSpacing(8)

        cpu_icon = QLabel()
        cpu_icon.setPixmap(qta.icon("fa6s.microchip", color="#8a8d91").pixmap(QSize(16, 16)))
        config_layout.addWidget(cpu_icon)

        config_label = QLabel(config)
        config_label.setObjectName("ProjectCardConfig")
        config_label.setWordWrap(True)
        config_layout.addWidget(config_label, stretch=1)

        right_layout.addLayout(config_layout)

        # Низ: Цена + Кнопка
        footer_layout = QHBoxLayout()
        footer_layout.setSpacing(15)

        try:
            price_formatted = f"{int(price):,}₽".replace(",", " ")
        except Exception:
            price_formatted = str(price)

        price_layout = QHBoxLayout()
        price_layout.setSpacing(5)
        price_icon = QLabel()
        price_icon.setPixmap(qta.icon("fa6s.ruble-sign", color="#2e7d32").pixmap(QSize(18, 18)))
        price_layout.addWidget(price_icon)

        price_label = QLabel(price_formatted)
        price_label.setObjectName("ProjectCardPrice")
        price_layout.addWidget(price_label)

        footer_layout.addLayout(price_layout)
        footer_layout.addStretch()

        details_btn = QPushButton("Открыть")
        details_btn.setObjectName("ProjectCardButton")
        details_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        if not self.is_list_view:
            details_btn.setFixedSize(100, 34)
        details_btn.clicked.connect(
            lambda: self.open_project.emit(self.project_id)
        )
        footer_layout.addWidget(details_btn)

        right_layout.addLayout(footer_layout)

        if self.is_list_view:
            right_container = QWidget()
            right_container.setLayout(right_layout)
            right_container.setFixedWidth(350)
            main_layout.addWidget(right_container)
        else:
            main_layout.addLayout(right_layout)

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

        main_layout.addWidget(self._build_top_panel())
        main_layout.addWidget(self._build_control_panel())

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
        layout.setSpacing(15)

        self.search_input = QLineEdit()
        self.search_input.setObjectName("SearchInput")
        self.search_input.setPlaceholderText("🔍  Поиск по названию или описанию...")
        self.search_input.textChanged.connect(self._filter_projects)
        layout.addWidget(self.search_input, stretch=1)

        # Сортировка
        self.sort_combo = QComboBox()
        self.sort_combo.setObjectName("SortCombo")
        self.sort_combo.addItems([
            "Сначала новые",
            "Сначала старые",
            "По цене (дорогие)",
            "По цене (дешёвые)",
            "По названию (А-Я)",
        ])
        self.sort_combo.currentIndexChanged.connect(self._load_projects)
        layout.addWidget(self.sort_combo)

        # Переключатель вида
        self.grid_btn = QPushButton()
        self.grid_btn.setIcon(qta.icon("fa6s.grip", color="white"))
        self.grid_btn.setIconSize(QSize(18, 18))
        self.grid_btn.setObjectName("ViewButton")
        self.grid_btn.setCheckable(True)
        self.grid_btn.setChecked(True)
        self.grid_btn.setFixedSize(38, 38)
        self.grid_btn.setToolTip("Сетка")
        self.grid_btn.clicked.connect(lambda: self._switch_view("grid"))
        layout.addWidget(self.grid_btn)

        self.list_btn = QPushButton()
        self.list_btn.setIcon(qta.icon("fa6s.list", color="white"))
        self.list_btn.setIconSize(QSize(18, 18))
        self.list_btn.setObjectName("ViewButton")
        self.list_btn.setCheckable(True)
        self.list_btn.setFixedSize(38, 38)
        self.list_btn.setToolTip("Список")
        self.list_btn.clicked.connect(lambda: self._switch_view("list"))
        layout.addWidget(self.list_btn)

        return panel

    def _switch_view(self, view):
        self.current_view = view
        self.grid_btn.setChecked(view == "grid")
        self.list_btn.setChecked(view == "list")
        self._load_projects()

    def _filter_projects(self):
        self._load_projects()

    def _load_projects(self):
        # Безопасная очистка layout
        while self.projects_layout.count():
            item = self.projects_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                # Рекурсивная очистка вложенных layout (для grid)
                self._clear_layout(item.layout())

        projects = self.project_manager.get_all_projects()
        search_text = self.search_input.text().lower()

        # Фильтрация
        filtered = {
            pid: pdata for pid, pdata in projects.items()
            if search_text in pdata["name"].lower() or search_text in pdata["description"].lower()
        }

        # Сортировка
        sort_index = self.sort_combo.currentIndex()
        items = list(filtered.items())

        if sort_index == 0: items.sort(key=lambda x: int(x[0]), reverse=True)
        elif sort_index == 1: items.sort(key=lambda x: int(x[0]))
        elif sort_index == 2: items.sort(key=lambda x: int(x[1].get("price", 0)), reverse=True)
        elif sort_index == 3: items.sort(key=lambda x: int(x[1].get("price", 0)))
        elif sort_index == 4: items.sort(key=lambda x: x[1]["name"])

        if not items:
            empty_layout = QVBoxLayout()
            empty_layout.addStretch()

            empty_icon = QLabel()
            empty_icon.setPixmap(qta.icon("fa6s.folder-open", color="#3a3b3c").pixmap(QSize(64, 64)))
            empty_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_layout.addWidget(empty_icon)

            empty_label = QLabel("По вашему запросу ничего не найдено")
            empty_label.setObjectName("EmptyLabel")
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_layout.addWidget(empty_label)

            empty_layout.addStretch()
            self.projects_layout.addLayout(empty_layout)
            return

        if self.current_view == "grid":
            grid = QGridLayout()
            grid.setSpacing(20)
            grid.setColumnStretch(0, 1)
            grid.setColumnStretch(1, 1)
            grid.setColumnStretch(2, 1)

            for i, (pid, pdata) in enumerate(items):
                row = i // 3
                col = i % 3
                config = f"{pdata['config'].get('cpu', '—')}  •  {pdata['config'].get('gpu', '—')}"

                card = ProjectCardModern(pid, pdata["name"], pdata["description"], pdata["price"], config, is_list_view=False)
                card.open_project.connect(self.open_project.emit)
                grid.addWidget(card, row, col)

            self.projects_layout.addLayout(grid)
        else:
            for pid, pdata in items:
                config = f"""
                    {pdata['config'].get('cpu', '—')}  •  {pdata['config'].get('gpu', '—')}
                    """
                
                card = ProjectCardModern(pid, pdata["name"], pdata["description"], pdata["price"], config, is_list_view=True)
                card.open_project.connect(self.open_project.emit)
                self.projects_layout.addWidget(card)

    def _clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self._clear_layout(item.layout())

    def refresh(self):
        self._load_projects()
