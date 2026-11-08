# 🖥️ Конфигуратор сборок PC Builder

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![PyQt6](https://img.shields.io/badge/UI-PyQt6-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

[Русский](#-о-проекте) | [English](#️-assembly-configurator-pcbuilder)


## 📌 Навигация по README.md:

- [📖 О проекте](#-о-проекте)
- [✨ Возможности](#-возможности)
- [📸 Скриншоты](#-скриншоты)
- [🛠️ Стек технологий](#️-стек-технологий)
- [🚀 Установка и запуск](#-установка-и-запуск)

## 📖 О проекте

**PCBuilder** - Современное кроссплатформенное десктопное приложение для просмотра, управления и экспорта конфигураций сборок ПК. Разработано на **Python** с использованием фреймворка **PyQt6**.

Приложение отличается чистым кодом, модульной архитектурой, тёмной темой оформления и удобными горячими клавишами.

---

## ✨ Возможности

- 📋 **Каталог сборок**: Удобный список проектов с краткой информацией и прокруткой.
- 🔍 **Детальный просмотр**: Полная информация о конфигурации (CPU, GPU, RAM, SSD, корпус, охлаждение, БП) и стоимости.
- 💾 **Экспорт данных**: Сохранение конфигурации проекта в форматы **CSV**, **TXT** или **PDF**.
- ✏️ **Редактирование**: Встроенный кастомный диалог для изменения описания и конфигурации с валидацией.
- ⌨️ **Горячие клавиши**: 
  - `Ctrl + Enter` или `Ctrl + S` — сохранить изменения в диалоге.
  - `Esc` — закрыть диалог без сохранения.
- 🎨 **Современный UI**: Тёмная тема, кастомные шрифты (*Nunito* для интерфейса, *JetBrains Mono* для технических данных) и векторные иконки через `QtAwesome`.
- ⚡ **Быстрая работа**: Использование `ProjectManager` с кэшированием данных в памяти для мгновенного доступа к `projects.json`.

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

---

## 🚀 Установка и запуск

1. **Склонируйте репозиторий**:
   ```bash
   git clone https://github.com/tylerderden9681-wq/PcBuilder.git
   cd PcBuilder

2. **Создайте виртуальное окружение**:

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

3. **Установите зависимости**:

   Для работы проекта нужно установить зависимости, находящиеся в файле `requirements.txt`, так что воспользуйтесь командой:

   ```bash
   pip install -r requirements.txt
   ```

4. **Запустите проект**:

   Чтобы запустить проект, воспользуйтесь командой:
   ```bash
   python main.py
   ```



## 🖥️ Assembly Configurator PcBuilder

## 📖 About Project

**PCBuilder** - A modern cross‑platform desktop application for viewing, managing, and exporting PC build configurations. Developed in **Python** using the **PyQt6** framework.

The application is characterized by clean code (the code was written using the `flake8` and `black` linters), a modular architecture, a dark theme, and convenient hotkeys.

---

## ✨ Features

- 📋 **Assembly catalog**: a convenient list of projects with brief information and scrolling.
- 🔍 **Detailed overview**: Full information about the configuration (CPU, GPU, RAM, SSD, case, cooling, power supply) and the cost.
- 💾 **Data export**: Saving the project configuration in **CSV**, **TXT**, or **PDF** formats.
- ✏️ **Editing**: Built-in custom dialog for modifying the description and configuration with validation.
- ⌨️ **Hotkeys**: 
  - `Ctrl + Enter` or `Ctrl + S` — save changes in the dialog.
  - `Esc` — close the dialog without saving.
- 🎨 **Modern UI**: Dark theme, custom fonts (*Nunito* for the interface, *JetBrains Mono* for technical data) and vector icons via `QtAwesome`.
- ⚡ **Fast operation**: Using `ProjectManager` with in‑memory data caching for instant access to `projects.json`.

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

- **Main Language**: Python 3.10+
- **GUI**: PyQt6
- **Icons**: QtAwesome
- **Data Storage**: JSON (with caching data)

---

## 🚀 Installing and launch project

1. **Clone the repository**:
   ```bash
   git clone https://github.com/tylerderden9681-wq/PcBuilder.git
   cd PcBuilder

2. **Create a virtual environment**:

   *Note*: the commands differ slightly across different operating systems, so use the commands that are applicable to your specific operating system and terminal:

   **Linux/MacOS**:
   ```bash
   source venv/bin/activate
   ```

   **Windows**:

   In Windows, things aren’t that simple, as the commands differ slightly for different terminals and look like this:

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

3. **Install the dependencies**:

   To run the project, you need to install the dependencies listed in the `requirements.txt` file, so use the following command:

   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the project**:

   To launch the project, use the command:
   ```bash
   python main.py
   ```

