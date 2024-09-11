import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


# Фикстура для инициализации и завершения работы веб-драйвера
@pytest.fixture(scope='module')
def driver():
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    yield driver
    driver.quit()


# Общая функция для авторизации
def perform_login(driver, login_method, username, password):
    # Переход на страницу авторизации
    driver.get(
        'https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=account_b2c&redirect_uri=https://b2c.passport.rt.ru/account_b2c/login&response_type=code&scope=openid&state=587c1919-a690-4117-bfad-30b1b3dd1cb4')

    # Ожидание таба, в зависимости от метода (Номер, Почта, Логин, ЛС)
    WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, login_method)))
    driver.find_element(By.XPATH, login_method).click()

    # Ввод имени пользователя и пароля
    driver.find_element(By.XPATH, '//*[@id="username"]').send_keys(username)
    driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(password)

    # Нажатие на кнопку "Войти"
    driver.find_element(By.XPATH, '//*[@id="kc-login"]').click()

    time.sleep(3)


# Тесты для негативных сценариев
def test_login_with_invalid_phone(driver):
    perform_login(driver, '//*[@id="t-btn-tab-phone"]', '9652292646', 'invalid')
    assert driver.find_element(By.XPATH, '//*[@id="form-error-message"]').text == 'Неверный логин или пароль'


def test_login_with_invalid_email(driver):
    perform_login(driver, '//*[@id="t-btn-tab-mail"]', 'invalid@mail.co', 'invalid')
    assert driver.find_element(By.XPATH, '//*[@id="form-error-message"]').text == 'Неверный логин или пароль'


def test_login_with_invalid_login(driver):
    perform_login(driver, '//*[@id="t-btn-tab-login"]', 'invalid_login', 'invalid')
    assert driver.find_element(By.XPATH, '//*[@id="form-error-message"]').text == 'Неверный логин или пароль'


def test_login_with_invalid_ls(driver):
    perform_login(driver, '//*[@id="t-btn-tab-ls"]', '999999999999', 'invalid')
    assert driver.find_element(By.XPATH, '//*[@id="form-error-message"]').text == 'Неверный логин или пароль'


# Тесты для позитивных сценариев
def test_login_with_valid_phone(driver):
    perform_login(driver, '//*[@id="t-btn-tab-phone"]', '9652292646', 'ycKAxiKzserar55')
    assert driver.find_element(By.XPATH, '//*[@id="app"]/main/div[2]/div[1]/div/div[1]/h2').text == 'Бархович Никита Олегович'
    driver.find_element(By.XPATH, '//*[@id="logout-btn"]').click()


def test_login_with_valid_email(driver):
    perform_login(driver, '//*[@id="t-btn-tab-mail"]', 'shaisikama@gmail.com', 'ycKAxiKzserar55')
    assert driver.find_element(By.XPATH, '//*[@id="app"]/main/div[2]/div[1]/div/div[1]/h2').text == 'Бархович Никита Олегович'
    driver.find_element(By.XPATH, '//*[@id="logout-btn"]').click()


def test_login_with_valid_login(driver):
    perform_login(driver, '//*[@id="t-btn-tab-login"]', 'msk17845406', 'ycKAxiKzserar55')
    assert driver.find_element(By.XPATH, '//*[@id="app"]/main/div[2]/div[1]/div/div[1]/h2').text == 'Бархович Никита Олегович'
    driver.find_element(By.XPATH, '//*[@id="logout-btn"]').click()


def test_login_with_valid_ls(driver):
    perform_login(driver, '//*[@id="t-btn-tab-ls"]', '680127486562', 'ycKAxiKzserar55')
    assert driver.find_element(By.XPATH, '//*[@id="app"]/main/div[2]/div[1]/div/div[1]/h2').text == 'Бархович Никита Олегович'
    driver.find_element(By.XPATH, '//*[@id="logout-btn"]').click()
