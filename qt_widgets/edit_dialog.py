from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel,
    QTextEdit, QPushButton,
)
from PyQt6.QtCore import Qt


class EditDialog(QDialog):
    """Универсальный диалог для редактирования текста"""

    def __init__(self, title, label_text, initial_text="", parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(500, 300)
        self.setObjectName("EditDialog")

        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        title_label = QLabel(title)
        title_label.setObjectName("EditDialogLabel")
        layout.addWidget(title_label)

        desc_label = QLabel(label_text)
        desc_label.setObjectName("DialogLabel")
        layout.addWidget(desc_label)

        self.text_edit = QTextEdit()
        self.text_edit.setObjectName("EditDialogTextEdit")
        self.text_edit.setPlainText(initial_text)
        layout.addWidget(self.text_edit)

        btn_layout = QVBoxLayout()
        btn_layout.addStretch()

        save_btn = QPushButton("Сохранить")
        save_btn.setObjectName("EditDialogButton")
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.setFixedSize(120, 35)
        save_btn.clicked.connect(self.accept)

        btn_layout.addWidget(save_btn, alignment=Qt.AlignmentFlag.AlignRight)
        layout.addLayout(btn_layout)

    def get_text(self):
        return self.text_edit.toPlainText().strip()
