import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException  # Импортируем для отлова

# Добавляем локатор для УСПЕШНОГО входа
LOGIN_INPUT = (By.ID, "login-input")
PASSWORD_INPUT = (By.ID, "password-input")
SUBMIT_BUTTON = (By.ID, "submit-button")
STATUS_MESSAGE = (By.ID, "error-message")
WELCOME_MESSAGE = (By.ID, "welcome-message")  # <-- ДОБАВИЛИ


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.mark.parametrize(
    "email, password, expected_text",
    [
        # --- ПОЗИТИВНЫЕ СЦЕНАРИИ ---
        ("user1", "password1", "Welcome, user1!"),

        # --- НЕГАТИВНЫЕ СЦЕНАРИИ ---
        ("USER1", "password1", "Wrong login or password"),  # <-- Исправили ожидание для USER1
        ("user1", "wrong_pass", "Wrong login or password"),
        ("unknown", "password1", "Wrong login or password"),
        ("", "password1", "Login is required"),
        ("user1", "", "Password is required"),
        ("", "", "Login and password are required"),
        ("ab", "password1", "Login must be at least 3 characters"),
        ("user1", "12345", "Password must be at least 6 characters"),
        ("user1' OR '1'='1", "' OR '1'='1", "Wrong login or password"),
    ]
)
def test_login_form(driver, email, password, expected_text):
    """Тест кейс, принимающий наборы данных (DDT)."""

    driver.get("https://qa-guru.github.io/one-page-form/login.html")

    driver.find_element(*LOGIN_INPUT).send_keys(email)
    driver.find_element(*PASSWORD_INPUT).send_keys(password)
    driver.find_element(*SUBMIT_BUTTON).click()

    wait = WebDriverWait(driver, 5)
    actual_result = ""

    # УМНОЕ ОЖИДАНИЕ: Ждем либо успех, либо ошибку
    try:
        # Пытаемся дождаться сообщения об УСПЕХЕ (3 секунды)
        success_element = WebDriverWait(driver, 3).until(
            EC.visibility_of_element_located(WELCOME_MESSAGE)
        )
        actual_result = success_element.text
    except TimeoutException:
        # Если успеха нет, значит появилась ОШИБКА. Ждем её.
        error_element = wait.until(EC.visibility_of_element_located(STATUS_MESSAGE))
        actual_result = error_element.text

    # Проверка результата
    assert expected_text in actual_result, f"Ожидали '{expected_text}', но получили '{actual_result}'"

    # Запустить pytest test_login.py -v
