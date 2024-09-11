import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


# Фикстура для запуска и завершения веб-драйвера
@pytest.fixture(scope='module')
def driver():
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    yield driver
    driver.quit()


# Универсальная функция для начала процесса восстановления пароля
def initiate_password_reset(driver, method_xpath, username):
    driver.get('https://b2c.passport.rt.ru/auth/realms/b2c/login-actions/reset-credentials?client_id=account_b2c&tab_id=0QqOGUAnieg')
    WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, method_xpath)))
    driver.find_element(By.XPATH, method_xpath).click()
    driver.find_element(By.XPATH, '//*[@id="username"]').send_keys(username)
    time.sleep(15)  # Ожидание ввода капчи вручную
    driver.find_element(By.XPATH, '//*[@id="reset"]').click()


# Тест на неуспешное восстановление пароля по номеру телефона
def test_reset_password_by_phone_unsuccess(driver):
    initiate_password_reset(driver, '//*[@id="t-btn-tab-phone"]', '9652292646')

    WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="sms-reset-type"]')))
    driver.find_element(By.XPATH, '//*[@id="sms-reset-type"]').click()
    driver.find_element(By.XPATH, '//*[@id="reset-form-submit"]').click()

    time.sleep(5)  # Ожидание для ручного ввода кода из SMS

    error_message = driver.find_element(By.XPATH, '//*[@id="form-error-message"]').text
    assert error_message == 'Неверный код. Повторите попытку'


# Тест на неуспешное восстановление пароля по email
def test_reset_password_by_email_unsuccess(driver):
    initiate_password_reset(driver, '//*[@id="t-btn-tab-mail"]', 'shaisikama@gmail.com')

    WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="email-reset-type"]')))
    driver.find_element(By.XPATH, '//*[@id="email-reset-type"]').click()
    driver.find_element(By.XPATH, '//*[@id="reset-form-submit"]').click()

    time.sleep(5)  # Ожидание для ручного ввода кода из SMS

    error_message = driver.find_element(By.XPATH, '//*[@id="form-error-message"]').text
    assert error_message == 'Неверный код. Повторите попытку'


# Тест на успешное восстановление пароля по номеру телефона
def test_reset_password_by_phone_success(driver):
    initiate_password_reset(driver, '//*[@id="t-btn-tab-phone"]', '9652292646')

    WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="sms-reset-type"]')))
    driver.find_element(By.XPATH, '//*[@id="sms-reset-type"]').click()
    driver.find_element(By.XPATH, '//*[@id="reset-form-submit"]').click()

    time.sleep(25)  # Ожидание для ручного ввода кода из SMS

    WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="password-new"]')))
    driver.find_element(By.XPATH, '//*[@id="password-new"]').send_keys('ycKAxiKzserar55')
    driver.find_element(By.XPATH, '//*[@id="password-confirm"]').send_keys('ycKAxiKzserar55')
    driver.find_element(By.XPATH, '//*[@id="t-btn-reset-pass"]').click()

    time.sleep(3)
    assert driver.find_element(By.XPATH, '//*[@id="card-title"]').text == 'Авторизация'


# Тест на успешное восстановление пароля по email
def test_reset_password_by_email_success(driver):
    initiate_password_reset(driver, '//*[@id="t-btn-tab-mail"]', 'shaisikama@gmail.com')

    WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="email-reset-type"]')))
    driver.find_element(By.XPATH, '//*[@id="email-reset-type"]').click()
    driver.find_element(By.XPATH, '//*[@id="reset-form-submit"]').click()

    time.sleep(50)  # Ожидание для ручного ввода кода из письма

    WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="password-new"]')))
    driver.find_element(By.XPATH, '//*[@id="password-new"]').send_keys('ycKAxiKzserar55')
    driver.find_element(By.XPATH, '//*[@id="password-confirm"]').send_keys('ycKAxiKzserar55')
    driver.find_element(By.XPATH, '//*[@id="t-btn-reset-pass"]').click()

    time.sleep(3)
    assert driver.find_element(By.XPATH, '//*[@id="card-title"]').text == 'Авторизация'
