from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import os.path
import glob
import UnitsTableElements as ute
import UnitsTableConsts as const
import Loading
import Screenshots
# CONSTS:
UNITS_CSV_FOLDER = const.UNITS_CSV_FOLDER
FILE_NAME_PREFIX = const.FILE_NAME_PREFIX
OUTPUT_RELOAD_FILES = const.OUTPUT_RELOAD_FILES
FILES_NUM = const.FILES_NUM
START_INDEX = const.START_INDEX
EXIT = const.EXIT
BREAK = const.BREAK
CONTINUE = const.CONTINUE
NOTHING = const.NOTHING
REFRESH = const.REFRESH


# checking when to press the Import csv after processing, called by 'upload_units_file' func
def wait_check(driver, file_num, no_wait):
    if no_wait is False:
        # opening the units table page
        if file_num == START_INDEX:
            # using try - exception
            Loading.loading_widget_wait(driver)
        # loading the units' table after process
        else:
            # using try - exception
            Loading.wait_after_import(driver)


# clicking on "Import data (csv) to table" button, using try - exception, called by 'upload_units_file' func
def clicking_import_csv(driver):
    time.sleep(10)
    for i in range(60):
        exception_msg = " 'upload_csv_modal' didn't open, try no. " + str(i)
        # using try - exception
        res = Loading.try_click_import(msg=exception_msg, driver=driver, wait_val=3)
        if res == BREAK:
            break
        time.sleep(5)
        if i > 0 and i % 5 == 0:
            driver.refresh()
            print("refreshing...")


# [NEW ver] this func uploads a unit file into Koe, called by 'import_base_actions' func in 'Main'
def upload_units_file(driver, file_path, file_num, no_wait=False):
    # making sure the input file is in the given file path
    if os.path.isfile(file_path) is False:
        return None
    driver.execute_script("document.getElementById('file-upload-form').style.display = null;")
    # clicking on "Import data (csv) to table" button, using try - exception
    clicking_import_csv(driver)
    # uploading a units csv file
    driver.find_element(By.XPATH, ute.choose_file_xpath).send_keys(file_path)
    # waiting for the file to load, using try - exception
    return_val = Loading.try_units_upload(driver=driver, wait_val=30)
    if return_val == EXIT:
        return None
    # getting upload alerts
    upload_alerts = Screenshots.get_elements(driver)
    up_alert_elements = upload_alerts[0]
    up_alert_elements_txt = upload_alerts[1]
    Screenshots.after_upload(up_alert_elements, file_num)
    # pressing the 'Process' button, using try - exception
    Loading.try_click_process(driver=driver,wait_val=7)
    no_wait = Screenshots.after_process_ver1(up_alert_elements_txt[0],driver,file_num)
    wait_check(driver, file_num, no_wait)


# [OLD ver] called by 'import_for_while_action_old' func in 'Main'
def upload_units_file_1(driver, file_num, no_wait=False):
    wait = WebDriverWait(driver, 30)
    driver.execute_script("document.getElementById('file-upload-form').style.display = null;")
    input_file_name = FILE_NAME_PREFIX + str(file_num) + ".csv"
    input_file_path = UNITS_CSV_FOLDER + input_file_name
    # clicking on "Import data (csv) to table" button
    clicking_import_csv(driver)
    # uploading a units csv file
    driver.find_element(By.XPATH, ute.choose_file_xpath).send_keys(input_file_path)
    # waiting for the file to load, using try - exception
    return_val = Loading.try_units_upload(driver=driver, wait_val=30)
    if return_val == EXIT:
        return None
    # getting upload alerts
    upload_alerts = Screenshots.get_elements(driver)
    up_alert_elements = upload_alerts[0]
    up_alert_elements_txt = upload_alerts[1]
    Screenshots.after_upload(up_alert_elements, file_num)
    # pressing the 'Process' button, using try - exception
    Loading.try_click_process(driver=driver, wait_val=7)
    no_wait = Screenshots.after_process_ver1(up_alert_elements_txt[0], driver, file_num)
    wait_check(driver, file_num, no_wait)
