# styles.py


def get_stylesheet(nunito_family: str = "", jetbrains_family: str = "") -> str:
    """
    Возвращает полный CSS-стиль для приложения с учетом загруженных шрифтов.
    """

    base_styles = """
        QMainWindow { background-color: #18191a; }

        /* ===== Дашборд ===== */
        QWidget#DashboardPage { background-color: #18191a; }

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

        QLabel#WelcomeDesc { color: #b0b3b8; font-size: 16px; }

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

        QLabel#StatTitle { color: #8a8d91; font-size: 12px; }
        QLabel#StatValue {
            color: white;
            font-size: 18px;
            font-weight: bold;
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
        QPushButton#ActionButton:hover { background-color: #005a9e; }

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

        QLabel#MiniProjectPrice { color: #4dc8ff; font-size: 13px; }
        QLabel#EmptyProjectsLabel {
            color: #8a8d91;
            font-size: 14px;
            font-style: italic;
            padding: 20px;
        }

        /* ===== Страница проекта ===== */
        #ProjectPage { background-color: #18191a; }
        #ProjectScroll, #ProjectContent { background-color: transparent; }

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

        #ProjectPageTitle { font-size: 20px; font-weight: 700; color: white; }

        QFrame#InfoBlock {
            background-color: white;
            border: 1px solid #3a3b3c;
            padding: 15px;
            border-radius: 10px;
        }

        QFrame#PriceBlock {
            background-color: white;
            border: 3px solid #2e7d32;
            padding: 8px 15px;
            border-radius: 10px;
        }

        #BlockHeader, #PriceBlockHeader { font-size: 20px; font-weight: bold; }
        #BlockHeader { color: #0078d7; }
        #PriceBlockHeader { color: green; }
        #BlockText { color: black; font-size: 14px; line-height: 1.5; }
        #BigPrice { color: green; font-size: 22px; font-weight: bold; }

        QPushButton#EditButton, QPushButton#DeleteButton {
            background-color: transparent;
            border: none;
            border-radius: 15px;
            padding: 4px;
        }

        QPushButton#EditButton:hover {
            background-color: rgba(0, 120, 215, 0.2);
        }

        QPushButton#DeleteButton:hover {
            background-color: rgba(252, 28, 3, 0.2);
        }

        /* ===== Диалоги ===== */
        QDialog#EditDialog,
        QDialog#ConfigDialog,
        QDialog#ComponentDetailDialog {
            background-color: #18191a;
        }

        QLabel#EditDialogLabel,
        QLabel#ConfigDialogTitle,
        QLabel#DetailName {
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

        QLabel#ProjectNameInputLabel, QLabel#ProjectDescInputLabel {
            font-size: 16px;
            font-weight: 700;
        }

        QLabel#DialogTitle {
            color: white;
            padding: 4px 12px;
            font-weight: 700;
            font-size: 20px;
            border-radius: 6px;
        }
        QLabel#DialogLabel { font-weight: 600; font-size: 14px; }

        QLineEdit#DialogInput, QTextEdit#DialogInput, QComboBox#DialogInput {
            background-color: #242526;
            color: white;
            border: 1px solid #3a3b3c;
            border-radius: 6px;
            padding: 6px 10px;
            font-size: 13px;
        }

        QLineEdit#DialogInput:focus,
        QTextEdit#DialogInput:focus,
        QComboBox#DialogInput:focus { border: 1px solid #0078d7; }
        QTextEdit#EditDialogTextEdit {
            background-color: #242526;
            color: white;
            border: 1px solid #3a3b3c;
            border-radius: 8px;
            padding: 10px;
            font-size: 14px;
        }
        QTextEdit#EditDialogTextEdit:focus { border: 1px solid #0078d7; }

        #DialogButtonPrimary, #DialogButtonSecondary {
            color: white;
            background-color: transparent;
            border: 2px solid white;
            border-radius: 6px;
        }

        #DialogButtonSecondary:hover, #DialogButtonPrimary:hover {
            background-color: rgba(252, 252, 252, 0.2);
        }

        QComboBox#DialogInput::drop-down { border: none; width: 20px; }
        QComboBox#DialogInput::down-arrow {
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

        /* ===== Конфигуратор ===== */
        #ConfigDialogScroll, #ConfigDialogFields {
            background-color: transparent;
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
            margin-right: 2px;
            font-size: 12px;
            font-weight: 600;
        }

        QTabBar::tab:selected {
            background-color: #242526;
            color: white;
            border-bottom: 2px solid #0078d7;
        }

        QTabBar::tab:hover { background-color: #2d2d2d; color: white; }
        QWidget#ConfigTab { background-color: #242526; }

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
        QLineEdit#ConfigSearchInput:focus { border: 2px solid #0078d7; }

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

        QWidget#ComponentItem { background-color: transparent; }
        QLabel#ComponentName {
            color: white;
            font-size: 13px;
            font-weight: 600;
        }

        QLabel#ComponentSpecs { color: #888; font-size: 11px; }
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
        }

        QFrame#DetailHeader {
            background-color: #242526;
            border: 1px solid #3a3b3c;
            border-radius: 12px;
        }

        QLabel#DetailPrice {
            color: #4dc8ff;
            font-size: 20px;
            font-weight: bold;
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

        QFrame#DetailFieldRow:hover { background-color: #2d2f31; }

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

        QPushButton#DetailButtonPrimary:hover { background-color: #005a9e; }
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

        QPushButton#FooterLink:hover { background-color: #2d2f31; }
        QLabel#FooterLinkText { color: white; font-size: 12px; }
        QPushButton#FooterLink:hover QLabel#FooterLinkText { color: #0078d7; }

        QFrame#FooterLink {
            background-color: transparent;
            border-radius: 6px;
            border: 2px solid #3a3b3c;
        }

        QFrame#FooterLink:hover { background-color: #2d2f31; }
        QFrame#FooterLink:hover QLabel#FooterLinkText { color: #747474; }

        QLabel#FooterVersion {
            color: #4dc8ff;
            font-size: 12px;
            font-weight: bold;
        }

        QLabel#FooterAuthor, QLabel#FooterYear {
            color: #8a8d91;
            font-size: 12px;
            font-weight: 600;
        }

        QLabel#FooterDot { color: #3a3b3c; font-size: 12px; }

        /* ===== Страница всех проектов ===== */
        QWidget#ProjectsListPage { background-color: #18191a; }
        QLabel#PageTitle { color: white; font-size: 24px; font-weight: bold; }

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
            margin-top: 10px;
        }

        #ProjectsScroll, #ProjectsContent { background-color: transparent; }


        /* ===== Панель управления (Поиск, Сортировка, Вид) ===== */
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
            border-radius: 8px;
            padding: 10px 15px;
            font-size: 14px;
            selection-background-color: #0078d7;
        }

        QLineEdit#SearchInput:focus {
            border: 1px solid #0078d7;
            background-color: #242526;
        }

        QComboBox#SortCombo {
            background-color: #1e1f20;
            color: white;
            border: 1px solid #3a3b3c;
            border-radius: 8px;
            padding: 8px 12px;
            font-size: 13px;
            min-width: 160px;
        }

        QPushButton#ViewButton {
            background-color: #1e1f20;
            border: 1px solid #3a3b3c;
            border-radius: 8px;
        }

        QPushButton#ViewButton:checked {
            background-color: #0078d7;
            border: 1px solid #005a9e;
        }

        QPushButton#ViewButton:hover { background-color: #2d2f31; }

        /* ===== Адаптивная карточка проекта ===== */
        QFrame#ProjectCardModern {
            background-color: #242526;
            border: 1px solid #3a3b3c;
            border-radius: 12px;
        }

        QFrame#ProjectCardModern:hover {
            border: 1px solid #0078d7;
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

        QLabel#ProjectCardConfig { color: #8a8d91; font-size: 12px; }
        QLabel#ProjectCardPrice {
            color: #2e7d32;
            font-size: 18px;
            font-weight: bold;
        }

        QPushButton#ProjectCardButton {
            background-color: #0078d7;
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            font-size: 13px;
            padding: 10px 6px;
        }

        QPushButton#ProjectCardButton:hover { background-color: #005a9e; }

        /* ===== Страница информации ===== */
        QWidget#InfoPage { background-color: #18191a; }
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

        QPushButton#FooterInfoButton:hover { background-color: #2d2f31; }
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

        QPushButton#ExportButton:pressed { background-color: #1e1f20; }

        /* ===== Скроллбар для списка проектов ===== */
        QScrollArea#ProjectsScroll > QWidget > QScrollBar:vertical {
            background-color: #18191a; width: 10px; border-radius: 5px;
        }
        QScrollArea#ProjectsScroll > QWidget > QScrollBar::handle:vertical {
            background-color: #3a3b3c; border-radius: 5px; min-height: 30px;
        }
        QScrollArea#ProjectsScroll > QWidget >
        QScrollBar::handle:vertical:hover {
            background-color: #0078d7;
        }

        /* ===== Панель совместимости ===== */
        QFrame#CompatibilityPanel {
            background-color: #2a1f1f;
            border: 2px solid #dc3545;
            margin: 10px 0;
        }

        QLabel#CompatibilityHeader[status="error"] {
            color: #dc3545;
            font-size: 15px;
            font-weight: bold;
        }

        QLabel#CompatibilityHeader[status="warning"] {
            color: #ff9800;
            font-size: 15px;
            font-weight: bold;
        }

        QFrame#IssueError {
            background-color: rgba(220, 53, 69, 0.1);
            border: 1px solid #dc3545;
        }

        QFrame#IssueWarning {
            background-color: rgba(255, 152, 0, 0.1);
            border: 1px solid #ff9800;
        }

        QLabel#IssueText {
            color: white;
            font-size: 13px;
            padding: 2px 0;
        }

        /* ===== Состояние кнопки сохранения ===== */
        QPushButton#SaveButton:disabled {
            background-color: #3a3b3c;
            color: #8a8d91;
            border: 1px solid #2d2f31;
        }

        QPushButton#SaveButton:disabled:hover {
            background-color: #3a3b3c;
            cursor: default;
        }

        /* ===== Страница справки ===== */
        QWidget#HelpPage {
            background-color: #18191a;
        }

        QFrame#HelpTocFrame {
            background-color: #242526;
            border: 1px solid #3a3b3c;
            border-radius: 10px;
            margin-right: 15px;
        }

        QLabel#HelpTocTitle {
            color: white;
            font-size: 16px;
            font-weight: bold;
            padding-bottom: 10px;
            border-bottom: 1px solid #3a3b3c;
            margin-bottom: 10px;
        }

        QPushButton#HelpTocButton {
            background-color: transparent;
            color: #b0b3b8;
            border: none;
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 13px;
            text-align: left;
        }

        QPushButton#HelpTocButton:hover {
            background-color: #2d2f31;
            color: #0078d7;
        }

        QPushButton#HelpTocButton:pressed {
            background-color: #1e1f20;
        }

        QTextBrowser#HelpTextBrowser {
            background-color: #242526;
            color: #e0e0e0;
            border: 1px solid #3a3b3c;
            border-radius: 10px;
            padding: 20px;
            font-size: 14px;
            line-height: 1.7;
        }

        QTextBrowser#HelpTextBrowser a {
            color: #0078d7;
            text-decoration: none;
        }

        QTextBrowser#HelpTextBrowser a:hover {
            color: #4dc8ff;
            text-decoration: underline;
        }

        /* Приветственный диалог */
        QFrame#WelcomeDialog {
            background-color: #242526;
            border: 2px solid #0078d7;
            border-radius: 12px;
            max-width: 500px;
        }

        QLabel#WelcomeDialogTitle {
            color: white;
            font-size: 22px;
            font-weight: bold;
            padding: 10px 0;
        }

        QLabel#WelcomeDialogPoint {
            color: #b0b3b8;
            font-size: 14px;
            padding: 8px 0;
        }

        QPushButton#DontShowButton {
            background-color: transparent;
            color: #8a8d91;
            border: 1px solid #3a3b3c;
            border-radius: 6px;
            padding: 8px;
            font-size: 13px;
        }

        QPushButton#DontShowButton:checked {
            background-color: #0078d7;
            color: white;
            border: 1px solid #005a9e;
        }

        /* Выбранный компонент в списке */
        QListWidget#ComponentList::item:selected {
            background-color: rgba(0, 120, 215, 0.2);
            border: 2px solid #0078d7;
        }

        QListWidget#ComponentList::item:selected QLabel#ComponentName {
            color: #0078d7;
            font-weight: bold;
        }

        /* ===== Редактируемый заголовок проекта ===== */
        QLineEdit#ProjectTitleEdit {
            background-color: #242526;
            color: white;
            border: 2px solid #0078d7;
            border-radius: 8px;
            padding: 8px 14px;
            font-size: 22px;
            font-weight: 700;
        }

        QLineEdit#ProjectTitleEdit:focus {
            border: 2px solid #4dc8ff;
            background-color: #2d2f31;
        }

        QPushButton#TitleEditButton {
            background-color: transparent;
            border: 1px solid #3a3b3c;
            border-radius: 8px;
        }

        QPushButton#TitleEditButton:hover {
            background-color: #2d2f31;
            border: 1px solid #0078d7;
        }

        /* ===== Кнопка удаления проекта ===== */
        QPushButton#DeleteProjectButton {
            background-color: #dc3545;
            border: none;
            border-radius: 8px;
        }

        QPushButton#DeleteProjectButton:hover {
            background-color: #c82333;
        }

        QPushButton#DeleteProjectButton:pressed {
            background-color: #bd2130;
        }
    """

    # Динамическое добавление шрифтов
    if nunito_family:
        base_styles += f"""
            * {{
                font-family: '{nunito_family}';
                font-size: 13px;
            }}
        """

    if jetbrains_family:
        base_styles += f"""
            #BlockText, #BigPrice, #ProjectConfig, #ProjectTitle,
            #DetailsLink, #ProjectPageTitle, #BlockHeader,
            #PriceBlockHeader, #StatValue, #MiniProjectPrice,
            #TotalPriceLabel, #TabTotalPriceLabel, #ConfigRowPrice,
            #DetailPrice, QLabel#ProjectCardPrice, QLabel#ComponentCardPrice {{
                font-family: '{jetbrains_family}';
            }}
        """

    return base_styles
