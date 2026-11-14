from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QTextEdit,
    QPushButton, QMessageBox,
)
from PyQt6.QtCore import Qt


class CreateProjectDialog(QDialog):
    """Диалоговое окно для создания нового проекта"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Создание нового проекта")
        self.setFixedSize(450, 350)
        self.setObjectName("CreateProjectDialog")

        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        title_label = QLabel("Создайте свой новый проект")
        title_label.setObjectName("DialogTitle")
        title_label.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        )
        layout.addWidget(title_label)

        project_name_input = QLabel("Название проекта:")
        project_name_input.setObjectName("ProjectNameInputLabel")
        layout.addWidget(project_name_input)
        self.name_input = QLineEdit()
        self.name_input.setObjectName("DialogInput")
        self.name_input.setPlaceholderText("Например: Игровой ПК за 100к")
        layout.addWidget(self.name_input)

        project_desc_input = QLabel("Описание:")
        project_desc_input.setObjectName("ProjectDescInputLabel")
        layout.addWidget(project_desc_input)
        self.desc_input = QTextEdit()
        self.desc_input.setObjectName("DialogInput")
        self.desc_input.setPlaceholderText(
            "Краткое описание сборки и её назначение..."
        )
        self.desc_input.setMaximumHeight(80)
        layout.addWidget(self.desc_input)

        layout.addStretch()

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        cancel_btn = QPushButton("Отмена")
        cancel_btn.setObjectName("DialogButtonSecondary")
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.setFixedSize(100, 35)
        cancel_btn.clicked.connect(self.reject)

        continue_btn = QPushButton("Продолжить")
        continue_btn.setObjectName("DialogButtonPrimary")
        continue_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        continue_btn.setFixedSize(120, 35)
        continue_btn.clicked.connect(self.validate_and_accept)

        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(continue_btn)
        layout.addLayout(btn_layout)

    def validate_and_accept(self):
        name = self.name_input.text().strip()

        if not name:
            QMessageBox.warning(
                self, "Ошибка", "Название проекта не может быть пустым!"
            )
            self.name_input.setFocus()
            return

        self.accept()

    def get_data(self):
        return {
            "name": self.name_input.text().strip(),
            "description": (
                self.desc_input.toPlainText().strip() or "Описание отсутствует"
            ),
        }
