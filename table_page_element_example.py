import time
from selenium import webdriver
from selenium.webdriver.common.by import By


# TODO: 4) Переписать используя PageFactory (Lesson 5) - Оставляем на будущее.

class TableElement:
    def __init__(self, driver, locator):
        self.driver = driver
        self.locator = locator

    @property
    def element(self):
        return self.driver.find_element(*self.locator)

    def get_headers(self) -> list[str]:
        """Возвращает список заголовков таблицы."""
        header_elements = self.element.find_elements(By.CSS_SELECTOR, "thead th")
        return [header.text for header in header_elements]

    def get_row_data(self, row_index: int) -> list[str]:
        """Возвращает данные конкретной строки по её индексу (начиная с 0)."""
        rows = self.element.find_elements(By.CSS_SELECTOR, "tbody tr")
        cells = rows[row_index].find_elements(By.TAG_NAME, "td")
        return [cell.text for cell in cells]

    def get_cell_value(self, row_index: int, column_index: int) -> str:
        """Возвращает значение конкретной ячейки."""
        # TODO: 1) РЕШЕНО: Переписали через вызов get_row_data
        row_data = self.get_row_data(row_index)
        return row_data[column_index]


# 2. Пример использования (Скрипт теста)
if __name__ == "__main__":
    # Инициализация драйвера
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(5)

    try:
        # Открытие страницы
        driver.get("https://the-internet.herokuapp.com/tables")

        # Инициализация ПЕРВОЙ таблицы
        table1_locator = (By.ID, "table1")
        table1 = TableElement(driver, table1_locator)

        # TODO: 2) РЕШЕНО: Добавили работу со ВТОРОЙ таблицей
        table2_locator = (By.ID, "table2")
        table2 = TableElement(driver, table2_locator)

        # === ТЕСТ 1: Работа только с первой таблицей (как было) ===
        print("--- Тест 1: Проверка Table 1 ---")
        headers1 = table1.get_headers()
        first_row1 = table1.get_row_data(0)
        specific_cell1 = table1.get_cell_value(row_index=2, column_index=3)  # Строка 3, Колонка 4 (Due)

        assert "Last Name" in headers1, "Заголовок 'Last Name' не найден"
        assert "Smith" in first_row1, "Фамилия 'Smith' должна быть в первой строке"
        assert specific_cell1 == "$100.00", f"Ожидалось $100.00, но получено {specific_cell1}"
        print("✅ Тест 1 пройден!")

        # TODO: 3) РЕШЕНО: Тест, работающий сразу с ДВУМЯ таблицами
        print("\n--- Тест 2: Сравнение Table 1 и Table 2 ---")

        # Проверяем, что заголовки в обеих таблицах одинаковые
        headers2 = table2.get_headers()
        assert headers1 == headers2, "Заголовки таблиц 1 и 2 должны совпадать"

        # Получаем Email из первой строки обеих таблиц (Email находится в 3-й колонке, индекс 2)
        email_table1 = table1.get_cell_value(row_index=0, column_index=2)
        email_table2 = table2.get_cell_value(row_index=0, column_index=2)

        # Проверяем, что у первого пользователя в обеих таблицах одинаковый email
        assert email_table1 == email_table2, f"Email не совпадает: {email_table1} != {email_table2}"
        print(f"✅ Тест 2 пройден! Email первого пользователя в обеих таблицах: {email_table1}")

        print("\n🎉 Все тесты успешно пройдены!")
        time.sleep(5)

    finally:
        driver.quit()

        # Запустить python table_page_element_example.py
