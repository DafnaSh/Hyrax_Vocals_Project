from selenium import webdriver
import login
import units_table_consts as const
import Loading


# this funcs receives one of the general constant URLs and creates a URL with the DB name in it (if necessary)
def get_database_url(url, database=None):
    if url.find('database=') != -1 and database is not None:
        split_url = url.split('|')
        database_url = split_url[0] + database + split_url[1]
    else:
        database_url = url
    return database_url


# This func opens koe in a visible popup screen
def open_koe_reg(url, database=None):
    database_url = get_database_url(url, database)
    driver = webdriver.Chrome()
    driver.implicitly_wait(15)
    # login to Koe:
    Login.login_func(driver)
    # opening the units' table page in koe:
    driver.get(database_url)
    Loading.loading_widget_wait(driver)
    return driver


# This func opens koe in a hidden and invisible way (does not work with one of the methods in CheckUpload).
def open_koe_headless(url, database=None):
    database_url = get_database_url(url, database)
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    headless_driver = webdriver.Chrome(options=options)
    headless_driver.implicitly_wait(15)
    # login to Koe:
    Login.login_func(headless_driver)
    # opening the units' table page in koe:
    headless_driver.get(database_url)
    Loading.loading_widget_wait(headless_driver)
    return headless_driver


# This func opens koe in a visible minimized popup screen
def open_koe_minimized(url, database=None):
    database_url = get_database_url(url, database)
    mini_driver = webdriver.Chrome()
    mini_driver.minimize_window()
    mini_driver.implicitly_wait(15)
    # login to Koe:
    Login.login_func(mini_driver)
    # opening the units' table page in koe:
    mini_driver.get(database_url)
    Loading.loading_widget_wait(mini_driver)
    return mini_driver


def open_koe(url, db_name=None, window_type=None):
    if window_type == const.MINI:
        driver = open_koe_minimized(url, db_name)
    elif window_type == const.HEADLESS:
        driver = open_koe_headless(url, db_name)
    else:
        driver = open_koe_reg(url, db_name)
    return driver
