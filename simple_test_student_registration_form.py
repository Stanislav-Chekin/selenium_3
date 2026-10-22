import os
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException  # Нужно для проверки негатива


class TestAutomationForm(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

        # ВАЖНО: Явное ожидание (Explicit Wait) для конкретных условий.
        # В отличие от implicitly_wait, оно ждет только там, где мы его вызываем.
        self.wait = WebDriverWait(self.driver, 5)
        self.url = "https://qa-guru.github.io/one-page-form/automation-practice-form.html"

    def test_fill_entire_form(self):
        """Позитивный тест: заполнение всей формы"""
        driver = self.driver
        wait = self.wait
        driver.get(self.url)

        # 0. Ожидаем загрузки страницы (проверяем видимость главного заголовка формы)
        form_title = self.wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/main/section/h1")))
        self.assertEqual(form_title.text, "Practice Form")

        # УБРАЛИ time.sleep(5) - он здесь не нужен, мы уже дождались заголовка

        form_sub_title = self.wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/main/section/div/p")))
        self.assertEqual(form_sub_title.text, "Student Registration Form")

        # 1. Убираем окно "Level up your automation"
        wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Level up your automation')]")))
        close_banner_btn = wait.until(EC.element_to_be_clickable((By.XPATH, """//*[@id="fixedban"]/div/div/button""")))
        close_banner_btn.click()
        wait.until(EC.invisibility_of_element(close_banner_btn))

        # 2. Текстовые поля
        first_name = wait.until(EC.element_to_be_clickable((By.ID, "firstName")))
        first_name.send_keys("Иван")

        driver.find_element(By.ID, "lastName").send_keys("Петров")
        driver.find_element(By.ID, "userEmail").send_keys("ivan.petrov@example.com")

        # 3. Радиокнопки (Gender)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='gender-radio-1']"))).click()

        # 4. Номер телефона
        driver.find_element(By.ID, "userNumber").send_keys("9991234567")

        # 5. Виджет календаря (Сложный элемент)
        driver.find_element(By.ID, "dateOfBirthInput").click()
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "react-datepicker__month-container")))

        month_select = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "react-datepicker__month-select")))
        month_select.click()
        month_select.find_element(By.XPATH, "//option[@value='11']").click()

        year_select = driver.find_element(By.CLASS_NAME, "react-datepicker__year-select")
        year_select.click()
        year_select.find_element(By.XPATH, "//option[@value='1995']").click()

        day_element = driver.find_element(By.CSS_SELECTOR,
                                          ".react-datepicker__day--025:not(.react-datepicker__day--outside-month)")
        day_element.click()

        # 6. Subjects (Автодополнение)
        subjects_input = wait.until(EC.element_to_be_clickable((By.ID, "subjectsInput")))
        subjects_input.send_keys("Computer Science")
        subjects_input.send_keys(Keys.ENTER)

        # 7. Чекбоксы (Hobbies)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='hobbies-checkbox-1']"))).click()
        driver.find_element(By.CSS_SELECTOR, "label[for='hobbies-checkbox-3']").click()

        # 8. Загрузка файла
        temp_file_path = os.path.abspath("test_image.jpg")
        with open(temp_file_path, "w") as f:
            f.write("fake image data")
        driver.find_element(By.ID, "uploadPicture").send_keys(temp_file_path)

        # 9. Адрес
        driver.find_element(By.ID, "currentAddress").send_keys("123456, г. Москва, ул. Ленина, д. 1")

        # 10. execute_script: Избавляемся от футера и скроллим вниз (динамический контент)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.execute_script("document.getElementsByTagName('footer')[0].style.display='none';")

        # 11. Выпадающие списки (State и City)
        wait.until(EC.element_to_be_clickable((By.ID, "state"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, """//*[@id="stateCity-wrapper"]/div[1]"""))).click()

        wait.until(EC.element_to_be_clickable((By.ID, "city"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, """//*[@id="stateCity-wrapper"]/div[1]"""))).click()

        # 12. Отправка формы (через JS, так как кнопку может перекрывать футер)
        submit_button = driver.find_element(By.ID, "submit")
        driver.execute_script("arguments[0].click();", submit_button)

        # 13. Проверка результатов
        modal_title = wait.until(EC.visibility_of_element_located((By.ID, "example-modal-sizes-title-lg")))
        self.assertEqual(modal_title.text, "Thanks for submitting the form")

        # УБРАЛИ time.sleep(5) - ожидание модального окна уже сработало

        result_table = driver.find_element(By.CLASS_NAME, "table-responsive")
        self.assertIn("Иван Петров", result_table.text)
        self.assertIn("ivan.petrov@example.com", result_table.text)
        self.assertIn("Male", result_table.text)
        self.assertIn("9991234567", result_table.text)
        self.assertIn("25 Dec 1995", result_table.text)
        self.assertIn("Computer Science", result_table.text)
        self.assertIn("Sports, Music", result_table.text)
        self.assertIn("test_image.jpg", result_table.text)
        self.assertIn("123456, г. Москва, ул. Ленина, д. 1", result_table.text)
        self.assertIn("NCR Delhi", result_table.text)

    # =======================================================
    # НОВЫЙ ТЕСТ: Начинаем покрывать форму с негативной стороны
    # =======================================================
    def test_submit_empty_form(self):
        """Негативный тест: проверяем, что пустая форма не отправляется"""
        driver = self.driver
        wait = self.wait
        driver.get(self.url)

        # Закрываем баннер
        close_banner_btn = wait.until(EC.element_to_be_clickable((By.XPATH, """//*[@id="fixedban"]/div/div/button""")))
        close_banner_btn.click()

        # Скроллим вниз и кликаем Submit, НЕ заполняя поля (через JS)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        submit_btn = driver.find_element(By.ID, "submit")
        driver.execute_script("arguments[0].click();", submit_btn)

        # Проверяем, что модальное окно НЕ появилось.
        # Мы используем assertRaises, чтобы поймать ошибку TimeoutException.
        # Если окно не появилось за 2 секунды - тест пройден.
        with self.assertRaises(TimeoutException):
            WebDriverWait(driver, 2).until(
                EC.visibility_of_element_located((By.ID, "example-modal-sizes-title-lg"))
            )

    def tearDown(self):
        if os.path.exists("test_image.jpg"):
            os.remove("test_image.jpg")
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()

    # Запустить python -m unittest simple_test_student_registration_form.py
