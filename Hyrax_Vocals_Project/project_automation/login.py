from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# CONSTS for login:
EMAIL = '<INSERT USER EMAIL>'
PASSWORD = '<INSERT USER PASSWORD>'
LOGIN_URL = 'https://koe.io.ac.nz/login#!'


# login to Koe:
def login_func(driver):
    driver.get(LOGIN_URL)
    username_xpath = '/html/body/div[1]/div/div/div/form/div[1]/div/input'
    password_xpath = '/html/body/div[1]/div/div/div/form/div[2]/div/input'
    driver.find_element(By.XPATH, username_xpath).send_keys(EMAIL)
    driver.find_element(By.XPATH, password_xpath).send_keys(PASSWORD + Keys.ENTER)
