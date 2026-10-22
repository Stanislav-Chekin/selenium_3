from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

LOGIN_INPUT = (By.ID, "login-input")
PASSWORD_INPUT = (By.ID, "password-input")
SUBMIT_BUTTON = (By.ID, "submit-button")
STATUS_MESSAGE = (By.ID, "error-message")

# 1. Инициализация браузера
driver = webdriver.Chrome()

try:
    # 2. Открытие страницы авторизации
    driver.get("https://qa-guru.github.io/one-page-form/login.html")
    driver.maximize_window()

    # ВАЖНО: Implicit Wait (Неявное ожидание).
    # Заставляет Selenium ждать до 5 секунд при КАЖДОМ поиске элемента, если его нет.
    # В современном тестировании используется редко, так как замедляет работу.
    driver.implicitly_wait(5)

    # ВАЖНО: Explicit Wait (Явное ожидание).
    # Ждет ровно столько, сколько нужно, для конкретного условия.
    wait = WebDriverWait(driver, 10)

    # 3. Поиск элементов и заполнение формы
    driver.find_element(*LOGIN_INPUT).send_keys("qaguru@gmail.com")
    driver.find_element(*PASSWORD_INPUT).send_keys("qagurupassword")

    # 4. Нажатие кнопки "Войти" (Ждем, пока она станет кликабельной)
    submit_button = wait.until(EC.element_to_be_clickable(SUBMIT_BUTTON))
    submit_button.click()

    # 5. Проверка того что входные данные не подходят
    # Вместо time.sleep(5) используем явное ожидание появления текста ошибки
    error_element = wait.until(EC.visibility_of_element_located(STATUS_MESSAGE))
    error_message = error_element.text

    # Проверяем, что текст ошибки именно тот, который мы ожидаем
    assert "Wrong login or password" in error_message
    print("✅ Тест пройден успешно! Вввели неверные данные и не смогли войти в систему.")

finally:
    # 6. Закрытие браузера
    driver.quit()

# Команда для запуска: python the_simplest_test_login.py

