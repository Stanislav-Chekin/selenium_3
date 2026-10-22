# 🧪 Selenium UI Tests - Lesson_3

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.14-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Selenium-4.x-43B02A?style=for-the-badge&logo=selenium&logoColor=white" alt="Selenium">
  <img src="https://img.shields.io/badge/pytest-9.1-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white" alt="Pytest">
  <img src="https://img.shields.io/badge/Unittest-Built--in-yellow?style=for-the-badge" alt="Unittest">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/status-completed-success?style=flat-square" alt="Status">
  <img src="https://img.shields.io/badge/waits-Explicit%20%7C%20Implicit-blueviolet?style=flat-square" alt="Waits">
  <img src="https://img.shields.io/badge/DDT-Parameterized-orange?style=flat-square" alt="DDT">
</p>

---

## 📖 О проекте

Домашнее задание по автоматизации тестирования веб-форм с использованием **Selenium WebDriver**.
В рамках работы были изучены и применены на практике различные типы ожиданий, методы работы с динамическим контентом (SPA) и сложными веб-элементами.

**Протестированные формы (AUT):**
- 🔐 [Login Form](https://qa-guru.github.io/one-page-form/login.html)
- 📝 [Text Box Form](https://qa-guru.github.io/one-page-form/text-box.html)
- 🎓 [Student Registration Form](https://qa-guru.github.io/one-page-form/automation-practice-form.html)
- 📊 [Tables](https://the-internet.herokuapp.com/tables)

---

## 🛠️ Реализованные сценарии и технологии

### 1. Ожидания (Waits)
- **Implicit Waits** (`driver.implicitly_wait`) — глобальные неявные ожидания.
- **Explicit Waits** (`WebDriverWait` + `expected_conditions`) — ожидание конкретных условий (видимость, кликабельность, исчезновение элемента).
- **Fluent Wait** — гибкая настройка частоты опроса и игнорируемых исключений.

### 2. Обработка динамического контента (React / SPA)
- Использование `driver.execute_script()` для скролла страницы и кликов в обход перекрывающих элементов (баннеров и футеров).
- Удаление перекрывающих элементов из DOM-дерева перед взаимодействием.

### 3. Сложные Web-элементы
- **Радиокнопки и чекбоксы** — клики по связанным `<label>` (так как сами `<input>` скрыты).
- **Календарь (Datepicker)** — комплексная работа с выпадающими списками месяцев/годов и выбором конкретного дня.
- **Кастомные Dropdowns (React-Select)** — взаимодействие с нестандартными выпадающими списками (State, City).
- **Загрузка файлов** — создание временного файла через `os` и отправка его в `input[type='file']`.
- **Таблицы** — реализация паттерна `Page Element` для извлечения заголовков и данных ячеек.

### 4. Подходы к тестированию
- **DDT (Data-Driven Testing)** — параметризация тестов в Pytest с использованием `@pytest.mark.parametrize`.
- **Позитивные и негативные сценарии** — проверка успешного входа и обработка ошибок (неверный пароль, пустые поля, SQL-инъекции).
- Тестирование с использованием `unittest` (классы, `setUp`, `tearDown`) и `pytest` (фикстуры).

---

## 📂 Структура проекта

| Файл | Описание |
| :--- | :--- |
| `the_simplest_test_login.py` | Линейный скрипт: явные и неявные ожидания при логине. |
| `test_login.py` | Pytest-тесты логина с DDT (позитив, негатив, пустые поля, инъекции). |
| `simple_test_student_registration_form.py` | Unittest-тесты формы регистрации (заполнение всех полей + негативный тест). |
| `table_page_element_example.py` | Работа с таблицами через паттерн Page Element. |

---

