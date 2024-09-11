import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


# Фикстура для запуска и завершения драйвера
@pytest.fixture(scope='module')
def driver():
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    yield driver
    driver.quit()


# Общая функция для регистрации пользователя
def register_user(driver, name, surname, contact, password):
    driver.get('https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=account_b2c&redirect_uri=https://b2c.passport.rt.ru/account_b2c/login&response_type=code&scope=openid&state=587c1919-a690-4117-bfad-30b1b3dd1cb4')
    WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="t-btn-tab-phone"]')))

    # Переход на форму регистрации
    driver.find_element(By.XPATH, '//*[@id="kc-register"]').click()
    time.sleep(3)

    # Заполнение полей формы
    driver.find_element(By.XPATH, '//*[@id="page-right"]/div[1]/div[1]/div[1]/form[1]/div[1]/div[1]/div[1]/input[1]').send_keys(name)
    driver.find_element(By.XPATH, '//*[@id="page-right"]/div[1]/div[1]/div[1]/form[1]/div[1]/div[2]/div[1]/input[1]').send_keys(surname)
    driver.find_element(By.XPATH, '//*[@id="address"]').send_keys(contact)
    driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(password)
    driver.find_element(By.XPATH, '//*[@id="password-confirm"]').send_keys(password)

    # Нажатие кнопки регистрации
    driver.find_element(By.XPATH, '//*[@id="page-right"]/div[1]/div[1]/div[1]/form[1]/button[1]').click()
    time.sleep(3)


# Негативный тест на регистрацию с уже существующим email
def test_register_existing_email(driver):
    register_user(driver, 'Петр', 'Петров', 'test@test.com', 'Zxcvb123*')
    assert driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div[1]/div/form/div[1]/div/div/h2').text == 'Учётная запись уже существует'


# Негативный тест на регистрацию с уже существующим номером телефона
def test_register_existing_phone(driver):
    register_user(driver, 'Петр', 'Петров', '9652292646', 'Zxcvb123*')
    assert driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div[1]/div/form/div[1]/div/div/h2').text == 'Учётная запись уже существует'


# Негативный тест на регистрацию с пустым полем имени
def test_register_without_name(driver):
    register_user(driver, '', 'Петров', '9652292646', 'Zxcvb123*')
    assert driver.find_element(By.XPATH, '//*[@id="page-right"]/div[1]/div[1]/div[1]/form[1]/div[1]/div[1]/span[1]').text == 'Необходимо заполнить поле кириллицей. От 2 до 30 символов.'


# Негативный тест на регистрацию с именем на латинице
def test_register_with_latin_name(driver):
    register_user(driver, 'Petr', 'Петров', '9652292646', 'Zxcvb123*')
    assert driver.find_element(By.XPATH, '//*[@id="page-right"]/div[1]/div[1]/div[1]/form[1]/div[1]/div[1]/span[1]').text == 'Необходимо заполнить поле кириллицей. От 2 до 30 символов.'


# Негативный тест на регистрацию с именем менее 2 символов
def test_register_with_short_name(driver):
    register_user(driver, 'П', 'Петров', '9652292646', 'Zxcvb123*')
    assert driver.find_element(By.XPATH, '//*[@id="page-right"]/div[1]/div[1]/div[1]/form[1]/div[1]/div[1]/span[1]').text == 'Необходимо заполнить поле кириллицей. От 2 до 30 символов.'


# Негативный тест на регистрацию с именем длиннее 30 символов
def test_register_with_long_name(driver):
    register_user(driver, 'Петрййййййййййййййййййййййййййй', 'Петров', '9652292646', 'Zxcvb123*')
    assert driver.find_element(By.XPATH, '//*[@id="page-right"]/div[1]/div[1]/div[1]/form[1]/div[1]/div[1]/span[1]').text == 'Необходимо заполнить поле кириллицей. От 2 до 30 символов.'


# Позитивный тест на успешную регистрацию по номеру телефона
def test_register_phone_success(driver):
    register_user(driver, 'Петр', 'Петров', '999999999', 'Zxcvb123*')
    WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="otp"]/div[1]/div[1]/input')))
    time.sleep(25)  # Ввести код вручную
    assert driver.find_element(By.XPATH, '//*[@id="app"]/main/div[2]/div[1]/div/div[1]/h2').text == 'Петров Петр'
    driver.find_element(By.XPATH, '//*[@id="logout-btn"]').click()


# Позитивный тест на успешную регистрацию по email
def test_register_email_success(driver):
    register_user(driver, 'Петр', 'Петров', 'qwerty@test.com', 'Zxcvb123*')
    WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="otp"]/div[1]/div[1]/input')))
    time.sleep(25)  # Ввести код вручную
    assert driver.find_element(By.XPATH, '//*[@id="app"]/main/div[2]/div[1]/div/div[1]/h2').text == 'Петров Петр'
    driver.find_element(By.XPATH, '//*[@id="logout-btn"]').click()
