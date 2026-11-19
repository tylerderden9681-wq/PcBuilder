# 🖥️ Конфигуратор сборок PC Builder

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![PyQt6](https://img.shields.io/badge/UI-PyQt6-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

[Русский](#-о-проекте) | [English](#️-assembly-configurator-pcbuilder)


## 📌 Навигация по README.md:

- 📖 [О проекте](#-о-проекте)
- ✨ [Возможности](#-возможности)
- 📸 [Скриншоты](#-скриншоты)
- 🛠️ [Стек технологий](#️-стек-технологий)
- 🚀 [Установка и запуск](#-установка-и-запуск)

## 📖 О проекте

**PCBuilder** - Современное кроссплатформенное десктопное приложение для просмотра, управления и экспорта конфигураций сборок ПК. Разработано на **Python** с использованием фреймворка **PyQt6**.

Приложение отличается чистым кодом, модульной архитектурой, тёмной темой оформления и удобными горячими клавишами.

---

## ✨ Возможности

### Ключевые возможности PCBuilder:

- 📊 **Дашборд** со статистикой, быстрым доступом и ссылками на магазины
- 📁 **Каталог проектов** с поиском, сортировкой и двумя режимами отображения
- ⚙️ **Конфигуратор** с 8 категориями комплектующих и поиском
- 🔍 **Проверка совместимости** в реальном времени (сокеты, память, БП, корпус)
- ✏️ **Inline-редактирование** названия и удаление проекта
- 📤 **Экспорт** конфигурации в CSV и TXT
- ⌨️ **Горячие клавиши** для быстрого сохранения и навигации
- 🎨 **Современный UI**: тёмная тема, кастомные шрифты, адаптивная сетка

---

## 📸 Скриншоты

| Дашборд | Конфигуратор | Страница проекта |
|---------|--------------|------------------|
| ![Дашборд](screenshots/dashboard_page.png) | ![Конфигуратор](screenshots/config_dialog.png) | ![Проект](screenshots/project_page.png) |

| Характеристики комплектующих | Все проекты |
| ----------------- | ----------------- |
| ![Характеристика комплектующего](screenshots/info_dependence.png) | ![Все проекты](screenshots/all_projects_page.png) |


---

## 🛠️ Стек технологий

- **Язык**: Python 3.10+
- **GUI**: PyQt6
- **Иконки**: QtAwesome
- **Хранение данных**:
   - **О проектах пользователей** - в JSON, который создается для каждого пользователя лично
   - **Все комплектующие** - в БД SQLite локально в папке приложения
- **Линтеры**: black и flake8

### Технологии и виджеты из PyQt6

| Виджет | Применение в проекте |
|:---|:---|
| `QMainWindow` | Главное окно приложения |
| `QWidget` | Базовый контейнер для страниц и кастомных виджетов |
| `QFrame` | Основа для стилизованных карточек (проектов, компонентов, статистики) |
| `QLabel` | Отображение текста, иконок и градиентного логотипа |
| `QPushButton` | Кнопки действий, переключатели вида, экспорт |
| `QLineEdit` | Поля поиска с иконкой и ввода данных в формах |
| `QTextEdit` | Многострочное поле для описания проекта |
| `QComboBox` | Выпадающий список для сортировки проектов |
| `QScrollArea` | Прокрутка списков проектов и длинных страниц |
| `QTabWidget` | Вкладки в конфигураторе комплектующих |
| `QListWidget` / `QListWidgetItem` | Списки компонентов с кастомными виджетами внутри |
| `QSplitter` | Разделитель колонок на дашборде |
| `QStackedWidget` | Переключение между страницами (дашборд, каталог, проект) |
| `QDialog` | Модальные окна (конфигуратор, детали компонента) |
| `QMessageBox` | Уведомления, предупреждения и подтверждения действий |
| `QFileDialog` | Нативное окно выбора пути для экспорта CSV/TXT |

---

## 🚀 Установка и запуск

### 1. Инструкция для запуска стабильной версии приложения (ветка main):

1. <a id="clone-main"></a> **Склонируйте репозиторий**:
   ```bash
   git clone https://github.com/tylerderden9681-wq/PcBuilder.git
   cd PcBuilder
   ```

2. <a id="create-venv"></a> **Создайте виртуальное окружение**:

   **Для пользователей Linux/MacOS**:
   ```bash
   python3 -m venv venv
   ```

   **Для пользователей Windows с `установленным Python`**:
   ```bash
   python -m venv venv
   ```

   **Для пользователей Windows без установленного Python**:
   ```bash
   py -3.12 -m venv venv
   ```

   *P.S.*: вместо версии python 3.12 вы можете установить любую версию не ниже 3.10

3. <a id="activate-venv"></a>**Активируйте виртуальное окружение**:

   *Примечание*: на разных OC команды немного отличаются, так что используйте команды, применимые именно для вашей OC и вашего терминала:

   **Linux/MacOS**:
   ```bash
   source venv/bin/activate
   ```

   **Windows**:

   В Windows не так всё просто, так как для разных терминалов команды немного отличаются и выглядят следующим образом:

   **CMD**:
   ```bash
   venv\Scripts\activate
   ```

   **PowerShell**:
   ```bash
   venv\Scripts\Activate.ps1
   ```

   **Git Bash / MINGW**:
   ```bash
   source venv/Scripts/activate
   ```

4. **Установите зависимости для `продового` режима**:

   Для работы проекта нужно установить зависимости, находящиеся в файле `requirements/prod.txt`, так что воспользуйтесь командой:

   ```bash
   pip install -r requirements/prod.txt
   ```

5. **Запустите проект**:

   Чтобы запустить проект, воспользуйтесь командой:
   ```bash
   python main.py
   ```

### 2. Инструкция для разработчиков и контрибьюторов (ветка dev):

1. **Склонируйте ветку dev командой и перейдите в склонированную директорию**:

   ```bash
   git clone --branch dev https://github.com/tylerderden9681-wq/PcBuilder.git
   cd PcBulder
   ```

2. **Проделайте шаги по [созданию](#create-venv) и [активации](#activate-venv) виртуального окружения**

3. **Установите зависимости для разработки (с линтерами flake8 и black):**

   В режиме разработки предпочтительно установить зависимости из `requirements/dev.txt`, где находятся линтеры для грамотного и понятного написания кода:

   ```bash
   pip install -r requirements/dev.txt
   ```



## 🖥️ Assembly Configurator PcBuilder

## 📌 Navigation of README.md:

- 📖 [About Project](#-about-project)
- ✨ [Features](#-features)
- 📸 [Screenshots](#-screenshots)
- 🛠️ [Technologies stack](#️-used-technologies)
- 🚀 [Installation and launching](#-installing-and-launch-project)

## 📖 About Project

**PCBuilder** - A modern cross‑platform desktop application for viewing, managing, and exporting PC build configurations. Developed in **Python** using the **PyQt6** framework.

The application is characterized by clean code (the code was written using the `flake8` and `black` linters), a modular architecture, a dark theme, and convenient hotkeys.

---

## ✨ Features

### Main Features of PCBuilder:

- 📊 **Dashboard** with statistics, quick access, and links to stores
- 📁 **Projects List** with search, sorting, and two display modes
- ⚙️ **Configurator** with 8 categories of components and search
- 🔍 **Real-time compatibility check** (sockets, memory, power supply, case)
- ✏️ **Inline editing** of the project name and deletion of the project
- 📤 **Export** of configurations to CSV and TXT
- ⌨️ **HotKeys** for quick saving and navigation
- 🎨 **Modern UI**: dark theme, custom fonts, adaptive grid

---

## 📸 Screenshots

| Dashboard | Configurator | Project Page |
|---------|--------------|------------------|
| ![Dashboard](screenshots/dashboard_page.png) | ![Configurator](screenshots/config_dialog.png) | ![Project](screenshots/project_page.png) |

| Component specifications | All Projects |
| ----------------- | ----------------- |
| ![Component specifications](screenshots/info_dependence.png) | ![All Projects](screenshots/all_projects_page.png) |

---

## 🛠️ Used technologies

- **Programming Language**: Python 3.10+
- **GUI**: PyQt6
- **Icons**: QtAwesome
- **Data Storage**:
   - **About Users Projects** - in the JSON that is created locally for each user
   - **All Dependencies** - in the database locally in the application folder
- **Linters**: black and flake8

### Technologies and widgets from PyQt6

| Widget | Usage in the project |
|:---|:---|
| `QMainWindow` | Main application window |
| `QWidget` | Base container for pages and custom widgets |
| `QFrame` | Base for styled cards (projects, components, statistics) |
| `QLabel` | Displaying text, icons, and gradient logo |
| `QPushButton` | Action buttons, view toggles, export |
| `QLineEdit` | Search fields with icon and form data input |
| `QTextEdit` | Multi-line field for project description |
| `QComboBox` | Dropdown list for project sorting |
| `QScrollArea` | Scrolling for project lists and long pages |
| `QTabWidget` | Tabs in the component configurator |
| `QListWidget` / `QListWidgetItem` | Component lists with custom widgets inside |
| `QSplitter` | Column divider on the dashboard |
| `QStackedWidget` | Switching between pages (dashboard, catalog, project) |
| `QDialog` | Modal windows (configurator, component details) |
| `QMessageBox` | Notifications, warnings, and action confirmations |
| `QFileDialog` | Native path selection dialog for CSV/TXT export |

---

## 🚀 Installation and launch

### 1. Instructions for launching the stable version of the application (main branch):

1. <a id="clone-main"></a> **Clone the repository**:
   ```bash
   git clone https://github.com/tylerderden9681-wq/PcBuilder.git
   cd PcBuilder
   ```

2. <a id="create-venv-en"></a> **Create a virtual environment**:

   **For Linux/MacOS users**:
   ```bash
   python3 -m venv venv
   ```

   **For Windows users with `Python installed`**:
   ```bash
   python -m venv venv
   ```

   **For Windows users without Python installed**:
   ```bash
   py -3.12 -m venv venv
   ```

   *P.S.*: instead of Python version 3.12, you can install any version no lower than 3.10.

3. <a id="activate-venv-en"></a>**Activate the virtual environment**:

   *Note*: the commands differ slightly depending on the OS, so use the commands that are applicable to your OS and your terminal:

   **Linux/MacOS**:
   ```bash
   source venv/bin/activate
   ```

   **Windows**:

   In Windows, not It’s that simple, since the commands differ slightly for different terminals and look like this:

   **CMD**:
   ```bash
   venv\Scripts\activate
   ```

   **PowerShell**:
   ```bash
   venv\Scripts\Activate.ps1
   ```

   **Git Bash / MINGW**:
   ```bash
   source venv/Scripts/activate
   ```

4. **Install dependencies for `prod` mode**:

   For the project to work, you need to install the dependencies listed in the `requirements/prod.txt` file, so use the following command:

   ```bash
   pip install -r requirements/prod.txt
   ```

5. **Run the project**:

   To run the project, use the following command:
   ```bash
   python main.py
   ```

### 2. Instructions for developers and contributors (dev branch):

1. **Clone the `dev` branch using the command and navigate to the cloned directory**:

   ```bash
   git clone --branch dev https://github.com/tylerderden9681-wq/PcBuilder.git
   cd PcBuilder
   ```

2. **Follow the steps to [create](#create-venv-en) and [activate](#activate-venv-en) the virtual environment.**

3. **Install development dependencies (with flake8 and black linters):**

   In development mode, it is preferable to install dependencies from `requirements/dev.txt`, which contain linters for writing clean and understandable code:

   ```bash
   pip install -r requirements/dev.txt
   ```
